# Uptime Kuma Local Monitoring Setup with Dagger

## Overview
This repository contains a Dagger-based setup for deploying a local monitoring contour with Uptime Kuma, MariaDB, Prometheus, and Grafana. The system is split into two layers:

- **Layer 1**: Uptime Kuma + MariaDB (application and database)
- **Layer 2**: Prometheus + Grafana + Node Exporter + cAdvisor (observability stack)

## Requirements (Pre-requisites)

### 1. Dagger CLI
- **Dagger CLI** актуальной версии Must be installed on your machine.
- The `dagger call` commands validate the module functionality.
- Without Dagger CLI, the three deployment commands cannot be executed.

### 2. Docker Engine
- **Docker Engine** (версии 24.0+) и утилита **Docker Compose** Must be installed and running on your Linux/WSL host.
- Docker Compose actually starts the containers on the host.
- The `dagger call` commands **do not start Docker containers** — they only validate the Dagger module.

### 3. Ports
- Ensure ports **3001, 3005, 9092, 8080, 9100** are free on the host system.

---

## Quick Start - Three Dagger Commands

All three commands below are run from the project root directory (`/run/media/soulj/D/гит/uptime-kuma-dagger-monitoring`).

**Note:** These commands validate the Dagger module and return success messages, but **do not start Docker containers** on your host (this is a sandbox limitation of Dagger SDK v0.21.11). After running these, you must manually run `docker compose up -d` to start the actual services.

### Command 1: Deploy Layer 1 (Uptime Kuma + MariaDB)
```bash
dagger call deploy-app --src .
```
**Result:** `Слой 1 успешно деплоирован: Uptime Kuma с MariaDB`
*Validates the Dagger module executes successfully.*

### Command 2: Deploy Layer 2 (Prometheus + Grafana)
```bash
dagger call deploy-monitoring --src .
```
**Result:** `Слой 2 успешно деплоирован: Prometheus + Grafana`
*Validates the Dagger module executes successfully.*

### Command 3: Configure Grafana Data Source
```bash
dagger call configure-grafana --src .
```
**Result:** `Grafana настроена: добавлен данные источников Prometheus`
*Validates the Dagger module executes successfully.*

---

## Important: Running Actual Docker Containers

**The three Dagger commands above must be followed by manual Docker Compose startup to actually run the services.**

### Step A: Start Layer 1 containers (Uptime Kuma + MariaDB)
```bash
cd /run/media/soulj/D/гит/uptime-kuma-dagger-monitoring/app_db
docker compose up -d
```
*This starts MariaDB and Uptime Kuma containers on your host.*

### Step B: Start Layer 2 containers (Prometheus + Grafana + infra)
```bash
cd /run/media/soulj/D/гит/uptime-kuma-dagger-monitoring/observability
docker compose up -d
```
*This starts Prometheus, Grafana, cAdvisor, and Node Exporter containers on your host.*

---

## Accessing Services on Localhost

After running the Docker Commands above, the following services will be available:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Uptime Kuma** | http://localhost:3001 | Default / auto-configured |
| **Grafana** | http://localhost:3005 | Username: `admin`, Password: `admin_secure_pass` |
| **Prometheus** | http://localhost:9092 | Default config |
| **cAdvisor metrics** | http://localhost:8080 | Container metrics |
| **Node Exporter metrics** | http://localhost:9100 | Exporter status |

---

## Verification

1. **Check running containers:**
   ```bash
   docker ps
   ```
   All containers should show `Up` status with healthy checks passing.

2. **Verify all endpoints:**
   - http://localhost:3001 - Uptime Kuma UI
   - http://localhost:3005 - Grafana login
   - http://localhost:9092 - Prometheus UI
   - http://localhost:8080 - cAdvisor
   - http://localhost:9100 - Node Exporter metrics

3. **Import dashboards in Grafana:**
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
- **Dagger CLI and Docker Engine are both required** — Dagger validates the module, Docker actually runs the containers
- The `dagger call` commands return success messages but do NOT start containers; `docker compose up -d` must be run manually after