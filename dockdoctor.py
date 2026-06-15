#!/usr/bin/env python3
"""
DockDoctor - Docker Compose 專案診斷與中文化修復建議工具

使用方式:
    python dockdoctor.py scan
    python dockdoctor.py scan --path ./your-project
    python dockdoctor.py scan --path ./your-project --format md
"""

import argparse
import sys
from pathlib import Path

from analyzers.compose_analyzer import analyze_compose
from analyzers.container_checker import check_containers
from analyzers.port_checker import check_ports
from analyzers.log_analyzer import analyze_logs
from reports.report_generator import generate_report


def run_scan(project_path: str, output_format: str = "md"):
    project_path = Path(project_path)

    compose_file = project_path / "docker-compose.yml"
    if not compose_file.exists():
        compose_file = project_path / "docker-compose.yaml"

    if not compose_file.exists():
        print(f"[錯誤] 在 {project_path} 找不到 docker-compose.yml")
        sys.exit(1)

    print(f"[DockDoctor] 開始診斷專案: {project_path}\n")

    results = {}

    print("[1/4] 解析 Compose 設定 (compose_analyzer)...")
    results["compose"] = analyze_compose(compose_file)

    print("[2/4] 檢查 Container 狀態 (container_checker)...")
    results["containers"] = check_containers(project_path)

    print("[3/4] 檢查 Port 衝突 (port_checker)...")
    results["ports"] = check_ports(results["compose"])

    print("[4/4] 分析 Docker Logs (log_analyzer)...")
    results["logs"] = analyze_logs(project_path)

    report_path = generate_report(results, output_format=output_format)
    print(f"\n[完成] 診斷報告已輸出: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="DockDoctor - Docker Compose 專案診斷工具"
    )
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="掃描並診斷 Docker Compose 專案")
    scan_parser.add_argument(
        "--path", default=".", help="Docker Compose 專案路徑 (預設為目前目錄)"
    )
    scan_parser.add_argument(
        "--format", default="md", choices=["md", "html"], help="輸出報告格式 (目前先支援 md)"
    )

    args = parser.parse_args()

    if args.command == "scan":
        run_scan(args.path, args.format)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
