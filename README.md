**Desafio5**

1. **Codigo Python API com variavel de ambiente (app.py):**

``````
from flask import Flask, redirect, render_template, request, url_for, jsonify
import mysql.connector, os
from mysql.connector import Error
from flaskext.mysql import MySQL
import redis, boto3

app = Flask(__name__) #Executando (__name__) para exibir somente as variaveis
@app.route('/healthcheck') #Executando (./healthcheck) para exibir o 0.0.0.0:5000/healthcheck
def healthcheck():
    api = versaoAPI()
    sts = status()
    mysql = conexaodb()
    nosql = NOSQL()
    fila = FILA()
    return jsonify(api, sts, mysql, nosql, fila)

def versaoAPI():
    versao = 'API: 1.0'
    return (versao)

def status():
    statusDeAcesso = 'Status 200'
    return(statusDeAcesso)
    
def conexaodb():
    conn = None
    try:
        conn = mysql.connector.connect(host=os.getenv('banco'),
           user=os.getenv('user'),
           password=os.getenv('password'),
           db=os.getenv('db')
         )
        if conn.is_connected():
            return ('Mysql OK')
    except:
        return ('Mysql: ERRO')

def FILA():
    conn =  None
    try:
        conectfila = boto3.client('sqs', aws_access_key_id=os.getenv('access'),aws_secret_access_key=os.getenv('secret'), region_name=os.getenv('region')) 
        geturl = conectfila.get_queue_url(QueueName=os.getenv('fila'))
        return('Fila: OK')
    except: 
        return('Fila: ERRO')


def NOSQL():
    conn =  None
    try:
        conn = redis.StrictRedis(host=os.getenv('nosql'), port=6379, password='') 
        if conn.ping() == True:
            return ('Nosql: Ok') 
    except: 
        return('Nosql: ERRO')


if __name__ == '__main__':
        app.run(host='0.0.0.0', port='5000', debug=True)

``````

**Dockerfile:**

``````
FROM python:2
COPY . /app
RUN pip install flask && pip install mysql-connector-python && pip install redis && pip install flask-redis && pip install flask-mysql && pip install boto3
WORKDIR /app
CMD python app.py
EXPOSE 5000

``````



2. **Instalando o Kubernetes e executando imagem Docker**


**Executar o Comando para sudo:**
``````
sudo su
``````
**Instalado Docker:**

	sudo apt-get install \apt-transport-https \ca-certificates \curl \gnupg-agent \software-properties-common

	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -+
	
	apt-key fingerprint 0EBFCD88

	sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu \$(lsb_release -cs) \stable"

	apt-get update

	apt-get install docker.io


**Comando para acessar Dockerhub:**

	Docker login

**Comando para criar conteiner com base no Dockerfile:**

	docker build .

***Return***
``````
Sending build context to Docker daemon  13.82kB
Step 1/6 : FROM python:2
 ---> 68e7be49c28c
Step 2/6 : COPY . /app
 ---> c62363640ff9
Step 3/6 : RUN pip install flask && pip install mysql-connector-python && pip install redis && pip install flask-redis && pip install flask-mysql && pip install boto3
 ---> Running in 9837394f067e .......
``````
**Comando para ver os conteiners:**

	docker images

***Return***
``````
REPOSITORY                        TAG                 IMAGE ID            CREATED             SIZE
<none>                            <none>              b947f07f186d        28 seconds ago      1.05GB
``````
**Comando para renomear os conteiners:**

	docker tag b947f07f186d  cristianofeliciano/desafio5teste:latest

**Comando para ver os conteiners:**

	docker images

***Return***
``````
REPOSITORY                         TAG                 IMAGE ID            CREATED             SIZE
cristianofeliciano/desafio5teste   latest              b947f07f186d        8 minutes ago       1.05GB
``````

**Comando para ativar aplicação e verificar se está funcionando:**

	docker run -it -p 5000:5000 -e access=***** -e secret=***** cristianofeliciano/desafio5teste

***Return***
``````
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 221-771-569
 ``````
 
***Return no navegador***

``````	
0	"API: 1.0"
1	"Status 200"
2	"Mysql ERRO"
3	"Nosql: ERRO"
4	"Fila: ERRO"
``````
*Obs: ERRO será apresentado pois as variaveis de ambiente estará no servidor cloud kubernetes*-

**Comando para subir imagem Docker Hub:**

	docker push cristianofeliciano/desafio5teste

***Return***
``````
he push refers to repository [docker.io/cristianofeliciano/desafio5teste]
e4b6854cc8c0: Pushed 
493ba80cd0e7: Pushed 
bbb86040b5df: Pushed 
e571d2d3c73c: Mounted from cristianofeliciano/crisdesafio5 
da7b0a80a4f2: Mounted from cristianofeliciano/crisdesafio5 
ceee8816bb96: Mounted from cristianofeliciano/crisdesafio5 
47458fb45d99: Mounted from cristianofeliciano/crisdesafio5 
46829331b1e4: Mounted from cristianofeliciano/crisdesafio5 
d35c5bda4793: Mounted from cristianofeliciano/crisdesafio5 
a3c1026c6bcc: Mounted from cristianofeliciano/crisdesafio5 
f1d420c2af1a: Mounted from cristianofeliciano/crisdesafio5 
461719022993: Mounted from cristianofeliciano/crisdesafio5 
latest: digest: sha256:0da749ee999685b9b156a4002f653a4cc519bce3a9945b1725b82e47f4b925b1 size: 2852
``````

3. **PARTINDO PARA SERVIDOR VIRTUAL KUBERNETES**

**Executar o Comando para sudo:**
``````
sudo su
``````
**Instalado Docker:**

	sudo apt-get install \apt-transport-https \ca-certificates \curl \gnupg-agent \software-properties-common

	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -+
	
	apt-key fingerprint 0EBFCD88

	sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu \$(lsb_release -cs) \stable"

	apt-get update

	apt-get install docker.io


**Comando para acessar Dockerhub:**

	Docker login


**Comando para Baixar imagem Docker Hub:**

	docker pull cristianofeliciano/desafio5teste


**Comando para verificar se baixou a imagem:**

	Docker images

***Return***

``````	
REPOSITORY                                TAG                 IMAGE ID            CREATED             SIZE
cristianofeliciano/desafio5teste          latest              b947f07f186d        3 hours ago         1.05GB
``````

**Instalar Kubectl Comandos:**
``````
sudo apt-get update && sudo apt-get install -y apt-transport-https gnupg2

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update

sudo apt-get install -y kubectl

chmod +x ./kubectl

sudo mv ./kubectl /usr/local/bin/kubectl

kubectl version --client
``````
**Instalando Minikube:**

	curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

	chmod +x minikube

	sudo mkdir -p /usr/local/bin/

	sudo install minikube /usr/local/bin/

**Confirmar instalação:**

	minikube start –driver=<driver_name>

	minikube status

***Return;***
``````
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
``````

**Inicializando MiniKube:**

	minikube start

***Return;***
``````
😄  minikube v1.12.1 on Ubuntu 18.04 (vbox/amd64)
✨  Using the none driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🔄  Restarting existing none bare metal machine for "minikube" ...
ℹ️  OS release is Ubuntu 18.04.4 LTS
🐳  Preparing Kubernetes v1.18.3 on Docker 19.03.6 ...
kubelet.resolv-conf=/run/systemd/resolve/resolv.conf
🤹  Configuring local host environment ...

❗  The 'none' driver is designed for experts who need to integrate with an existing VM
💡  Most users should use the newer 'docker' driver instead, which does not require root!
📘  For more information, see: https://minikube.sigs.k8s.io/docs/reference/drivers/none/

❗  kubectl and minikube configuration will be stored in /root
❗  To use kubectl or minikube commands as your own user, you may need to relocate them. For example, to overwrite your own settings, run:


sudo mv /root/.kube /root/.minikube $HOME
sudo chown -R $USER $HOME/.kube $HOME/.minikube

💡  This can also be done automatically by setting the env var CHANGE_MINIKUBE_NONE_USER=true
🔎  Verifying Kubernetes components...
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube"

NAME              STATUS   ROLES    AGE   VERSION
cris-virtualbox   Ready    master   22h   v1.18.3
``````

**Comando para iniciar imagem no Minikube:**

	kubectl run desafio5 --image=cristianofeliciano/desafio5teste

***Return;***
``````
pod/desafio5 created
``````
**Comando para verificar Pods:**

	kubectl get pods

***Return;***
``````
NAME       READY   STATUS    RESTARTS   AGE
desafio5   1/1     Running   0          29s
``````

**Comando para expor porta 5000:**

	kubectl expose pod desafio5 –port=5000

***Return;***
``````
service/desafio5 exposed
``````

**Comando para saber qual IP configurado:**

	kubectl describe pod desafio5

**Return;**
``````
Name:         desafio5
Namespace:    default
Priority:     0
Node:         cris-virtualbox/10.0.2.15
Start Time:   Fri, 31 Jul 2020 11:30:08 -0300
Labels:       run=desafio5
Annotations:  <none>
Status:       Running
IP:           172.17.0.3
IPs:
IP:  172.17.0.3
Containers:
desafio5:
Container ID:   docker://3c896dd87750a6dc680f83dacfc4423d1e53f595ee6dfff6396166903f3bd348
Image:          cristianofeliciano/crisdesafio5
Image ID:       docker-pullable://cristianofeliciano/crisdesafio5@sha256:57022d4f997fe6516140d671f732f95d76cf71101f15b3c77b4aa754d1621d70
Port:           <none>
Host Port:      <none>
State:          Running
Started:      Fri, 31 Jul 2020 11:30:13 -0300
Ready:          True
Restart Count:  0
Environment:    <none>
Mounts:
/var/run/secrets/kubernetes.io/serviceaccount from default-token-zbxjv (ro)
Conditions:
Type              Status
Initialized       True 
Ready             True 
ContainersReady   True 
PodScheduled      True 
Volumes:
default-token-zbxjv:
Type:        Secret (a volume populated by a Secret)
SecretName:  default-token-zbxjv
Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
node.kubernetes.io/unreachable:NoExecute for 300s
Events:
Type    Reason     Age        From                      Message
Normal  Scheduled  <unknown>  default-scheduler         Successfully assigned default/desafio5 to cris-virtualbox
Normal  Pulling    2m24s      kubelet, cris-virtualbox  Pulling image "cristianofeliciano/crisdesafio5"
Normal  Pulled     2m20s      kubelet, cris-virtualbox  Successfully pulled image "cristianofeliciano/crisdesafio5"
Normal  Created    2m20s      kubelet, cris-virtualbox  Created container desafio5
Normal  Started    2m20s      kubelet, cris-virtualbox  Started container desafio5

``````
**Comando para criar as credenciais das variáveis arquivo:**

	kubectl create secret generic senha --from-literal=banco=(ip do banco) --from-literal=user=(usuário) --from-literal=password=(senha) --from-literal=db=(nome do banco) --from-literal=access=(access aws) --from-literal=secret=(secret aws) --from-literal=region=us-east-1 --from-literal=fila=(nome da fila) --from-literal=nosql=(ip do redis)

**Comando para verificar se secrets foi criada:**

	kubectl get secrets

***Return***
``````
NAME                  TYPE                                  DATA   AGE
default-token-228xn   kubernetes.io/service-account-token   3      27h
senha                 Opaque
``````


**Comando para configurar arquivo yaml:**

	kubectl describe pod desafio5

***Return***
``````
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2020-08-05T17:47:21Z"
  labels:
    run: desafio5
  managedFields:
  - apiVersion: v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:labels:
          .: {}
          f:run: {}
      f:spec:
        f:containers:
          k:{"name":"desafio5"}:
            .: {}
            f:image: {}
            f:imagePullPolicy: {}
            f:name: {}
            f:resources: {}
            f:terminationMessagePath: {}
            f:terminationMessagePolicy: {}
        f:dnsPolicy: {}
        f:enableServiceLinks: {}
        f:restartPolicy: {}
        f:schedulerName: {}
        f:securityContext: {}
        f:terminationGracePeriodSeconds: {}
    manager: kubectl
    operation: Update
    time: "2020-08-05T17:47:21Z"
  - apiVersion: v1
    fieldsType: FieldsV1
    fieldsV1:
      f:status:
        f:conditions:
          k:{"type":"ContainersReady"}:
            .: {}
            f:lastProbeTime: {}
            f:lastTransitionTime: {}
            f:status: {}
            f:type: {}
          k:{"type":"Initialized"}:
            .: {}
            f:lastProbeTime: {}
            f:lastTransitionTime: {}
            f:status: {}
            f:type: {}
          k:{"type":"Ready"}:
            .: {}
            f:lastProbeTime: {}
            f:lastTransitionTime: {}
            f:status: {}
            f:type: {}
        f:containerStatuses: {}
        f:hostIP: {}
        f:phase: {}
        f:podIP: {}
        f:podIPs:
          .: {}
          k:{"ip":"172.17.0.3"}:
            .: {}
            f:ip: {}
        f:startTime: {}
    manager: kubelet
    operation: Update
    time: "2020-08-05T17:47:25Z"
  name: desafio5
  namespace: default
  resourceVersion: "14397"
  selfLink: /api/v1/namespaces/default/pods/desafio5
  uid: 0aa9b5c9-545f-4371-8316-89f98ab4e275
spec:
  containers:
  - image: cristianofeliciano/desafio5teste
    imagePullPolicy: Always
    name: desafio5
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
 name: default-token-228xn
 readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: cris-virtualbox
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: default
  serviceAccountName: default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - name: default-token-228xn
    secret:
      defaultMode: 420
      secretName: default-token-228xn
status:
  conditions:
  - lastProbeTime: null
    lastTransitionTime: "2020-08-05T17:47:21Z"
    status: "True"
    type: Initialized
  - lastProbeTime: null
    lastTransitionTime: "2020-08-05T17:47:25Z"
    status: "True"
    type: Ready
  - lastProbeTime: null
    lastTransitionTime: "2020-08-05T17:47:25Z"
    status: "True"
    type: ContainersReady
  - lastProbeTime: null
    lastTransitionTime: "2020-08-05T17:47:21Z"
    status: "True"
    type: PodScheduled
  containerStatuses:
  - containerID: docker://32043a5a36fbe467c48ef360c33cc8ceef74113af4c42c7f39eb593817adf6d5
    image: cristianofeliciano/desafio5teste:latest
    imageID: docker-pullable://cristianofeliciano/desafio5teste@sha256:0da749ee999685b9b156a4002f653a4cc519bce3a9945b1725b82e47f4b925b1
    lastState: {}
    name: desafio5
    ready: true
    restartCount: 0
    started: true
    state:
      running:
        startedAt: "2020-08-05T17:47:25Z"
  hostIP: 10.0.2.15
  phase: Running
  podIP: 172.17.0.3
  podIPs:
  - ip: 172.17.0.3
  qosClass: BestEffort
  startTime: "2020-08-05T17:47:21Z"

``````

**Configurar o arquivo.yaml para configuração do pod com as variaveis de ambiente:**
``````
*Colocar o deployment abaixo;*

    env:
      - name: banco
        valueFrom:
          secretKeyRef:
            name: senha
            key: banco
      - name: user
        valueFrom:
          secretKeyRef:
            name: senha
            key: user
      - name: password
        valueFrom:
          secretKeyRef:
            name: senha
            key: password
      - name: db
        valueFrom:
          secretKeyRef:
            name: senha
            key: db
      - name: access
        valueFrom:
          secretKeyRef:
            name: senha
            key: access
      - name: secret
        valueFrom:
          secretKeyRef:
            name: senha
            key: secret
      - name: region
        valueFrom:
          secretKeyRef:
            name: senha
            key: region
      - name: fila
        valueFrom:
          secretKeyRef:
            name: senha
            key: fila
      - name: nosql
        valueFrom:
          secretKeyRef:
            name: senha
            key: nosql
``````
**Após colocar esse é o resultado:**

**Return**
``````
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2020-08-05T17:47:21Z"
  labels:
    run: desafio5
  managedFields:
  - apiVersion: v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:labels:
          .: {}
          f:run: {}
      f:spec:
        f:containers:
          k:{"name":"desafio5"}:
            .: {}
            f:image: {}
            f:imagePullPolicy: {}
            f:name: {}
            f:resources: {}
            f:terminationMessagePath: {}
            f:terminationMessagePolicy: {}
        f:dnsPolicy: {}
        f:enableServiceLinks: {}
        f:restartPolicy: {}
        f:schedulerName: {}
        f:securityContext: {}
        f:terminationGracePeriodSeconds: {}
    manager: kubectl
    operation: Update
    time: "2020-08-05T17:47:21Z"
  - apiVersion: v1
    fieldsType: FieldsV1
    fieldsV1:
      f:status:
        f:conditions:
          k:{"type":"ContainersReady"}:
            .: {}
            f:lastProbeTime: {}
            f:lastTransitionTime: {}
            f:status: {}
            f:type: {}
          k:{"type":"Initialized"}:
            .: {}
            f:lastProbeTime: {}
            f:lastTransitionTime: {}
            f:status: {}
            f:type: {}
          k:{"type":"Ready"}:
            .: {}
            f:lastProbeTime: {}
            f:lastTransitionTime: {}
            f:status: {}
            f:type: {}
        f:containerStatuses: {}
        f:hostIP: {}
        f:phase: {}
        f:podIP: {}
        f:podIPs:
          .: {}
          k:{"ip":"172.17.0.3"}:
            .: {}
            f:ip: {}
        f:startTime: {}
    manager: kubelet
    operation: Update
    time: "2020-08-05T17:47:25Z"
  name: desafio5
  namespace: default
spec:
  containers:
  - image: cristianofeliciano/desafio5teste
    imagePullPolicy: Always
    name: desafio5
    env:
      - name: banco
        valueFrom:
          secretKeyRef:
            name: senha
            key: banco
      - name: user
        valueFrom:
          secretKeyRef:
            name: senha
            key: user
      - name: password
        valueFrom:
          secretKeyRef:
            name: senha
            key: password
      - name: db
        valueFrom:
          secretKeyRef:
            name: senha
            key: db
      - name: access
        valueFrom:
          secretKeyRef:
            name: senha
            key: access
      - name: secret
        valueFrom:
          secretKeyRef:
            name: senha
            key: secret
      - name: region
        valueFrom:
          secretKeyRef:
            name: senha
            key: region
      - name: fila
        valueFrom:
          secretKeyRef:
            name: senha
            key: fila
      - name: nosql
        valueFrom:
          secretKeyRef:
            name: senha
            key: nosql
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-228xn
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: cris-virtualbox
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: default
  serviceAccountName: default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - name: default-token-228xn
    secret:
      defaultMode: 420
      secretName: default-token-228xn
status:
  conditions:
  - lastProbeTime: null
    lastTransitionTime: "2020-08-05T17:47:21Z"
    status: "True"
    type: Initialized
  - lastProbeTime: null
    lastTransitionTime: "2020-08-05T17:47:25Z"
    status: "True"
    type: Ready
  - lastProbeTime: null
    lastTransitionTime: "2020-08-05T17:47:25Z"
    status: "True"
    type: ContainersReady
  - lastProbeTime: null
    lastTransitionTime: "2020-08-05T17:47:21Z"
    status: "True"
    type: PodScheduled
  containerStatuses:
  - containerID: docker://32043a5a36fbe467c48ef360c33cc8ceef74113af4c42c7f39eb593817adf6d5
    image: cristianofeliciano/desafio5teste:latest
    imageID: docker-pullable://cristianofeliciano/desafio5teste@sha256:0da749ee999685b9b156a4002f653a4cc519bce3a9945b1725b82e47f4b925b1
    lastState: {}
    name: desafio5
    ready: true
    restartCount: 0
    started: true
    state:
      running:
        startedAt: "2020-08-05T17:47:25Z"
  hostIP: 10.0.2.15
  phase: Running
  podIP: 172.17.0.3
  podIPs:
  - ip: 172.17.0.3
  qosClass: BestEffort
  startTime: "2020-08-05T17:47:21Z"
``````

*Obs: após fazer esse procedimento salvar o aquivo como configuracao.yaml*

**Comando deletar pod anterior :**
``````
kubectl delete pod desafio5
``````
***Return***
``````
pod "desafio5" deleted
``````

**Comando para subir nova pod com a configuração correta :**
``````
kubectl apply -f configuracao.yaml
``````
***Return***
``````
pod/desafio5 created
``````

**Comando para verificar a pod criada :**
``````
kubectl get pods
``````
***Return***
``````
NAME       READY   STATUS    RESTARTS   AGE
desafio5   1/1     Running   0          13s
``````


**Pronto, para acessar sua API:**

*172.17.0.3:5000/healthcheck*

***Return***
``````
0	"API: 1.0"
1	"Status 200"
2	"Mysql OK"
3	"Nosql: Ok"
4	"Fila: OK"

``````

****EXTRAS:****

**Comando para editar pod :**
``````
kubectl edit pod desafio5
``````

**Comando para entrar na pod :**
``````
kubectl exec -it desafio5 bash
``````
***Return***
``````
root@desafio5:/app#

root@desafio5:/app# ls
Dockerfile  app.py  conexaodb.py  conexaodb.pyc  healthcheck.pyc  requirements.txt  worker.py  worker.pyc
root@desafio5:/app# 

``````
**Comando para verificar se a secret está dentro da pod :**

*Acessar pod*

``````
kubectl exec -it desafio5 bash
``````

*Dentro da pod executar comando*

``````
env
``````
***Return***

``````
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_SERVICE_PORT=443
HOSTNAME=desafio5
PYTHON_VERSION=2.7.18
PWD=/app
HOME=/root
LANG=C.UTF-8
KUBERNETES_PORT_443_TCP=tcp://**xxxxx**
DESAFIO5_SERVICE_PORT=5000
GPG_KEY=**xxxxx**
DESAFIO5_SERVICE_HOST=**xxxxx**
DESAFIO5_PORT=**xxxxx**
secret=**xxxxx**
DESAFIO5_PORT_5000_TCP_PORT=5000
TERM=xterm
PYTHONIOENCODING=UTF-8
SHLVL=1
KUBERNETES_PORT_443_TCP_PROTO=tcp
PYTHON_PIP_VERSION=20.0.2
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
PYTHON_GET_PIP_SHA256=**xxxxx**
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_PORT=**xxxxx**
KUBERNETES_PORT_443_TCP_PORT=443
PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/d59197a3c169cef378a22428a3fa99d33e080a5d/get-pip.py
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
DESAFIO5_PORT_5000_TCP=tcp:**xxxxx**
access=**xxxxx**
DESAFIO5_PORT_5000_TCP_ADDR=10.98.91.85
DESAFIO5_PORT_5000_TCP_PROTO=tcp
``````
*Todos "xxxxx" são informações confidenciais*



**Referencias**

Kubernetes - https://kubernetes.io/docs/concepts/

Kubertips ─ https://github.com/elisboa/kubertips - Connect to preview  ─ contribua!

minikube - https://kubernetes.io/docs/tasks/tools/install-minikube/

kind - https://kind.sigs.k8s.io/

microk8s - https://microk8s.io/

Descomplicando o Kubernetes - https://github.com/badtuxx/DescomplicandoKubernetes - Connect to preview 

Medium - https://medium.com/xp-inc/principais-comandos-docker-f9b02e6944cd






