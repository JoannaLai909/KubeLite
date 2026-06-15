"""
Error Rules (成員 C 負責)

定義常見 Docker / Log 錯誤關鍵字，對應的中文說明與修復建議。
log_analyzer.py 會用這份規則去比對 docker compose logs 的內容。

TODO (成員 C):
- 可以依照實際測試到的 log 內容，繼續擴充這個字典
- 之後也可以把這份規則改成從 JSON / YAML 檔案讀取，方便社群貢獻新規則
"""

ERROR_RULES = {
    "connection refused": {
        "title": "服務連線失敗 (Connection Refused)",
        "explanation": "目標 container 可能尚未啟動，或服務尚未準備好接受連線。",
        "suggestions": [
            "確認目標 container 是否為 running 狀態",
            "確認連線設定 (例如 DATABASE_URL) 是否使用正確的 service name，而不是 localhost",
            "檢查 depends_on 與 healthcheck 設定是否完整",
        ],
    },
    "ECONNREFUSED": {
        "title": "前後端 / API 連線失敗",
        "explanation": "應用程式無法連接到指定的服務位址與 Port。",
        "suggestions": [
            "確認對方服務是否已啟動 (docker compose ps)",
            "確認連線位址與 Port 設定是否正確",
        ],
    },
    "address already in use": {
        "title": "Port 已被占用",
        "explanation": "Container 想要綁定的 host port 已經被其他程式使用。",
        "suggestions": [
            "使用 ss -tuln 或 netstat -ano 確認哪個程式占用該 port",
            "修改 docker-compose.yml 或使用 docker-compose.override.yml，改用其他 host port",
        ],
    },
    "ModuleNotFoundError": {
        "title": "缺少 Python 套件",
        "explanation": "容器內缺少程式執行時所需要的 Python 套件。",
        "suggestions": [
            "確認 requirements.txt 是否包含該套件",
            "重新 build image: docker compose build --no-cache",
        ],
    },
    "permission denied": {
        "title": "權限不足",
        "explanation": "容器內的程式無法存取某個檔案或目錄。",
        "suggestions": [
            "檢查 volume 掛載路徑的權限設定",
            "確認容器內執行程式的使用者是否有足夠權限",
        ],
    },
    "database is not ready": {
        "title": "資料庫尚未完成初始化",
        "explanation": "資料庫 container 可能還在啟動或初始化中，尚未可以接受連線。",
        "suggestions": [
            "為資料庫服務加上 healthcheck",
            "讓相依服務的 depends_on 設定 condition: service_healthy",
        ],
    },
    "OOMKilled": {
        "title": "Container 因記憶體不足被強制終止 (OOMKilled)",
        "explanation": "Container 使用的記憶體超過限制，被 Linux kernel 強制終止。",
        "suggestions": [
            "在 docker-compose.yml 的 deploy.resources.limits 調高記憶體上限",
            "檢查應用程式是否有記憶體洩漏 (memory leak)",
        ],
    },
    "no space left on device": {
        "title": "磁碟空間不足",
        "explanation": "Host 或 container 的磁碟已滿，無法寫入檔案。",
        "suggestions": [
            "執行 docker system prune 清理未使用的 image、volume 與 container",
            "確認 log 輸出量是否過大，考慮設定 logging.options.max-size",
        ],
    },
    "exec format error": {
        "title": "執行檔架構不符 (exec format error)",
        "explanation": "Image 的 CPU 架構（例如 arm64 / amd64）與目前 Host 不相符。",
        "suggestions": [
            "確認 image 是否支援目前平台，或在 build 時加上 --platform linux/amd64",
            "使用多架構 image（multi-arch manifest）",
        ],
    },
    "Bind for 0.0.0.0": {
        "title": "Port 綁定失敗",
        "explanation": "Docker 嘗試綁定 host port 時失敗，通常是 port 已被占用。",
        "suggestions": [
            "執行 ss -tuln 或 lsof -i :<port> 確認占用程式",
            "修改 docker-compose.yml 中的 host port 或停止占用該 port 的程式",
        ],
    },
}
