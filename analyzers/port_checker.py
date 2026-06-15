"""
Port Checker (成員 B 負責)

負責:
- 從 compose 設定中抓出 host port
- 使用 ss / netstat 檢查 host port 是否已被占用
- 提供替代 port 建議 (例如 5432 衝突 -> 55432:5432)
"""

import subprocess
import platform


def _is_port_in_use(port: int) -> bool:
    """
    檢查指定的 host port 是否已被占用。

    TODO: 依照作業系統選擇指令
        Linux/macOS: ss -tuln | grep :{port}
        Windows:     netstat -ano | findstr :{port}
    回傳 True/False
    """
    system = platform.system()

    try:
        if system == "Windows":
            result = subprocess.run(
                ["netstat", "-ano"], capture_output=True, text=True, check=False
            )
            return f":{port} " in result.stdout
        elif system == "Darwin":
            # macOS 沒有 ss，改用 lsof
            result = subprocess.run(
                ["lsof", f"-iTCP:{port}", "-sTCP:LISTEN"],
                capture_output=True, text=True, check=False
            )
            return result.returncode == 0 and bool(result.stdout.strip())
        else:
            result = subprocess.run(
                ["ss", "-tuln"], capture_output=True, text=True, check=False
            )
            return f":{port} " in result.stdout

    except FileNotFoundError:
        return False


def check_ports(compose_result):
    """
    檢查 docker-compose.yml 中宣告的 host port 是否與本機其他程式衝突。

    Args:
        compose_result (dict): analyze_compose() 的回傳結果，
                                需要用到 compose_result["services"]

    Returns:
        dict: {
            "conflicts": [str, ...],  # 例如 "5432 is already in use, 建議改用 55432:5432"
            "issues": [str, ...]
        }
    """
    conflicts = []
    issues = []

    services = compose_result.get("services", {})

    for service_name, config in services.items():
        config = config or {}
        ports = config.get("ports", [])

        for port_mapping in ports:
            # port_mapping 常見格式: "5432:5432"、"5432:5432/tcp"、或 dict 格式
            host_port = None

            if isinstance(port_mapping, str):
                # 去掉 /tcp、/udp 後綴，再取冒號前的 host port
                mapping = port_mapping.split("/")[0]
                if ":" in mapping:
                    host_part = mapping.split(":")[0]
                    if host_part.isdigit():
                        host_port = int(host_part)
            elif isinstance(port_mapping, dict):
                # dict 格式: { published: 5432, target: 5432 }
                published = port_mapping.get("published")
                if published is not None:
                    host_port = int(published)

            if host_port is not None and _is_port_in_use(host_port):
                suggested = host_port + 50000
                conflicts.append(
                    f"{service_name} 使用的 host port {host_port} 已被占用，"
                    f"建議改用 {suggested}:{host_port}"
                )
                issues.append(
                    f"{service_name} port 衝突: {host_port} 已被其他程式使用"
                )

    return {
        "conflicts": conflicts,
        "issues": issues,
    }
