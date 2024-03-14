## Fastchat Kubernetes Deployment

Create pvc (not part of the kustomize):
```
kubectl create -f fastchat_worker_PVC.yaml
```

Deploy to test ns:
```
kubectl kustomize |  kubectl apply -f -
```

Deploy to staging ns:
```
kubectl kustomize staging |  kubectl apply -f -
```

Deploy to prod ns:
```
kubectl kustomize prod |  kubectl apply -f -
```

Output all manifest into one yaml file (for debugging):
```
kubectl kustomize  >> ndp-test-fastchat.yaml
```