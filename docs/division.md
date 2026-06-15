# Division of Work

## 成員 A：微服務與 Docker 化

負責內容：

- 建立 Flask 微服務
- 撰寫 Dockerfile
- 撰寫 docker-compose.yml
- 本機測試三個服務
- 建立 /health 與 /version API

負責服務：

- api-gateway
- calculator-service
- message-service

---

## 成員 B：GitHub Actions 與 GHCR

負責內容：

- 撰寫 GitHub Actions workflow
- 自動 build Docker image
- 自動 push image 到 GitHub Container Registry
- 設定 latest 與 commit SHA tag
- 確認 GitHub Packages image 成功產生

---

## 成員 C：k3d / k3s 與 Kubernetes 部署

負責內容：

- 建立 k3d / k3s cluster
- 撰寫 Kubernetes Deployment
- 撰寫 Kubernetes Service
- 部署 image 到 cluster
- 展示 Rolling Update
- 展示 Pod 自動修復
- 嘗試 HPA 自動擴展