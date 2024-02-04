# jupyterhub-on-nautilus

Sample JupyterHub config to run z2jh on [nautilus.optiputer.net](https://nautilus.optiputer.net/)

## Set up

### Create a namespace for yourself

1. Create a namespace using the Nautilus portal
2. Download `kubeconfig` file from the Nautilus portal

### Set up helm in your namespace

1. Download and install `helm` locally:
   
   ```bash
   curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
   ```
   
   You can use [other installation methods](https://github.com/kubernetes/helm/blob/master/docs/install.md)
   if curling into bash bothers you.

Congratulations, you now have a working `helm` on nautilus!

### Install JupyterHub
   
More information on configuring JupyterHub with z2jh can be found at https://z2jh.jupyter.org/

This repo contains a minimal JupyterHub with the following properties:

1. No pre-pulling of user images for faster startup
2. 1Gi of persistent storage per user
3. Ingress into the hub so users can use it

It is set up using a deployment chart, to make it easy to customize it with additional
helm charts.

1. Add the Jupyterhub helm repository.

   ```bash
   helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
   helm repo update
   ```

2. Fetch the version of JupyterHub chart mentioned in `requirements.yaml`.

   ```bash
   cd commons-hub
   helm dep up
   cd ..
   ```

3. Create values.yaml from template and generate and add random bytes for proxy:

   ```bash
   cp commons-hub/values.yaml.template commons-hub/values.yaml
   ```

   ```bash
   openssl rand -hex 32
   ```
   
   Add output to `commons-hub/values.yaml`:
  
   ```bash
   jupyterhub:
     proxy:
       secretToken: "..."
   ```
4. Set up Authentication (CiLogon).
Directions for different [third-party OAuth2](https://zero-to-jupyterhub.readthedocs.io/en/stable/administrator/authentication.html#oauth2-based-authentication). We are going to use [CiLogon](https://z2jh.jupyter.org/en/stable/administrator/authentication.html#cilogon). Here is the link to [register](https://cilogon.org/oauth2/register).


5. Install the hub!

   ```bash
   helm upgrade --cleanup-on-fail --install commons-hub commons-hub --kube-context nautilus --namespace ndp --values commons-hub/values.yaml
   ```

   You will need to modify `commons-hub/values.yaml` to set the hostname
   to something other than the current default.

6. Wait for the pods to be ready, and enjoy your JupyterHub!

7. To stop everything:
   
   ```bash
   helm uninstall commons-hub --kube-context nautilus
   ```

8. Debuging:
   Generate yaml file :
   helm template --namespace=ndp commons-hub commons-hub >> templateWithValues.yaml