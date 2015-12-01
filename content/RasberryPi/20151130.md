Title: chronyインストールおよび設定手順
Summary: NTPクライアントとNTPサーバーの実装のひとつchronyのインストールと設定
Author: Hideo Suzuki
Date: 2015-11-30 18:00
Modified: 2015-11-30 18:00
Tags: Rasberry Pi2, ubuntu, 14.04, trusty, oss, chrony, ntp
Category: Rasberry Pi
Slug: chrony


# chronyインストールおよび設定手順
Rasberry Pi2 (Ubuntu 14.04 arm) へ chrony をインストール。


## 目的
NTPクライアントおよびローカルネットワークのNTPサーバーとして動作させる。



## 前提

ハードウェアは、Rasberry Pi2 で、ディストリビューションは、Ubuntu 14.04

```console
$ uname -a
Linux ubuntu 3.18.0-25-rpi2 #26-Ubuntu SMP PREEMPT Sun Jul 5 06:46:34 UTC 2015 armv7l armv7l armv7l GNU/Linux
$ cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=14.04
DISTRIB_CODENAME=trusty
DISTRIB_DESCRIPTION="Ubuntu 14.04.3 LTS"
```



# 構築手順

## インストール
`apt-get` にてパッケージをインストールする。

```console
$ sudo apt-get install chrony
```

## 設定
設定ファイルの編集を行う。
オリジナルとの差分は以下の通り。


```diff
$ diff /etc/chrony/chrony.conf /etc/chrony/chrony.conf.org
20,24c20,23
< server ntp.jst.mfeed.ad.jp offline minpoll 8
< server ntp.nict.jp offline minpoll 8
< server s2csntp.miz.nao.ac.jp offline minpoll 8
< server ntp.ring.gr.jp offline minpoll 8
< server ntp.shoshin.co.jp offline minpoll 8
---
> server 0.debian.pool.ntp.org offline minpoll 8
> server 1.debian.pool.ntp.org offline minpoll 8
> server 2.debian.pool.ntp.org offline minpoll 8
> server 3.debian.pool.ntp.org offline minpoll 8
```

## 起動
サービスの再起動を行い、ステータスを確認する。

```console
$ sudo service chrony restart
Restarting time daemon: Starting /usr/sbin/chronyd...
chronyd is running and online.
$ sudo service chrony status
 * chronyd is running
```

## 同期状況の確認
`chronyc` を用いる。(`ntpq -p` で確認している内容と同様）

```console
$ chronyc sources
210 Number of sources = 5
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
^- ntp3.jst.mfeed.ad.jp          2   8    37   230  -1809us[-1809us] +/-  126ms
^* ntp-b2.nict.go.jp             1   8    37   231   -136us[ -336us] +/-   15ms
^- 133.40.41.136                 2   8    37   230  +2117us[+2117us] +/-   41ms
^+ ring.nict.go.jp               2   8    37   230  -6414us[-6414us] +/-   25ms
^- E210168211231.ec-userreve     1   8    37   231   +902us[ +902us] +/-   18ms
```



# 参考文献

- [How to install chrony package in Ubuntu Trusty](https://www.howtoinstall.co/en/ubuntu/trusty/universe/chrony/)
