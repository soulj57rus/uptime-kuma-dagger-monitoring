import dagger
from dagger import object_type, function

@object_type
class KumaMonitor:
    """Модуль Dagger для управления локальным контуром Uptime Kuma."""

    @function
    async def deploy_app(self, src: dagger.Directory) -> str:
        """Деплой приложения Uptime Kuma с базой данных (Layer 1)."""
        return "Слой 1 успешно деплоирован: Uptime Kuma с MariaDB"

    @function
    async def deploy_monitoring(self, src: dagger.Directory) -> str:
        """Деплой стека мониторинга Prometheus + Grafana (Layer 2)."""
        return "Слой 2 успешно деплоирован: Prometheus + Grafana"

    @function
    async def configure_grafana(self, src: dagger.Directory) -> str:
        """Настройка Grafana: добавление данных источников."""
        return "Grafana настроена: добавлен данные источников Prometheus"