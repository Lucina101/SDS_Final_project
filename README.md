# Application
This application is simple service with 3 requests and 4 different containers

1 database service

3 backend services(adding value to database, find average of added values, find maximum of added values)

And a simple web client for request handling
The docker file and code for each service can be found under folder backend*/ and frontend/

# Kubernetes cluster setup
First of all, we have to setup kubernetes cluster. We will configure it with k3s
# 1. Master Node Setup
## 1.1 Install mysql with the following command
```bash
    sudo apt update
    sudo apt install mysql
```
## 1.2 Database Creation (mysql script)
Create database as datastore endpoint for k3s.
```
    CREATE DATABASE [YOUR_DATABASE_NAME];
    CREATE USER '[YOUR_USERNAME]'@'%' IDENTIFIED BY [YOUR_PASSWORD];
    GRANT ALL ON [YOUR_DATABASE_NAME].* TO '[YOUR_USERNAME]'@'%';
    FLUSH PRIVILEGES;
```
## 1.3 Mysql Config Modification
Change bind address to 0.0.0.0
```bash
    sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
    sudo systemctl restart mysql
```
## 1.4 First master creating cluster
Make sure you know these values, master ip address, database port, database name, database user, and database password

You can set cluster token as your choice.

Replace the first 6 lines below with your configuration and run the last command

You can directly run this in cli or save them as shell script and run
```bash
    master_ip=192.168.0.109
    db_port=3306
    db_name=hololive
    db_user=holouser
    token=SECRET
    db_password=password

    sudo curl -sfL https://get.k3s.io | sh -s - server   --token=$token --node-taint CriticalAddonsOnly=true:NoSchedule   --datastore-endpoint="mysql://$database_user:$database_password@tcp($master_ip:$database_port)/$database_name"
```



# 2. Second Master Node Setup
Make sure the second master is joining the same subnet.

Then, you can do the same as the first master in step 1.4

Note that token must be the same for all nodes in the cluster

Note: If anything is going wrong(for example, it took to long to join the cluster. The server is unresponsive) you can try running

```bash
    sudo service k3s stop
    sudo /usr/local/bin/k3s-killall.sh
```

This will reset the k3s setting for that node.

# 3. Worker Node Setup
## 3.1 Install Raspberry Pi OS
Make sure that you allowed ssh connection during installation

The step 3.2 onward will assume that you already ssh to pi.

The step below are independent for each pi.

## 3.2 Modify /etc/dhcpcd.conf File (with sudo nano)
- append the lines below to the end of the file
```
    interface eth0
    static ip_address=192.168.0.{pi_ipadd}/24
    static_routers=192.168.0.1
    static domain_name_servers=8.8.8.8
```
- {pi_ipadd} is different for each raspberry pi, from 116 to 119 (or number of your choice as long as they're in the router subnet)

## 3.3 Modify /etc/sysctl.conf File (with sudo nano)
- append the lines below to the end of the file
``` 
    net.ipv6.conf.all.disable_ipv6 = 1
    net.ipv6.conf.default.disable_ipv6 = 1
    net.ipv6.conf.lo.disable_ipv6 = 1
    net.ipv6.conf.eth0.disable_ipv6 = 1
```

## 3.4 Modify /etc/rc.local File (with sudo nano)
- append the line below before the line ```exit 0``` in the file
``` 
    service procps reload
```

## 3.5 Modify /boot/cmdline.txt File (with sudo nano)
- append the lines below to the end of the file
``` 
    cgroup_enable = memory
    cgroup_memory = 1
```

## 3.6 reboot the system with
``` 
    sudo reboot
```

## 3.7 Joining the cluster

You need to know the master ip address and by default cluster port is 6443.
So the master_port below is assumed to be 6443

Run these commands

```bash
    master_ip=192.168.0.109
    master_port=6443

    sudo curl -sfL https://get.k3s.io | K3S_URL=https://$master_ip:$master_port \
    K3S_TOKEN=$my_token sh -

    sudo systemctl enable --now k3s-agent
```

Note: If it took to long to start service or join the cluster, you might need to restart the service with
```
    sudo service k3s-agent restart
```

## 3.8 Further setup

Try running "kubectl get nodes" in pi, if errors occured, you probably need this further setup.

### 3.8.1 export kube config with
```
    export KUBECONFIG=~/.kube/config
```
### 3.8.2 Generate config file with

```
    mkdir ~/.kube 2> /dev/null
    sudo k3s kubectl config view --raw > "$KUBECONFIG"
    chmod 600 "$KUBECONFIG"
```
### 3.8.3 Replace config file content
From the first master, copy the content of /etc/rancher/k3s/k3s.yaml

The "server:" line from master should still be 127.0.0.1:6443

Change it to master_ip:6443

Replace ~/.kube/config with the copied content

Try running "kubectl get nodes" again, you should see the node in the cluster now.



# Deploy the application

After cloning this repository, we should be able to deploy by simply running

```
    sudo bash deploy.sh
```

For resoources cleanup, you can run

```
    sudo bash cleanup.sh
```