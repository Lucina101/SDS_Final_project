# Application
This application is simple 
image.png

# 1. First Master Setup
- Connect first master to the same subnet with raspberry pis
## 1.1 Mysql Installation
```bash
    sudo apt update
    sudo apt install mysql
```
## 1.2 Database Creation (mysql script)
run "sudo mysql" and create database there
```
    CREATE DATABASE [YOUR_DATABASE_NAME];
    CREATE USER '[YOUR_USERNAME]'@'%' IDENTIFIED BY [YOUR_PASSWORD];
    GRANT ALL ON [YOUR_DATABASE_NAME].* TO '[YOUR_USERNAME]'@'%';
    FLUSH PRIVILEGES;
```
## 1.3 Mysql Config Modification
```bash
    sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf
    sudo systemctl restart mysql
```
## 1.4 Password and Token File Creation
```bash
    cd sds_final
    echo -e 'password' >> dbpass.txt
    echo -e 'secret' >> token.txt
```
## 1.5 master.sh Modifcation
- Change the ```master.sh``` file to as follow
```
    master_ip=192.168.0.108
    db_port=3306
    db_name=hololive
    db_users=holouser
```
## 1.6 Master 1 Starting
```bash
    chmod 775 master.sh
    ./master.sh
```

# 2. Master 2 Setup
- Connect Master 2 to the same subnet with raspberry pis
- Copy the master.sh file from the first step to the directory ```/sds_final```
```bash
    cd sds_final
    ./master.sh
```

# 3. Worker Setup
## 3.1 Install Raspberry Pi OS
## 3.2 Modify /etc/dhcpcd.conf File (with sudo nano)
- append the lines below to the end of the file
``` 
    interface eth0
    static ip_address = 192.168.0.xxx/24
    static_routers = 192.168.0.1
    static domain_name_servers = 8.8.8.8
```
- xxx is different for each raspberry pi, from 116 to 119
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

# 4.