"""
Compose Analyzer (成員 A 負責)

負責:
- 讀取 docker-compose.yml
- 解析 services
- 檢查 ports / environment / depends_on / healthcheck / restart / volumes
- 檢查 environment 是否出現 localhost
"""

import yaml


def analyze_compose(compose_file_path):
    """
    讀取並解析 docker-compose.yml，回傳設定檢查結果。

    Args:
        compose_file_path (Path): docker-compose.yml 的路徑

    Returns:
        dict: {
            "services": {...},   # 原始 service 設定 (給其他模組用，例如 port_checker)
            "issues": [str, ...] # 中文診斷訊息清單
        }
    """
    with open(compose_file_path, "r", encoding="utf-8") as f:
        compose_data = yaml.safe_load(f) or {}

    services = compose_data.get("services", {})
    issues = []

    for service_name, config in services.items():
        config = config or {}

        # TODO 1: 檢查是否有 restart policy
        if "restart" not in config:
            issues.append(f"{service_name} 缺少 restart policy，建議加上 restart: unless-stopped")

        # TODO 2: 檢查是否有 healthcheck
        if "healthcheck" not in config:
            issues.append(f"{service_name} 缺少 healthcheck，其他服務的 depends_on 可能無法正確等待它就緒")

        # TODO 3: 檢查 depends_on 設定是否合理
        depends_on = config.get("depends_on")
        if depends_on:
            # dict 格式: depends_on: { db: { condition: service_healthy } }
            if isinstance(depends_on, dict):
                for dep_name, dep_config in depends_on.items():
                    dep_config = dep_config or {}
                    condition = dep_config.get("condition")
                    if condition != "service_healthy":
                        issues.append(
                            f"{service_name} 的 depends_on.{dep_name} 未設定 condition: service_healthy，"
                            f"可能在 {dep_name} 尚未就緒時就嘗試連線"
                        )
            # list 格式: depends_on: [db]
            elif isinstance(depends_on, list):
                for dep_name in depends_on:
                    issues.append(
                        f"{service_name} 的 depends_on.{dep_name} 使用舊版 list 格式，"
                        f"無法等待 {dep_name} 健康就緒，建議改用 dict 格式並加上 condition: service_healthy"
                    )

        # TODO 4: 檢查 environment 是否使用 localhost
        environment = config.get("environment", [])
        if isinstance(environment, list):
            env_pairs = {}
            for item in environment:
                if "=" in str(item):
                    key, _, value = str(item).partition("=")
                    env_pairs[key.strip()] = value.strip()
        elif isinstance(environment, dict):
            env_pairs = {k: str(v) for k, v in environment.items()}
        else:
            env_pairs = {}

        for key, value in env_pairs.items():
            if "localhost" in value:
                issues.append(
                    f"{service_name} 的 {key} 包含 localhost，"
                    f"Docker 內部 container 之間應使用 service name 互相連線，而非 localhost"
                )

        # TODO 5: 檢查 volumes 設定
        volumes = config.get("volumes", [])
        for volume in volumes:
            # volumes 可能是 "host_path:container_path" 字串或 dict 格式
            if isinstance(volume, str):
                parts = volume.split(":")
                host_part = parts[0] if parts else ""
                # 只檢查 bind mount（以 . 或 / 開頭），named volume 不需要檢查路徑存在
                if host_part.startswith(".") or host_part.startswith("/"):
                    from pathlib import Path
                    if not Path(host_part).exists():
                        issues.append(
                            f"{service_name} 的 volume 掛載來源路徑 '{host_part}' 不存在，"
                            f"container 啟動後可能出現空目錄或權限問題"
                        )

    return {
        "services": services,
        "issues": issues,
    }
