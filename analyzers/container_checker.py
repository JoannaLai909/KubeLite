"""
Container Checker (成員 B 負責)

負責:
- 執行 docker compose ps
- 判斷 container 是否 running / exited / restarting / unhealthy
- 必要時執行 docker inspect 取得細節
"""

import subprocess
import json


def check_containers(project_path):
    """
    檢查目前 Docker Compose 專案中各 container 的執行狀態。

    Args:
        project_path (Path): docker-compose.yml 所在的專案路徑

    Returns:
        dict: {
            "status": {service_name: state, ...},  # 例如 {"web": "running", "api": "exited"}
            "issues": [str, ...]                    # 中文診斷訊息清單
        }
    """
    status = {}
    issues = []

    try:
        # docker compose ps --format json 會印出多行 JSON (JSON Lines)
        result = subprocess.run(
            ["docker", "compose", "ps", "--format", "json"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )

        # TODO 1: 解析 result.stdout（每一行是一個 JSON 物件）
        for line in result.stdout.strip().splitlines():
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                service_name = item.get("Service") or item.get("Name", "unknown")
                state = item.get("State", "unknown")
                status[service_name] = state
            except json.JSONDecodeError:
                continue

        # TODO 2: 依照 state 產生中文 issues
        for svc, state in status.items():
            if state == "exited":
                issues.append(
                    f"{svc} container 已停止 (exited)，"
                    f"建議執行 docker compose up -d {svc} 或檢查 docker compose logs {svc}"
                )
            elif state == "restarting":
                issues.append(
                    f"{svc} container 持續重啟中，可能是啟動失敗，"
                    f"請執行 docker compose logs {svc} 查看原因"
                )
            elif state == "unhealthy":
                issues.append(
                    f"{svc} container 狀態為 unhealthy，healthcheck 未通過，"
                    f"請確認服務是否正常啟動"
                )

        # TODO 3 (進階): 對 unhealthy 的 container 用 docker inspect 取得 healthcheck 細節
        unhealthy_services = [svc for svc, state in status.items() if state == "unhealthy"]
        for svc in unhealthy_services:
            inspect_result = subprocess.run(
                ["docker", "inspect", "--format", "{{json .State.Health}}", svc],
                capture_output=True,
                text=True,
                check=False,
            )
            if inspect_result.returncode == 0 and inspect_result.stdout.strip():
                try:
                    health = json.loads(inspect_result.stdout.strip())
                    last_log = (health.get("Log") or [{}])[-1]
                    output = last_log.get("Output", "").strip()
                    if output:
                        issues.append(f"{svc} healthcheck 最後輸出: {output}")
                except json.JSONDecodeError:
                    pass

        if result.returncode != 0 and not status:
            issues.append("無法取得 container 狀態，請確認專案路徑下有 docker-compose.yml 且服務已啟動")

    except FileNotFoundError:
        issues.append("找不到 docker 指令，請確認 Docker 已安裝並加入 PATH")

    return {
        "status": status,
        "issues": issues,
    }
