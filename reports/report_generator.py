"""
Report Generator (成員 C 負責)

負責:
- 把 compose_analyzer / container_checker / port_checker / log_analyzer
  的結果整合在一起
- 輸出成中文 Markdown 診斷報告 (dockdoctor-report.md)

未來展望: 也可以輸出 HTML 版本 (output_format == "html")
"""

from pathlib import Path
from datetime import datetime


def generate_report(results, output_format="md"):
    """
    依照診斷結果產生報告檔案。

    Args:
        results (dict): {
            "compose": analyze_compose() 的結果,
            "containers": check_containers() 的結果,
            "ports": check_ports() 的結果,
            "logs": analyze_logs() 的結果,
        }
        output_format (str): "md" 或 "html" (目前先實作 md)

    Returns:
        str: 輸出檔案的路徑
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("# DockDoctor 診斷報告")
    lines.append(f"產生時間: {timestamp}\n")

    # [Compose Check]
    lines.append("## Compose 設定檢查")
    compose_issues = results.get("compose", {}).get("issues", [])
    if compose_issues:
        for issue in compose_issues:
            lines.append(f"- {issue}")
    else:
        lines.append("- 未發現問題")

    # [Container Status]
    lines.append("\n## Container 狀態")
    status = results.get("containers", {}).get("status", {})
    if status:
        for service, state in status.items():
            lines.append(f"- {service}: {state}")
    else:
        lines.append("- 無法取得 container 狀態")

    container_issues = results.get("containers", {}).get("issues", [])
    for issue in container_issues:
        lines.append(f"- {issue}")

    # [Port Check]
    lines.append("\n## Port 檢查")
    conflicts = results.get("ports", {}).get("conflicts", [])
    if conflicts:
        for conflict in conflicts:
            lines.append(f"- {conflict}")
    else:
        lines.append("- 未發現 Port 衝突")

    # [Log Analysis]
    lines.append("\n## Log 分析")
    findings = results.get("logs", {}).get("findings", [])
    if findings:
        for finding in findings:
            service = finding.get("service")
            prefix = f"[{service}] " if service else ""
            lines.append(f"- {prefix}{finding.get('title', '')}")
            lines.append(f"  - 說明: {finding.get('explanation', '')}")
            for suggestion in finding.get("suggestions", []):
                lines.append(f"  - 建議: {suggestion}")
    else:
        lines.append("- 未發現已知錯誤")

    if output_format == "html":
        md_content = "\n".join(lines)
        html_lines = [
            "<!DOCTYPE html>",
            "<html lang='zh-Hant'>",
            "<head><meta charset='utf-8'>",
            "<title>DockDoctor 診斷報告</title>",
            "<style>",
            "  body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }",
            "  h1 { color: #2563eb; } h2 { color: #1e40af; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px; }",
            "  li { margin: 4px 0; } ul { padding-left: 20px; }",
            "  p { color: #6b7280; font-size: 0.9em; }",
            "</style></head><body>",
        ]
        for line in lines:
            if line.startswith("# "):
                html_lines.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith("## "):
                html_lines.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith("- "):
                html_lines.append(f"<ul><li>{line[2:]}</li></ul>")
            elif line.startswith("  - "):
                html_lines.append(f"<ul style='margin-left:20px'><li>{line[4:]}</li></ul>")
            elif line.strip():
                html_lines.append(f"<p>{line}</p>")
        html_lines.append("</body></html>")

        output_path = Path("dockdoctor-report.html")
        output_path.write_text("\n".join(html_lines), encoding="utf-8")
        return str(output_path)

    output_path = Path("dockdoctor-report.md")
    output_path.write_text("\n".join(lines), encoding="utf-8")

    return str(output_path)
