"""Utility script to run infrastructure health checks from the container or CI.

This script is intentionally defensive: it will report a clear status even when
the async client libraries are not installed (so it can be used in early
bootstrap phases). It supports checks via common environment variables:

- DATABASE_URL (Postgres/MySQL style)
- REDIS_URL
- MONGODB_URI
- KAFKA_BOOTSTRAP_SERVERS (comma separated)
- RABBITMQ_URL
- SQS_REGION and AWS credentials via environment

Exit codes:
- 0: all configured checks healthy
- 2: one or more checks unhealthy

Usage:
    python -m src.utils.health_check_cli --timeout 5

This file is added to the template so projects can wire it into a Docker
Compose `healthcheck` or a Kubernetes readinessProbe command.
"""
import asyncio
import json
import os
import sys
import time
from typing import Any, Dict


async def _check_postgres(database_url: str, timeout: int) -> Dict[str, Any]:
    try:
        import asyncpg
    except Exception as e:
        return {"status": "not_available", "error": f"asyncpg import error: {e}"}

    start = time.time()
    try:
        conn = await asyncio.wait_for(asyncpg.connect(dsn=database_url), timeout=timeout)
        await asyncio.wait_for(conn.execute('SELECT 1'), timeout=timeout)
        await conn.close()
        return {"status": "healthy", "response_time_ms": round((time.time()-start)*1000,2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "response_time_ms": round((time.time()-start)*1000,2)}


async def _check_mysql(database_url: str, timeout: int) -> Dict[str, Any]:
    try:
        import aiomysql
    except Exception as e:
        return {"status": "not_available", "error": f"aiomysql import error: {e}"}
    start = time.time()
    try:
        # aiomysql needs parsed connection params; let it accept a DSN like pymysql
        # For simplicity, accept host/port/user/pass/db in env or use urlparse if provided
        import urllib.parse as _up
        p = _up.urlparse(database_url)
        conn = await asyncio.wait_for(aiomysql.connect(host=p.hostname, port=p.port or 3306,
                                                       user=p.username, password=p.password,
                                                       db=(p.path or '').lstrip('/')), timeout=timeout)
        cur = await conn.cursor()
        await cur.execute('SELECT 1')
        await cur.close()
        conn.close()
        return {"status": "healthy", "response_time_ms": round((time.time()-start)*1000,2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "response_time_ms": round((time.time()-start)*1000,2)}


async def _check_mongo(uri: str, timeout: int) -> Dict[str, Any]:
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
    except Exception as e:
        return {"status": "not_available", "error": f"motor import error: {e}"}
    start = time.time()
    try:
        client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=timeout*1000)
        await client.admin.command('ping')
        client.close()
        return {"status": "healthy", "response_time_ms": round((time.time()-start)*1000,2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "response_time_ms": round((time.time()-start)*1000,2)}


async def _check_redis(redis_url: str, timeout: int) -> Dict[str, Any]:
    try:
        import redis.asyncio as aioredis
    except Exception as e:
        return {"status": "not_available", "error": f"redis.asyncio import error: {e}"}
    start = time.time()
    try:
        client = aioredis.from_url(redis_url)
        ok = await asyncio.wait_for(client.ping(), timeout=timeout)
        await client.close()
        return {"status": "healthy" if ok else "unhealthy", "response_time_ms": round((time.time()-start)*1000,2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "response_time_ms": round((time.time()-start)*1000,2)}


async def _check_kafka(servers: str, timeout: int) -> Dict[str, Any]:
    try:
        from aiokafka import AIOKafkaAdminClient
    except Exception as e:
        return {"status": "not_available", "error": f"aiokafka import error: {e}"}
    start = time.time()
    try:
        admin = AIOKafkaAdminClient(bootstrap_servers=servers)
        await admin.start()
        topics = await asyncio.wait_for(admin.list_topics(), timeout=timeout)
        await admin.close()
        return {"status": "healthy", "topics_count": len(topics), "response_time_ms": round((time.time()-start)*1000,2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "response_time_ms": round((time.time()-start)*1000,2)}


async def _check_rabbitmq(url: str, timeout: int) -> Dict[str, Any]:
    try:
        import aio_pika
    except Exception as e:
        return {"status": "not_available", "error": f"aio_pika import error: {e}"}
    start = time.time()
    try:
        conn = await asyncio.wait_for(aio_pika.connect_robust(url), timeout=timeout)
        await conn.close()
        return {"status": "healthy", "response_time_ms": round((time.time()-start)*1000,2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "response_time_ms": round((time.time()-start)*1000,2)}


async def _check_sqs(region: str, timeout: int) -> Dict[str, Any]:
    try:
        import aioboto3
    except Exception as e:
        return {"status": "not_available", "error": f"aioboto3 import error: {e}"}
    start = time.time()
    try:
        async with aioboto3.client('sqs', region_name=region) as sqs:
            res = await asyncio.wait_for(sqs.list_queues(), timeout=timeout)
            return {"status": "healthy", "queues_count": len(res.get('QueueUrls', [])), "response_time_ms": round((time.time()-start)*1000,2)}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "response_time_ms": round((time.time()-start)*1000,2)}


async def run_checks(timeout: int = 5) -> Dict[str, Any]:
    checks: Dict[str, Any] = {"status": "healthy", "checks": {}}

    # Database
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        if db_url.startswith('postgres') or db_url.startswith('postgresql'):
            checks['checks']['database'] = await _check_postgres(db_url, timeout)
        elif db_url.startswith('mysql') or db_url.startswith('mariadb'):
            checks['checks']['database'] = await _check_mysql(db_url, timeout)
        elif db_url.startswith('mongodb'):
            checks['checks']['database'] = await _check_mongo(db_url, timeout)
        else:
            checks['checks']['database'] = {"status": "unknown_engine", "uri": db_url}
        if checks['checks']['database'].get('status') != 'healthy':
            checks['status'] = 'degraded'
    else:
        checks['checks']['database'] = {"status": "not_configured"}

    # Cache
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        checks['checks']['cache'] = await _check_redis(redis_url, timeout)
        if checks['checks']['cache'].get('status') != 'healthy':
            checks['status'] = 'degraded'
    else:
        checks['checks']['cache'] = {"status": "not_configured"}

    # Queue
    kafka = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    rabbit = os.getenv('RABBITMQ_URL')
    sqs_region = os.getenv('SQS_REGION')
    if kafka:
        checks['checks']['queue'] = await _check_kafka(kafka, timeout)
        if checks['checks']['queue'].get('status') != 'healthy':
            checks['status'] = 'degraded'
    elif rabbit:
        checks['checks']['queue'] = await _check_rabbitmq(rabbit, timeout)
        if checks['checks']['queue'].get('status') != 'healthy':
            checks['status'] = 'degraded'
    elif sqs_region:
        checks['checks']['queue'] = await _check_sqs(sqs_region, timeout)
        if checks['checks']['queue'].get('status') != 'healthy':
            checks['status'] = 'degraded'
    else:
        checks['checks']['queue'] = {"status": "not_configured"}

    return checks


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description='Run infra health checks')
    parser.add_argument('--timeout', type=int, default=5, help='per-check timeout in seconds')
    parser.add_argument('--json', action='store_true', help='print JSON only')
    args = parser.parse_args(argv)

    result = asyncio.run(run_checks(timeout=args.timeout))

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # human friendly
        print('Overall status:', result['status'])
        for name, info in result['checks'].items():
            print(f"- {name}: {info.get('status')}")
    # exit code
    if result['status'] == 'healthy' or result['status'] == 'not_configured':
        sys.exit(0)
    else:
        sys.exit(2)


if __name__ == '__main__':
    main()
