# Grafana Dashboard Setup Guide

## Node Exporter Dashboard

The cookiecutter template includes automatic provisioning of a Node Exporter dashboard in Grafana.

### What's Included

When you generate a microservice with `enable_node_exporter=yes` and `deploy_monitoring_stack=yes`, the following is automatically configured:

1. **Node Exporter** - Collects system metrics (CPU, memory, disk, network)
2. **Prometheus** - Scrapes metrics from Node Exporter
3. **Grafana** - Pre-configured dashboard for visualizing Node Exporter metrics

### Accessing the Dashboard

#### Docker Compose

1. Start your services:
   ```bash
   docker-compose up -d
   ```

2. Access Grafana at http://localhost:3000
   - Username: `admin`
   - Password: `admin`

3. The Node Exporter dashboard is automatically available at:
   - Navigate to **Dashboards** → **Node Exporter Dashboard**

#### Kubernetes

1. Deploy monitoring stack:
   ```bash
   kubectl apply -f k8s/monitoring/
   ```

2. Port-forward Grafana:
   ```bash
   kubectl port-forward svc/grafana 3000:3000
   ```

3. Access at http://localhost:3000 (admin/admin)

### Dashboard Metrics

The pre-configured dashboard includes:

- **CPU Usage** - CPU utilization across all cores
- **Memory Usage** - RAM utilization percentage
- **Disk Usage** - Filesystem usage for root mount
- **Network Traffic** - Receive/transmit bytes per second
- **System Load** - 1-minute load average
- **System Uptime** - Time since last boot

### Manual Import (Alternative Method)

If you want to manually import the dashboard:

1. **From Grafana UI:**
   - Go to **Dashboards** → **Import**
   - Upload `monitoring/node-exporter-dashboard.json`
   - Select Prometheus datasource
   - Click **Import**

2. **From Grafana.com:**
   - Go to **Dashboards** → **Import**
   - Enter dashboard ID: `1860` (Node Exporter Full)
   - Select Prometheus datasource
   - Click **Load** then **Import**

### Customizing the Dashboard

The dashboard is fully editable. You can:

1. **Add new panels** with custom PromQL queries
2. **Modify existing panels** to show different metrics
3. **Save changes** to your dashboard
4. **Export the dashboard** as JSON for version control

### Common PromQL Queries

Here are some useful queries for Node Exporter:

```promql
# CPU Usage by mode
rate(node_cpu_seconds_total[5m])

# Memory usage percentage
100 * (1 - ((node_memory_MemAvailable_bytes) / (node_memory_MemTotal_bytes)))

# Disk I/O
rate(node_disk_read_bytes_total[5m])
rate(node_disk_written_bytes_total[5m])

# Network bandwidth
rate(node_network_receive_bytes_total[5m])
rate(node_network_transmit_bytes_total[5m])

# Disk space available
node_filesystem_avail_bytes{mountpoint="/"}

# System load
node_load1
node_load5
node_load15
```

### Troubleshooting

**Dashboard not appearing?**
- Check Grafana logs: `docker-compose logs grafana`
- Verify dashboard provisioning: Check `/etc/grafana/provisioning/dashboards/` in the container

**No data in panels?**
- Verify Prometheus is scraping Node Exporter: http://localhost:9090/targets
- Check Node Exporter is running: http://localhost:9100/metrics
- Verify datasource in Grafana: Configuration → Data Sources → Prometheus

**Permission errors?**
- Ensure dashboard files have correct permissions
- Check Grafana container can read mounted volumes

### Additional Resources

- [Node Exporter GitHub](https://github.com/prometheus/node_exporter)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [Prometheus Query Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Node Exporter Dashboard ID: 1860](https://grafana.com/grafana/dashboards/1860)
