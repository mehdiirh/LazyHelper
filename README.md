# 🦥 Lazy Helper !

### A simple interface to help lazy people like me to shut down/reboot/sleep/lock/etc. their computer remotely.

![img.png](images/img.png)

## - USAGE

#### If you're a lazy guy, like me. or a busy one, you may leave your PC on, when you're going to sleep, or going to watch a movie on TV.
#### There you are ! This is the solution you're looking for :)

#### Just install and run LazyHelper and after that you're able to shut down your linux PC with your mobile !

## - API

LazyHelper API is described [Here](api/README.md)

## - Installation

```shell
git clone https://github.com/mehdiirh/LazyHelper.git && cd LazyHelper
```

LazyHelper🦥 likes lazy people, so because you're too lazy to install step by step, it will install itself :)

You will be asked to create a superuser, please do it to use authentication system. 

Run:

```shell
sudo bash install.sh && source venv/bin/activate
```

Yay !

#### - To use "copy to clipboard" feature, you need to install [xclip](https://github.com/astrand/xclip)


### Now you can run your LazyHelper:
```shell
./manage.py runserver 0.0.0.0:8081  # <- you can change the port 
```
 Connect your phone and PC to same network and access it from your PC local ip address :

`192.168.*.*:<port>`

## - [Optional] Set host name 
```shell
sudo nano /etc/hosts
```

Add this line after `127.0.0.1    localhost`:
```shell
127.0.0.1    <your-host-name>  # like: mehdi
```

Execute this command:
```shell
hostnamectl set-hostname <your-host-name>
```

Reboot!

Now you can access your PC from your-host-name.local ( like: mehdi.local) from any device on your network

## - Daemonize 
```shell
sudo nano /etc/systemd/system/LazyHelper.service
```

 **Edit** this service based on your configs, then hit Ctrl+X and Enter to save
```shell
[Unit]
Description=LazyHelper
After=network.target

[Service]
WorkingDirectory=  # Like: /home/mehdi/python/projects/LazyHelper
ExecStart= # Like: /home/mehdi/python/projects/LazyHelper/venv/bin/python manage.py runserver 0.0.0.0:8081
Restart=always

[Install]
WantedBy=multi-user.target

```

 Execute:
```shell
sudo systemctl enable LazyHelper
sudo systemctl start LazyHelper
```

Done !

### - Disable authentication ( NOT RECOMMENDED ) 
To use LazyHelper you have to log in by default, if you want to disable this behavior, go to "settings" section, disable "login-required" and save

> #### ❗️SECURITY WARNING
> By disabling authentication, anyone on your network can access your PC.  
> They can execute everything. even delete your whole OS !!
> 
> If you're on a public network, never disable authentication

---

### Your Pull Requests are so welcome !
Currently, I have no idea how to make this work on Windows. If you know, please submit a PR.

Also, any UI/UX improvements are welcome

### - [Telegram](https://t.me/PythonUnion)
