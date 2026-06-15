# DockDoctor

Docker Compose 專案診斷與中文化修復建議工具。

## 簡介

DockDoctor 會掃描你的 Docker Compose 專案，檢查：

- `docker-compose.yml` 設定 (ports / environment / depends_on / healthcheck / restart / volumes)
- container 實際執行狀態 (running / exited / restarting / unhealthy)
- host port 是否衝突
- `docker compose logs` 中常見的錯誤訊息

並輸出中文化的 Markdown 診斷報告 `dockdoctor-report.md`。

## 安裝

```bash
pip install -r requirements.txt
```

## 使用方式

在你要診斷的 Docker Compose 專案目錄下執行：

```bash
python dockdoctor.py scan
```

或指定其他專案路徑：

```bash
python dockdoctor.py scan --path ./examples/good-compose
```

## 專案結構

```
DockDoctor/
├─ dockdoctor.py              # 主程式入口
├─ analyzers/
│  ├─ compose_analyzer.py     # 成員 A: 解析 docker-compose.yml
│  ├─ container_checker.py    # 成員 B: 檢查 container 狀態
│  ├─ port_checker.py         # 成員 B: 檢查 port 衝突
│  └─ log_analyzer.py         # 成員 C: 分析 docker compose logs
├─ rules/
│  └─ error_rules.py          # 成員 C: 常見錯誤規則與中文建議
├─ reports/
│  └─ report_generator.py     # 成員 C: 產生 Markdown 診斷報告
├─ examples/
│  ├─ good-compose/           # 正常的範例專案
│  └─ broken-compose/         # 故意設計成有問題的範例專案 (Demo 用)
├─ requirements.txt
└─ README.md
```

## 開發分工

- **成員 A**：`analyzers/compose_analyzer.py`
- **成員 B**：`analyzers/container_checker.py`、`analyzers/port_checker.py`
- **成員 C**：`analyzers/log_analyzer.py`、`rules/error_rules.py`、`reports/report_generator.py`

每個檔案裡都已經寫好函式簽名、docstring 與 `TODO` 註解，請依照註解實作對應的檢查邏輯。

## 目前進度

- [x] 專案骨架 (Day 1)
- [ ] compose_analyzer 實作
- [ ] container_checker / port_checker 實作
- [ ] log_analyzer / error_rules / report_generator 實作
- [ ] 整合測試 (good-compose / broken-compose)
- [ ] Demo 案例設計
