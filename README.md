# master 1 node setup
master 1 device will running k3s database.
## 1. setup database
- install database 
    ```bash
        sudo apt update
        sudo apt install mysql
    ```
- login to database
    ```bash
        sudo mysql
    ```
- create database and user. And modify privileges.
    - template
        ```
            CREATE DATABASE [YOUR_DATABASE_NAME];
            CREATE USER '[YOUR_DATABASE_USER]'@'%' IDENTIFIED BY '[YOUR_DATABASE_PASSWORD]';
            GRANT ALL ON [YOUR_DATABASE_NAME].* TO '[YOUR_DATABASE_USER]'@'%';
            FLUSH PRIVILEGES;
        ```
    - example
        ```
        CREATE DATABASE ym;
        CREATE USER 'ym_group'@'%' IDENTIFIED BY 'password';
        GRANT ALL ON ym.* TO 'ym_group'@'%';
        FLUSH PRIVILEGES;
        ```
- modify mysql configuration to allow external access.
    ```bash
        sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
        # and then change bind-address to 0.0.0.0
        # save and exit
    ```
- restart mysql server.
    ```
    sudo systemctl restart mysql
    ```
## 2.config k3s builder and run
- please make sure that master 1 connect to internet with the same subnet with raspberry pis already.
- change directory to **k3sbuild**.
- create ```dbpass.txt``` and fill database user's password which is set at step 1 with no line space or newlines.
- create ```token.txt ``` and fill your generated token with no line space or newlines.
- modify master.sh
    - config database name and user at master.sh .
    - change master ip to your master 1 private ip address.
    - for example
    ```bash
        master_ip=192.168.0.104
        db_port=3306
        db_name=ym_db
        db_users=ym_group
    ```
- change permission of ``` master.sh ``` to allow execution.
    - ```bash 
        chmod 775 master.sh
      ```
- use this command  to start worker.
    - ```
        ./master.sh start
      ```

    
# master 2 node setup
- please make sure that master 2 connect to internet with the same subnet with raspberry pis already.
- change directory to configured **k3sbuild** that modified at master 1 step 2.
- use this command  to start worker.
    - ```
        ./master.sh start
      ```

# worker node setup
 This section, we will configure 4 raspberry pi device followed by these instructions.
## 1. install raspberry pi os
- install raspberry-pi-os-64 by using rpi-imager to your micro sd card for each worker node.
## 2. config the static ipv4
- we will configure static ip4 address for each raspberry pi to ```192.168.0.148 -> 192.168.0.151``` respectively.
- append these code lines into ```/etc/dhcpcd.conf``` in each micro sd card's rootfs drive with **root privilege**.
```bash
  interface [YOUR_INTERFACE]
  static ip_address=[YOUR_IP]
  static_routers=[ROUTER_IP]
  static domain_name_servers=[DOMAINNAME_IP]
  ```
- for example
```
interface eth0
static ip_address=192.168.0.148/24
static_routers=192.168.0.1
static domain_name_servers=8.8.8.8
```
## 3. disable ipv6 ip-address
- append these code lines into ```/etc/sysctl.conf``` in each micro sd card's rootfs drive with **root privilege**.
```bash
net.ipv6.conf.all.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6=1
net.ipv6.conf.lo.disable_ipv6=1
net.ipv6.conf.eth0.disable_ipv6 = 1
```
- append these code lines into ```/etc/rc.local``` before "exit 0" in each micro sd card's rootfs drive with **root privilege**.
```bash
service procps reload
```

## 4. enable c-groups
- append this line into ```/boot/cmdline.txt``` in each micro sd card's rootfs drive with **root privilege**
```bash
cgroup_enable=memory cgroup_memory=1
```

## 5. test for each worker
- to ensure that each worker node are setting up correctly. you may use these command for example.
```bash
ssh pi@192.168.0.148 # 192.168.0.148 -> 151
```
```bash
curl --version # curl must be used in each worker node to start k3s agent
```
```bash
ifconfig # to ensure that each worker's ip is set correctly
```
## 6.start k3s worker
- you may use master1 computer to orchestrate this section.
- change directory to **k3sbuild** .
- create pipass.txt
    -  fill pipass.txt with your password that configured to rasberry-pi.
    -  master_ip at ``` slave.sh ``` to your master computer ip address.
- change permission of ``` slave.sh ``` to allow execution.
    - ```bash 
        chmod 775 slave.sh
      ```
- use this command  to start worker
    - ```
        ./slave.sh start
      ```
    
## 7.stop k3s worker(optional)
- if raspberry pi aren't working or starting up correctly, you may use this command to reset it.
    - ```bash
        ./slave.sh reset
      ```
# workloads setup