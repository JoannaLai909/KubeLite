"""
Docker Remote Analyzer

使用 Docker SDK 連線到遠端 Docker 主機，
取得 container 狀態與 logs（替代本地 subprocess 版本）。
"""

import docker
from rules.error_rules import ERROR_RULES


def get_docker_client(docker_host: str):
    """建立遠端 Docker client，連線失敗時拋出例外。"""
    return docker.DockerClient(base_url=docker_host, timeout=10)


def check_containers_remote(docker_host: str, project_name: str = None):
    """
    透過 Docker SDK 取得遠端主機的 container 狀態。

    Args:
        docker_host: 遠端 Docker API 位址，例如 tcp://192.168.1.100:2375
        project_name: Compose 專案名稱（用來篩選 container），可為 None

    Returns:
        dict: { "status": {service: state}, "issues": [...] }
    """
    status = {}
    issues = []

    try:
        client = get_docker_client(docker_host)
        containers = client.containers.list(all=True)

        for container in containers:
            labels = container.labels or {}
            # docker compose 的 container 會有這個 label
            service = labels.get("com.docker.compose.service")
            proj = labels.get("com.docker.compose.project")

            if project_name and proj != project_name:
                continue

            if not service:
                service = container.name

            state = container.status  # running / exited / restarting / paused
            status[service] = state

        for svc, state in status.items():
            if state == "exited":
                issues.append(
                    f"{svc} container 已停止 (exited)，"
                    f"建議執行 docker compose up -d {svc} 或檢查 logs"
                )
            elif state == "restarting":
                issues.append(
                    f"{svc} container 持續重啟中，可能是啟動失敗，請檢查 logs"
                )
            elif state == "unhealthy":
                issues.append(
                    f"{svc} container healthcheck 未通過，請確認服務是否正常啟動"
                )

        client.close()

    except docker.errors.DockerException as e:
        issues.append(f"無法連線到遠端 Docker ({docker_host})：{e}")

    return {"status": status, "issues": issues}


def analyze_logs_remote(docker_host: str, project_name: str = None):
    """
    透過 Docker SDK 取得遠端主機的 container logs 並比對錯誤規則。

    Args:
        docker_host: 遠端 Docker API 位址
        project_name: Compose 專案名稱，可為 None

    Returns:
        dict: { "raw_logs": {service: log_text}, "findings": [...] }
    """
    raw_logs = {}
    findings = []

    try:
        client = get_docker_client(docker_host)
        containers = client.containers.list(all=True)

        for container in containers:
            labels = container.labels or {}
            service = labels.get("com.docker.compose.service")
            proj = labels.get("com.docker.compose.project")

            if project_name and proj != project_name:
                continue

            if not service:
                service = container.name

            try:
                log_bytes = container.logs(tail=200, timestamps=False)
                log_text = log_bytes.decode("utf-8", errors="replace")
                raw_logs[service] = log_text
            except Exception:
                continue

        already_found = set()
        for svc, log_text in raw_logs.items():
            for keyword, rule in ERROR_RULES.items():
                if keyword in log_text and (svc, keyword) not in already_found:
                    already_found.add((svc, keyword))
                    findings.append({
                        "service": svc,
                        "title": rule["title"],
                        "explanation": rule["explanation"],
                        "suggestions": rule["suggestions"],
                    })

        client.close()

    except docker.errors.DockerException as e:
        findings.append({
            "service": None,
            "title": "無法連線到遠端 Docker",
            "explanation": str(e),
            "suggestions": ["確認 Docker host 位址是否正確", "確認遠端主機的 Docker API 已開放（預設 port 2375）"],
        })

    return {"raw_logs": raw_logs, "findings": findings}
