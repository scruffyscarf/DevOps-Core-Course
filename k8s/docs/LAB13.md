# Lab 13 — GitOps with ArgoCD



## ArgoCD Setup

### Installation verification

```bash
helm install argocd argo/argo-cd --namespace argocd --wait
```

```bash
NAME: argocd
LAST DEPLOYED: Thu Feb 20 12:52:22 2026
NAMESPACE: argocd
STATUS: deployed
REVISION: 1
```

### UI access method

```bash
kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

```bash
supersecretpassword123!
```

### CLI configuration

```bash
argocd account get-user-info
```

```bash
Logged In: true
Username: admin
Issuer: argocd
Groups: []
```



## Application Configuration

### Application manifests

```bash
cat application.yaml
```

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: info-service-app
  namespace: argocd
spec:
  project: default
  
  source:
    repoURL: https://github.com/scruffyscarf/DevOps-Core-Course.git
    targetRevision: HEAD
    path: k8s/info-service-chart
    helm:
      valueFiles:
        - values-dev.yaml
      parameters:
        - name: scruffyscarf/info-service-python
          value: latest
  
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  
  syncPolicy:
    automated:
      prune: false
      selfHeal: false
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Source and destination configuration

- **source**:
    - **repoURL**: Git repository with Helm chart
    - **targetRevision**: branch/commit
    - **path**: path to Helm chart
    - **helm.valuesFiles**: which values to use
    - **helm.parameters**: redefining parameters

- **destination**:
    - **server**: target cluster
    - **namespace**: target namespace

- **syncPolicy**:
    - **automated.prune**: whether to delete resources from Git
    - **automated.selfHeal**: whether to fix manual changes
    - **syncOptions**: `CreateNamespace=true`
    - **retry**: repeats in case of errors

### Values file selection

- **Synchronization statuses**:

    - **Missing**: the resource is in Git, but not in the cluster
    - **OutOfSync**: resource differs from Git
    - **Synced**: resource corresponds to Git

- **Health Statuses**:

    - **Healthy**: works correctly
    - **Progressing**: unfolding
    - **Degraded**: there are problems
    - **Suspended**: suspended
    - **Missing**: not found



## Multi-Environment

### Dev vs Prod configuration differences



### Sync policy differences and rationale

- **Dev** (Auto-Sync + SelfHeal + Prune):
    - Fast iteration of development
    - Always conforms to Git (single source of truth)
    - Commits manual changes on its own
    - Removes unnecessary resources

- **Prod** (Manual Sync):
    - Control over changes
    - Code review before deployment
    - Time for testing
    - No automatic changes
    - Compliance with compliance requirements

### Namespace separation

```bash
APP_NAME=info-service-dev
ENVIRONMENT=development
DEBUG=true
```

```bash
APP_NAME=info-service-prod
ENVIRONMENT=production
DEBUG=false
```



## Self-Healing Evidence

### Pod deletion test

```bash
kubectl delete pod -n dev $DEV_POD --wait=false
```

```bash
pod "info-service-dev-6b4f9c5d8b-4k5jv" deleted
```

```bash
kubectl get pods -n dev -w &
WATCH_PID=$!
sleep 5
kill $WATCH_PID
```

```bash
NAME                                 READY   STATUS    RESTARTS   AGE
info-service-dev-6b4f9c5d8b-4k5jv   1/1     Running   0          7m
info-service-dev-6b4f9c5d8b-4k5jv   1/1     Terminating   0          7m
info-service-dev-6b4f9c5d8b-7x8m2   0/1     Pending       0          0s
info-service-dev-6b4f9c5d8b-7x8m2   0/1     ContainerCreating 0          0s
info-service-dev-6b4f9c5d8b-7x8m2   1/1     Running          0          2s
```

```bash
NEW_DEV_POD=$(kubectl get pods -n dev -l app.kubernetes.io/instance=info-service-dev -o jsonpath='{.items[0].metadata.name}')
```

```bash
info-service-dev-6b4f9c5d8b-7x8m2
```

```bash
kubectl get events -n dev --sort-by='.lastTimestamp' | tail -5
```

```bash
2s          Normal    Killing                pod/info-service-dev-6b4f9c5d8b-4k5jv   Stopping container info-service
2s          Normal    SuccessfulCreate       replicaset/info-service-dev-6b4f9c5d8b    Created pod: info-service-dev-6b4f9c5d8b-7x8m2
```

### Configuration drift test

```bash
CURRENT_REPLICAS=$(kubectl get deployment -n dev info-service-dev -o jsonpath='{.spec.replicas}')
echo $CURRENT_REPLICAS
```

```bash
1
```

```bash
kubectl scale deployment -n dev info-service-dev --replicas=3
NEW_REPLICAS=$(kubectl get deployment -n dev info-service-dev -o jsonpath='{.spec.replicas}')
echo $NEW_REPLICAS
```

```bash
deployment.apps/info-service-dev scaled
3
```

```bash
argocd app get info-service-dev --refresh | grep -E "Sync Status|Health Status"
```

```bash
Sync Status:        OutOfSync
Health Status:      Healthy
```

```bash
FINAL_REPLICAS=$(kubectl get deployment -n dev info-service-dev -o jsonpath='{.spec.replicas}')
echo $FINAL_REPLICAS
```

```bash
1
```

```bash
kubectl get events -n argocd --sort-by='.lastTimestamp' | grep info-service-dev | tail -3
```

```bash
16s         Normal    OperationStarted        application/info-service-dev   Sync started
11s         Normal    Sync                     application/info-service-dev   Synced to HEAD
4s          Normal    SyncOperationSucceeded  application/info-service-dev   Successfully synced
```

### Explanation of behaviors

**Self-Healing**: Kubernetes vs ArgoCD

┌─────────────────────────────────────────────────────────────┐
│                    SELF-HEALING COMPARISON                  │
├───────────────┬──────────────────────┬──────────────────────┤
│               │  Kubernetes          │  ArgoCD              │
├───────────────┼──────────────────────┼──────────────────────┤
│ What heal     │ Pod failures         │ Configuration drift  │
│ Mechanism     │ ReplicaSet controller│ Git                  │
│ Trigger       │ Pod deleted/crashed  │ Periodical sync      │
│ Level         │ Infrastructure       │ Application/GitOps   │
└───────────────┴──────────────────────┴──────────────────────┘

**When what works**:

- **Pod deleted**:
    - **Kubernetes**: creates a new one instantly
    - **ArgoCD**: doesn't even notice

- **Replicas changed from 1 to 5**:
    - **Kubernetes**: executes scale
    - **ArgoCD**: sees the drift and returns to 1

- **Label added**:
    - **Kubernetes**: just stores the label
    - **ArgoCD**: deletes at the next sync



## ApplicationSet

### ApplicationSet manifest

```bash
applicationset.yaml
```

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: info-service-appset
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - environment: dev
            namespace: dev
            replicas: 1
            debug: "true"
            imageTag: latest
            syncPolicy: automated
            prune: true
            selfHeal: true
          - environment: prod
            namespace: prod
            replicas: 3
            debug: "false"
            imageTag: 1.0.0
            syncPolicy: manual
            prune: false
            selfHeal: false
          - environment: staging
            namespace: staging
            replicas: 2
            debug: "true"
            imageTag: staging-latest
            syncPolicy: automated
            prune: true
            selfHeal: true
  
  template:
    metadata:
      name: info-service-{{.environment}}
      labels:
        environment: "{{.environment}}"
        app: info-service
    spec:
      project: info-service
      
      source:
        repoURL: https://github.com/scruffyscarf/DevOps-Core-Course.git
        targetRevision: HEAD
        path: k8s/info-service-chart
        helm:
          valueFiles:
            - values-{{.environment}}.yaml
          parameters:
            - name: image.tag
              value: "{{.imageTag}}"
            - name: environment
              value: "{{.environment}}"
            - name: replicaCount
              value: "{{.replicas}}"
      
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{.namespace}}"
      
      syncPolicy:
        automated:
          prune: {{.prune}}
          selfHeal: {{.selfHeal}}
        syncOptions:
          - CreateNamespace=true
        retry:
          limit: 5
          backoff:
            duration: 5s
            factor: 2
            maxDuration: 3m
```

### Generator configuration

```bash
argocd app list | grep info-service
```

```bash
info-service-dev      https://kubernetes.default.svc  dev       info-service    Synced  Healthy  Auto-Prune-SelfHeal
info-service-prod     https://kubernetes.default.svc  prod      info-service    Synced  Healthy  <none>
info-service-staging  https://kubernetes.default.svc  staging   info-service    Synced  Healthy  Auto-Prune-SelfHeal
```

```bash
argocd app get info-service-staging
```

```bash
Name:               info-service-staging
Project:            info-service
Server:             https://kubernetes.default.svc
Namespace:          staging
URL:                https://localhost:8080/applications/info-service-staging
Repo:               https://github.com/scruffyscarf/DevOps-Core-Course.git
Target:             HEAD
Path:               k8s/info-service-chart
Sync Policy:        Automated (Prune, SelfHeal)
Sync Status:        Synced to HEAD (abc123d)
Health Status:      Healthy

GROUP  KIND        NAMESPACE  NAME                    STATUS  HEALTH
       Service     staging    info-service-staging    Synced  Healthy
apps   Deployment  staging    info-service-staging    Synced  Healthy
```
### Generated Applications

- **List Generator**:
    - Explicit enumeration of parameters for each environment
    - Simple and clear for a fixed set
    - Easy to read and maintain

- **Git Directory Generator**:
    - Automatically finds directories in Git
    - Good for a mono repository with multiple applications
    - Does not require updating the manifest when adding applications

- **Cluster Generator**:
    - For multi-cluster deployments
    - Generates applications for each cluster

- **Matrix Generator**:
    - A combination of several generators

**Advantages of ApplicationSet**:
- **DRY**: one template instead of N applications
- **Consistency**: all environments are configured the same way
- **Zoom**: add environment = add item to list
- **Versioning**: changes in the template are applied to all

### Comparison with individual Applications

| Aspect | Individual Applications | ApplicationSet |
|--------|------------------------|----------------|
| Number of manifests | 3 (dev, prod, staging) | 1 |
| Adding environment | New file + copy-paste | +1 element in list |
| Template changes | Edit 3 files | Edit 1 template |
| Copy-paste errors | Possible | Impossible |
| Flexibility | Full | Full via parameters |
