# Architecture

## Core Pipeline

Developer push code  
↓  
GitHub Actions  
↓  
Build Docker image  
↓  
Push image to GitHub Container Registry  
↓  
k3d / k3s pulls image  
↓  
Kubernetes Deployment update  
↓  
Rolling Update  
↓  
Service available to users  

## Components

- Flask microservices
- Docker images
- GitHub Actions workflow
- GitHub Container Registry
- k3d / k3s Kubernetes cluster
- Kubernetes Deployment and Service