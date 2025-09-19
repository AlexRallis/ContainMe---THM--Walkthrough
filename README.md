# ContainMe - THM -Walkthrough
<img width="90" height="89" alt="1_urU3DCALxSjKakNfdRlyGQ" src="https://github.com/user-attachments/assets/c9bc61b9-fea8-4efe-b9ad-c393bd913c37" />

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

RESULTS

```

## Shell

## Root Access



