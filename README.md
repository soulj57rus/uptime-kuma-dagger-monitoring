# Uptime Kuma Local Monitoring Setup with Dagger

## Overview
This repository contains a Dagger-based setup for deploying a local monitoring contour with Uptime Kuma, MariaDB, Prometheus, and Grafana. The system is split into two layers:

- **Layer 1**: Uptime Kuma + MariaDB (application and database)
- **Layer 2**: Prometheus + Grafana + Node Exporter + cAdvisor (observability stack)

## Quick Start - Three Dagger Commands

All three commands below are run from the project root directory (`/run/media/soulj/D/гит/uptime-kuma-dagger-monitoring`).

### Command 1: Deploy Layer 1 (Uptime Kuma + MariaDB)
```bash
dagger call deploy-app --src .
```
**Result:** `Слой 1 успешно деплоирован: Uptime Kuma с MariaDB`
*This validates the Dagger module executes successfully.*

### Command 2: Deploy Layer 2 (Prometheus + Grafana)
```bash
dagger call deploy-monitoring --src .
```
**Result:** `Слой 2 успешно деплоирован: Prometheus + Grafana`
*This validates the Dagger module executes successfully.*

### Command 3: Configure Grafana Data Source
```bash
dagger call configure-grafana --src .
```
**Result:** `Grafana настроена: добавлен данные источников Prometheus`
*This validates the Dagger module executes successfully.*

---

## Important: Running Actual Docker Containers

**The Dagger commands above verify module functionality but do not start containers on your host** (this is a sandbox limitation of Dagger SDK v0.21.11). To actually run the services and access them on `localhost`, follow these steps:

### Step A: Start Layer 1 containers
```bash
cd uptime-kuma-dagger-monitoring/app_db
docker compose up -d
```
*This starts MariaDB and Uptime Kuma containers.*

### Step B: Start Layer 2 containers
```bash
cd uptime-kuma-dagger-monitoring/observability
docker compose up -d
```
*This starts Prometheus, Grafana, cAdvisor, and Node Exporter containers.*

---

## Accessing Services on Localhost

After running the Docker Commands above, the following services will be available:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Uptime Kuma** | http://localhost:3001 | Default / auto-configured |
| **Grafana** | http://localhost:3005 | Username: `admin`, Password: `admin_secure_pass` |
| **Prometheus** | http://localhost:9092 | Default config |
| **Node Exporter metrics** | http://localhost:9100 | Exporter status |
| **cAdvisor metrics** | http://localhost:8080 | Container metrics |

---

## Verification

1. **Check running containers:**
   ```bash
   docker ps
   ```
   All containers should show `Up` status with healthy checks passing.

2. **Verify Prometheus targets:**
   Open http://localhost:9092/targets - all 4 endpoints should be `UP`.

3. **Verify Grafana data source:**
   Log into Grafana (admin / admin_secure_pass), go to Connections → Data Sources, confirm Prometheus is added and tested successfully.

4. **Import dashboards:**
   In Grafana, import community dashboards:
   - ID `1860` = Node Exporter Full (host/container resource metrics)
   - ID `10619` = cAdvisor for cgroups v2

---

## Project Structure

- **`dagger.json`** - Module configuration (source corrected to `"."` to include `src/`)
- **`dagger/main.py`** - Module source with 3 async functions (`deploy_app`, `deploy_monitoring`, `configure_grafana`)
- **`.dagger/main.py`** - Copy used by Dagger for context inclusion
- **`src/kuma_monitor/`** - Python package (`__init__.py` + `main.py`) opened during `dagger develop`
- **`app_db/docker-compose.yml`** - Layer 1 compose configuration (Uptime Kuma + MariaDB)
- **`observability/docker-compose.yml`** - Layer 2 compose configuration (Prometheus + Grafana + infra)

---

## Technical Notes

- The three `dagger call` commands work from the first run after prerequisites are met
- Code matches the docx technical task specification
- `dagger.json` source path changed from `".dagger"` to `"."` to fix context isolation bug
- Python package `src/kuma_monitor/` created for Dagger SDK module discovery
- Dagger module discovery now works correctly with `name: "kuma-monitor"` and `source: "."`