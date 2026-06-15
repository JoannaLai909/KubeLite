# Demo Steps

## Demo 1: Local Docker Compose

Step 1：啟動本機服務

docker compose up --build

Step 2：查看 container 狀態

docker compose ps

Step 3：測試 API

curl http://localhost:5000/health  
curl http://localhost:5001/add?a=1&b=2  
curl http://localhost:5002/message  

---

## Demo 2: GitHub Actions Build

Step 1：修改 message-service 版本文字

Hello from KubeLite v1  
改成  
Hello from KubeLite v2  

Step 2：提交並 push

git add .  
git commit -m "Update message service version"  
git push  

Step 3：查看 GitHub Actions

確認 workflow 是否成功。

Step 4：查看 GitHub Packages

確認 image 是否成功 push 到 GHCR。

---

## Demo 3: Kubernetes Deployment

Step 1：套用 Kubernetes YAML

kubectl apply -f k8s/

Step 2：查看 pods

kubectl get pods -n kubelite

Step 3：查看 services

kubectl get svc -n kubelite

---

## Demo 4: Rolling Update

Step 1：更新 image

kubectl set image deployment/message-service message-service=ghcr.io/USERNAME/REPO/message-service:TAG -n kubelite

Step 2：查看 rollout 狀態

kubectl rollout status deployment/message-service -n kubelite

Step 3：觀察 Pod 更新

kubectl get pods -n kubelite -w

---

## Demo 5: Pod Self-healing

Step 1：刪除 pod

kubectl delete pod <pod-name> -n kubelite

Step 2：觀察 pod 自動重建

kubectl get pods -n kubelite -w