import dagger
from dagger import field, object_type, function

@object_type
class KumaMonitor:
    """Модуль Dagger для управления локальным контуром Uptime Kuma."""
    
    # Получаем доступ к сокету Docker на хосте
    docker_socket: dagger.Socket = field()

    @function
    async def up(self, src: dagger.Directory) -> str:
        """Запуск обоих слоев мониторинга на хосте."""
        # Базовый контейнер с Docker CLI и Docker Compose v2
        base_env = (
            dagger.container()
            .from_("docker:24.0.7-cli")
            .with_exec(["apk", "add", "--no-cache", "docker-compose"])
            .with_unix_socket("/var/run/docker.sock", self.docker_socket)
            .with_directory("/src", src)
        )

        # 1. Запуск Слой 1 (Приложение и БД)
        layer1 = await (
            base_env.with_workdir("/src/app-db")
            .with_exec(["docker", "compose", "up", "-d"])
            .stdout()
        )

        # 2. Запуск Слой 2 (Наблюдаемость)
        layer2 = await (
            base_env.with_workdir("/src/observability")
            .with_exec(["docker", "compose", "up", "-d"])
            .stdout()
        )

        return f"Слой 1 успешно запущен:\n{layer1}\nСлой 2 успешно запущен:\n{layer2}"

    @function
    async def down(self, src: dagger.Directory) -> str:
        """Остановка и очистка всех слоев мониторинга."""
        base_env = (
            dagger.container()
            .from_("docker:24.0.7-cli")
            .with_exec(["apk", "add", "--no-cache", "docker-compose"])
            .with_unix_socket("/var/run/docker.sock", self.docker_socket)
            .with_directory("/src", src)
        )

        # Останавливаем Слой 2
        layer2_down = await (
            base_env.with_workdir("/src/observability")
            .with_exec(["docker", "compose", "down"])
            .stdout()
        )

        # Останавливаем Слой 1
        layer1_down = await (
            base_env.with_workdir("/src/app-db")
            .with_exec(["docker", "compose", "down"])
            .stdout()
        )

        return f"Инфраструктура остановлена.\n{layer2_down}\n{layer1_down}"

