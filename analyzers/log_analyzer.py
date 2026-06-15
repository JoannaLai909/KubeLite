"""
Log Analyzer (成員 C 負責)

負責:
- 執行 docker compose logs
- 依照 error_rules.py 的關鍵字規則偵測常見錯誤
- 找出哪個 service 出現了哪些問題
"""

import subprocess
from rules.error_rules import ERROR_RULES


def analyze_logs(project_path):
    """
    分析 docker compose logs，偵測常見錯誤關鍵字並對應到中文說明與建議。

    Args:
        project_path (Path): docker-compose.yml 所在的專案路徑

    Returns:
        dict: {
            "raw_logs": {service_name: log_text, ...},  # 選填，先留著給除錯用
            "findings": [
                {
                    "service": "api",                # 哪個 service 的 log 出現問題 (選填)
                    "title": "...",
                    "explanation": "...",
                    "suggestions": [...]
                },
                ...
            ]
        }
    """
    raw_logs = {}
    findings = []

    try:
        result = subprocess.run(
            ["docker", "compose", "logs", "--no-color"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )
        log_text = result.stdout

        # TODO 1: 依照 service 名稱拆分 log
        # docker compose logs 每一行格式: "service_name-1  | log內容"
        import re
        for line in log_text.splitlines():
            match = re.match(r"^([a-zA-Z0-9_-]+)-\d+\s+\|\s?(.*)", line)
            if match:
                svc = match.group(1)
                content = match.group(2)
                raw_logs.setdefault(svc, [])
                raw_logs[svc].append(content)

        # TODO 2: 用 ERROR_RULES 比對每個 service 的 log，找出是哪個 service 出了問題
        already_found = set()  # 避免同一個 service 同一個關鍵字重複回報
        for svc, lines in raw_logs.items():
            svc_log = "\n".join(lines)
            for keyword, rule in ERROR_RULES.items():
                if keyword in svc_log and (svc, keyword) not in already_found:
                    already_found.add((svc, keyword))
                    findings.append(
                        {
                            "service": svc,
                            "title": rule["title"],
                            "explanation": rule["explanation"],
                            "suggestions": rule["suggestions"],
                        }
                    )

        # 若 log 無法按 service 拆分，退回對整份 log 比對
        if not raw_logs:
            for keyword, rule in ERROR_RULES.items():
                if keyword in log_text:
                    findings.append(
                        {
                            "service": None,
                            "title": rule["title"],
                            "explanation": rule["explanation"],
                            "suggestions": rule["suggestions"],
                        }
                    )

    except FileNotFoundError:
        findings.append(
            {
                "service": None,
                "title": "找不到 docker 指令",
                "explanation": "請確認 Docker 已安裝並加入 PATH。",
                "suggestions": [],
            }
        )

    return {
        "raw_logs": raw_logs,
        "findings": findings,
    }
