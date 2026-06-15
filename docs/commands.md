# Useful Commands

## Docker Compose

啟動服務：

docker compose up --build

關閉服務：

docker compose down

查看服務：

docker compose ps

查看 logs：

docker compose logs

---

## Docker Images

查看 images：

docker images

Build api-gateway：

docker build -t kubelite-api-gateway ./services/api-gateway

Build calculator-service：

docker build -t kubelite-calculator-service ./services/calculator-service

Build message-service：

docker build -t kubelite-message-service ./services/message-service

---

## k3d

建立 cluster：

k3d cluster create kubelite --agents 2 -p "8080:80@loadbalancer"

查看 cluster：

k3d cluster list

刪除 cluster：

k3d cluster delete kubelite

---

## kubectl

查看 nodes：

kubectl get nodes

套用所有 Kubernetes YAML：

kubectl apply -f k8s/

查看 pods：

kubectl get pods -n kubelite

查看 services：

kubectl get svc -n kubelite

查看 rolling update：

kubectl rollout status deployment/message-service -n kubelite

即時觀察 pods：

kubectl get pods -n kubelite -w