"""Simple background worker for the template.

This worker provides a minimal, well-behaved entrypoint so that generated
projects (and the local `docker-compose` setups) can run `python -m src.worker`
without failing when no more advanced worker implementation is needed.

It will initialize database/cache managers if configured, then wait for
termination signals and shut down gracefully.
"""
import asyncio
import signal
from typing import Optional

from src.config import Settings, InfrastructureConfig
from src.utils.logging import setup_logging, get_logger
from src.utils.database import DatabaseManager
from src.utils.cache import CacheManager


class Worker:
    def __init__(self):
        self.settings = Settings()
        self.infra = InfrastructureConfig()
        self.logger = get_logger(__name__)

        self.db: Optional[DatabaseManager] = None
        self.cache: Optional[CacheManager] = None
        self._shutdown = asyncio.Event()

    async def initialize(self):
        self.logger.info("Initializing worker components")
        if self.infra.database != 'none':
            self.db = DatabaseManager(self.settings, self.infra)
            await self.db.initialize()

        if self.infra.cache != 'none':
            self.cache = CacheManager(self.settings, self.infra)
            await self.cache.initialize()

    async def start(self):
        await self.initialize()
        self.logger.info("Worker started — waiting for shutdown signal")
        await self._shutdown.wait()
        await self.shutdown()

    async def shutdown(self):
        self.logger.info("Worker shutting down")
        if self.cache:
            try:
                await self.cache.close()
            except Exception:
                self.logger.exception("Error closing cache")
        if self.db:
            try:
                await self.db.close()
            except Exception:
                self.logger.exception("Error closing database")

    def handle_signal(self, *_args):
        self.logger.info("Shutdown signal received")
        self._shutdown.set()


async def main():
    settings = Settings()
    setup_logging(settings.LOG_LEVEL)
    logger = get_logger(__name__)

    worker = Worker()
    signal.signal(signal.SIGTERM, lambda s, f: worker.handle_signal(s, f))
    signal.signal(signal.SIGINT, lambda s, f: worker.handle_signal(s, f))

    try:
        await worker.start()
    except Exception:
        logger.exception("Worker failed")
        raise


if __name__ == '__main__':
    asyncio.run(main())
