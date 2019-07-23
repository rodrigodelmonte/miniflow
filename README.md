# Miniflow

This repository aims to help you have an [Airflow](https://airflow.apache.org/) installation running in Kubernetes [minikube](https://github.com/kubernetes/minikube).

## Setup

This example expects a running [kubernetes](https://kubernetes.io) environment with [helm](https://helm.sh) installed. To setup it fast and easily (non-production), the following commands can be used:

```bash
minikube start -p airflow
kubectl apply -f 01_rbac_helm.yaml
helm init
kubectl create namespace airflow
```

In this example, we're using [minikube](https://github.com/kubernetes/minikube). You can check Kubernetes [official docs](https://kubernetes.io/docs/tasks/tools/install-minikube/), for more details on how to install it.

## Setup kubernetes credentials

To have the [Airflow Kubernetes Operator](https://airflow.apache.org/kubernetes.html) working properly. The Operator expects the Kubernetes credentials in the path `~/.kube/config` by default. The following steps create the required Kubernetes credentials.

```bash
mkdir kubeconfig/ && cd kubeconfig/
cp ~/.minikube/client.* ~/.minikube/ca.crt .
kubectl config view --minify | cat > config
kubectl create secret generic kubeconfig --from-file=config --from-file=ca.crt --from-file=client.crt --from-file=client.key --namespace airflow
cd ..
rm -rf kubeconfig/
```

You don't need to change the following config, just to be aware of where it is been configured in the `values.yaml` file.

```yaml
  extraVolumeMounts:
    - name: kubeconfig
      mountPath: /usr/local/airflow/.kube/
  ## Additional volumeMounts to the main containers in the Scheduler, Worker and Web pods.
  # - name: synchronised-dags
  #   mountPath: /usr/local/airflow/dags
  extraVolumes:
    - name: kubeconfig
      secret:
        secretName: kubeconfig
```

## Install Airflow

In this example, we are using the official community [helm chart](https://github.com/helm/charts/tree/master/stable/airflow).

```bash
helm install --namespace "airflow" --name "airflow" stable/airflow -f values.yaml
```

## Setup a git dag repository - OPTIONAL

More details about how it works [here](https://github.com/helm/charts/tree/master/stable/airflow#use-init-container).

```bash
cp ~/.ssh/id_rsa ~/.ssh/id_rsa.pub .
grep github ~/.ssh/known_hosts > known_hosts
kubectl create secret generic my-git-secret --from-file=id_rsa --from-file=known_hosts --from-file=id_rsa.pub --namespace airflow
rm id_rsa id_rsa.pub known_hosts
```

Change the `values.yaml`

```yaml
  git:
    ##
    ## url to clone the git repository
    url: git@github.com:<MYREPO>/dags.git
    ##
    ## branch name, tag or sha1 to reset to
    ref: master
    ## pre-created secret with key, key.pub and known_hosts file for private repos
    secret: my-git-secret
  initContainer:
    ## Fetch the source code when the pods starts
    enabled: true
```

## Upgrade Helm configs

Every time you update your `values.yaml` run the following command to apply the changes.

```bash
helm upgrade airflow -f values.yaml stable/airflow --namespace airflow
```

## Kubernetes dashboard

```bash
minikube dashboard -p airflow
```

## Airflow dashboard

```bash
kubectl port-forward svc/airflow-web -n airflow 8080
```

In the browser try http://localhost:8080

## Clean

```bash
helm del --purge airflow
minikube delete -p airflow
```

## DISCLAIMER

* In this example we are not following production best practices. So, please review the helm configs [here](https://github.com/helm/charts/tree/master/stable/airflow) if you plan to run production workloads.
* This example uses the docker image `rodrigodelmonte/docker-airflow:1.10.1` which uses the `Dockerfile` from [puckel/docker-airflow](https://github.com/puckel/docker-airflow), There is no official docker image maintained by the Airflow community, the current one maintained by the community is being used for development only. Fell free to build your image and check the `docker/` folder or try [puckel/docker-airflow](https://github.com/puckel/docker-airflow).

## Contributing

* Fork it (<https://github.com/Onefootball/miniflow/fork>)
* Create your feature branch (git checkout -b feature/fooBar)
* Commit your changes (git commit -am 'Add some fooBar')
* Push to the branch (git push origin feature/fooBar)
* Create a new Pull Request
