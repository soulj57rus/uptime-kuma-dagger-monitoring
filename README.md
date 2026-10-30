# Локальный мониторинг Uptime Kuma

Проект содержит два набора Docker Compose: Uptime Kuma с MariaDB и стек наблюдаемости (Prometheus, Grafana, Node Exporter, cAdvisor). Модуль Dagger предоставляет три команды, но **в текущей реализации они только возвращают сообщения и не запускают контейнеры и не меняют настройки Grafana**. Для работы сервисов необходимо отдельно выполнить команды Docker Compose.

## Требования

- Установленные и запущенные Docker Engine и Docker Compose (`docker compose`). Пользователь должен иметь доступ к Docker.
- Dagger CLI, если нужно запускать команды `dagger call`.
- Свободные порты 3001, 3005, 9092, 9100 и 8080.

Проверка инструментов:

```bash
docker version
docker compose version
dagger version
```

## Запуск сервисов

Выполняйте команды из **корня репозитория**. Сначала поднимите приложение: эта команда также создаёт общую сеть `kuma-shared-network`, необходимую стеку мониторинга.

```bash
docker compose -f app_db/docker-compose.yml up -d
docker compose -f observability/docker-compose.yml up -d
docker ps
```

При первом запуске Docker загрузит образы; дождитесь старта контейнеров. После изменения настроек Compose повторно выполните соответствующую команду `docker compose -f ... up -d`: Docker Compose пересоздаст контейнеры, конфигурация которых изменилась. Для проброса портов 9100 и 8080 необходимо, чтобы контейнеры Node Exporter и cAdvisor были пересозданы.

| Сервис | Адрес |
| --- | --- |
| Uptime Kuma | http://localhost:3001 |
| Grafana | http://localhost:3005 |
| Prometheus | http://localhost:9092 |
| cAdvisor | http://localhost:8080 |
| Метрики Node Exporter | http://localhost:9100/metrics |

Для входа в Grafana используются логин `admin` и пароль `admin_secure_pass`, заданный в `observability/docker-compose.yml`. При уже существующем томе Grafana пароль может отличаться. При первом открытии Uptime Kuma завершите первоначальную настройку в веб-интерфейсе.

## Команды Dagger

Если установлен Dagger CLI, из корня репозитория можно вызвать:

```bash
dagger call deploy-app --src .
dagger call deploy-monitoring --src .
dagger call configure-grafana --src .
```

**Важно:** названия команд пока не отражают их фактическое действие. В `src/kuma_monitor/main.py` функции только возвращают текст об успехе: `deploy-app` и `deploy-monitoring` не вызывают Docker Compose, а `configure-grafana` не обращается к API Grafana. Успешный вывод Dagger не означает, что сервисы запущены или источник данных создан.

## Настройка и проверка мониторинга

1. Проверьте контейнеры через `docker ps` и откройте http://localhost:9092/targets. Конфигурация Prometheus содержит цели Prometheus, Node Exporter, cAdvisor и Uptime Kuma.
2. В Grafana откройте **Connections → Data sources**, добавьте источник типа **Prometheus** с адресом `http://prometheus:9090` и режимом доступа **Server** (или **Proxy** в интерфейсе вашей версии Grafana), затем выполните **Save & test**. Указание `localhost:9092` внутри Grafana не подходит: Grafana работает в контейнере.
3. Если цель Uptime Kuma в Prometheus показывает `DOWN`, проверьте доступность `/metrics` и учётные данные для сбора метрик. В `observability/docker-compose.yml` сейчас записан статический пароль, который может не соответствовать настройкам вашей установки Uptime Kuma.

Порты 9100 и 8080 опубликованы также на хосте для просмотра метрик в браузере; для сбора метрик Prometheus обращается к экспортерам напрямую по внутренней Docker-сети.
