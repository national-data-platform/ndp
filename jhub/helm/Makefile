upgrade: template
	helm --tiller-namespace=suave upgrade --install --namespace=suave nautilus-hub nautilus-hub

restart: template
	helm del --purge --tiller-namespace=suave nautilus-hub
	sleep 10
	helm --tiller-namespace=suave upgrade --install --namespace=suave nautilus-hub nautilus-hub

template:
	cd nautilus-hub && \
	./gen_values.sh

buildrelease:
	cd tensorflow-notebook && \
	docker build -t gitlab-registry.nautilus.optiputer.net/crawld/jupyterlab/suave .

pushdocker:
	docker push gitlab-registry.nautilus.optiputer.net/crawld/jupyterlab/suave

inithelm:
	helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
	helm repo update
	helm init --client-only --service-account tiller --tiller-namespace=suave
