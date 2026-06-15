# KubeLite

KubeLite 是一個基於 k3s / k3d 的輕量級微服務 CI/CD 與自動擴展部署專題。

本專題整合 Flask 微服務、Docker、GitHub Actions、GitHub Container Registry 與 Kubernetes，展示從程式碼 push、Docker image build、push registry，到 k3s 部署與 rolling update 的完整 DevOps pipeline。

## Project Goals

- 建立多個 Flask 微服務
- 使用 Dockerfile 將服務容器化
- 使用 Docker Compose 進行本機測試
- 使用 GitHub Actions 自動 build Docker image
- 將 image push 到 GitHub Container Registry
- 使用 k3d / k3s 部署到 Kubernetes
- 展示 Rolling Update 與 Pod 自動修復
- 若時間允許，加入 HPA 自動擴展

## Services

| Service | Port | Description |
|---|---:|---|
| api-gateway | 5000 | 主要 API 入口 |
| calculator-service | 5001 | 提供簡單計算 API |
| message-service | 5002 | 提供版本訊息，作為 rolling update demo |

## Local Test

docker compose up --build

## API Endpoints

### api-gateway

- GET /
- GET /health
- GET /version

### calculator-service

- GET /
- GET /health
- GET /version
- GET /add?a=1&b=2
- GET /multiply?a=3&b=4

### message-service

- GET /
- GET /health
- GET /version
- GET /message

## Tech Stack

- Python Flask
- Docker
- Docker Compose
- GitHub Actions
- GitHub Container Registry
- k3d / k3s
- Kubernetes