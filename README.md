# Application

![Web client image](/front.PNG)


This application is a simple service with 3 requests and 4 different containers

There are 1 database service, 3 backend services (adding value to the database, find average of all the added values, find maximum of all the added values) and a simple web client for request handling.

The docker file and code for each service can be found under folder `Backend*/` and `Frontend/`

# How to setup the Kubernetes cluster
First of all, we have to setup the Kubernetes cluster. We will configure it with k3s.
## 1. Setup the first Master Node 
### 1.1 Install mysql and curl
Run these following commands
```bash
    sudo apt update
    sudo apt install mysql-server
    sudo apt install curl
```
### 1.2 Create the Database
Login to mysql as root and create database as datastore endpoint for k3s.

Replace `DATABASE_*` with your database configuration.
```mysql
    CREATE DATABASE [DATABASE_NAME];
    CREATE USER '[DATABASE_USERNAME]'@'%' IDENTIFIED BY [DATABASE_PASSWORD];
    GRANT ALL ON [DATABASE_NAME].* TO '[DATABASE_USERNAME]'@'%';
    FLUSH PRIVILEGES;
```
### 1.3 Modify the MySql Config
Change the bind address in `/etc/mysql/mysql.conf.d/mysqld.cnf` to `0.0.0.0`

This can be done by either manually modify the file or use the command below.
```
sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
```
After that, restart mysql by running ```sudo systemctl restart mysql```.
### 1.4 Create the cluster
Make sure you know these values: master IP address, database port, database name, database user, and database password.

Set the cluster token as your choice.

Replace the first 6 lines below with your configuration and run the last command.

Either directly run this in cli or save it as shell script and run.
```bash
    master_ip=[MASTER_IP]
    db_port=[DATABASE_PORT]
    db_name=[DATABASE_NAME]
    db_user=[DATABASE_USERNAME]
    token=[TOKEN]
    db_password=[DATABASE_PASSWORD]

    sudo curl -sfL https://get.k3s.io | sh -s - server   --token=$token --node-taint CriticalAddonsOnly=true:NoSchedule   --datastore-endpoint="mysql://$db_user:$db_password@tcp($master_ip:$db_port)/$db_name"
```


## 2. Setup the second Master Node
Make sure the second master is joining the same subnet and have `curl` installed. 

Then, do the same as the first master node's step 1.4. 
The token must be **the same** for all nodes in the cluster.

*Note: If anything is going wrong, for example, it takes too long to join the cluster or the server is unresponsive, you can try running ```sudo service k3s stop``` and ```sudo /usr/local/bin/k3s-killall.sh``` to reset the k3s setting for that node.*

## 3. Setup the Worker Nodes
For each pi, do these following steps:
### 3.1 Install Raspberry Pi OS
Make sure to allow the SSH connection during the installation.

SSH into the Pi.

### 3.2 Setup the static IP address
For the convenience, set the static IP address by appending the lines below to the end of `/etc/dhcpcd.conf`. **You have to use `sudo` to modify the file.**
```
    interface eth0
    static ip_address=192.168.0.{pi_ipadd}/24
    static_routers=192.168.0.1
    static domain_name_servers=8.8.8.8
```
- `{pi_ipadd}` must be different for each raspberry Pi, varying from 116 to 119 (or any numbers of your choice as long as they're in the router subnet.)

### 3.3 Setup the Cgroup
Append the lines below to the end of `/boot/cmdline.txt`. **You have to use `sudo` to modify the file.**
``` 
    cgroup_enable = memory
    cgroup_memory = 1
```

### 3.4 Disable the IPV6
Append these lines at the end of `/etc/sysctl.conf`. **You have to use `sudo` to modify the file.**
``` 
    net.ipv6.conf.all.disable_ipv6 = 1
    net.ipv6.conf.default.disable_ipv6 = 1
    net.ipv6.conf.lo.disable_ipv6 = 1
    net.ipv6.conf.eth0.disable_ipv6 = 1
```

### 3.5 Reload Procps Service by default
Append `service procps reload` before the line `exit 0` in `/etc/rc.local`. **You have to use `sudo` to modify the file.** 

### 3.6 Reboot the system
```bash
    sudo reboot
```

### 3.7 Joining the cluster
Make sure `curl` is installed.

You need to know the master ip address and by default, the cluster port is 6443.
The master_port below is assumed to be 6443.

Run these commands;

```bash
    master_ip=192.168.0.109
    master_port=6443

    sudo curl -sfL https://get.k3s.io | K3S_URL=https://$master_ip:$master_port \
    K3S_TOKEN=$token sh -

    sudo systemctl enable --now k3s-agent
```

*Note: If it takes too long to start service or join the cluster, you might need to restart the service with ```sudo service k3s-agent restart```*


### 3.8 Additional setup

Try running `kubectl get nodes` in Pi, if any errors have occured, you probably need this additional setup.

#### 3.8.1 Export the kube config
```bash
    export KUBECONFIG=~/.kube/config
```
#### 3.8.2 Generate the config file
```bash
    mkdir ~/.kube 2> /dev/null
    sudo k3s kubectl config view --raw > "$KUBECONFIG"
    chmod 600 "$KUBECONFIG"
```
#### 3.8.3 Replace config file content

From the first master, copy the content of `/etc/rancher/k3s/k3s.yaml`

The `"server:"` line from master should still be `127.0.0.1:6443`
Change it to `{master_ip}:6443` (e.g `192.168.0.109:6443`)

Replace `~/.kube/config` with the copied content and restart k3s-agent service by running ```sudo service k3s-agent restart```.


Try running ```kubectl get nodes``` again, you should see the node in the cluster now.


## Deploy the application

After cloning this repository, we should be able to deploy by simply running

```bash
    sudo bash deploy.sh
```

You can open http://localhost in the second master browser and see the web client.

For resources cleanup, you can run ```sudo bash cleanup.sh```.

