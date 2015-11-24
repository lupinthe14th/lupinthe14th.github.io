Title: N-DJBDNS インストールおよび設定手順
Summary: もっともセキュアと言われている N-DJBDNS のインストールと設定
Author: Hideo Suzuki
Date: 2015-11-23 17:00
Modified: 2015-11-23 17:00
Tags: Rasberry Pi2, ubuntu, 14.04, trusty, N-DJBDNS, djbdns, oss, dnscache, tinydns
Category: Rasberry Pi
Slug: ndjbdns

# N-DJBDNS のインストールおよび設定手順
Rasberry Pi2 (Ubuntu 14.04 arm) へ、もっともセキュアと言われている N-DJBDNS のイ
ンストールと設定を行います。


## 目的
以下の構成と基本動作を行う様にインストールと設定を行う。

### 構成

- tinydns: コンテンツ管理サーバー
- dnscache: キャッシュサーバー

としてローカルエリアのDNSとして動作させます。

### 基本動作

それぞれ、以下の動作を基本として設定します。

- tinydns
    - 127.0.0.1 で動作させる
    - ローカルドメインのコンテンツ管理サーバー

- dnscache
    - ローカルエリアからのクエリのみ受け付け
    - ローカルドメインであれば、tinydns へ問い合わせ
    - そうでなければ外部へ再帰検索を行う


## 前提

この手順の前提のハードウェアは、Rasberry Pi2 で、ディストリビューションは、
Ubuntu 14.04 を用います。

    $ uname -a
    Linux ubuntu 3.18.0-25-rpi2 #26-Ubuntu SMP PREEMPT Sun Jul 5 06:46:34 UTC 2015 armv7l armv7l armv7l GNU/Linux
    $ cat /etc/lsb-release
    DISTRIB_ID=Ubuntu
    DISTRIB_RELEASE=14.04
    DISTRIB_CODENAME=trusty
    DISTRIB_DESCRIPTION="Ubuntu 14.04.3 LTS"

# 構築手順

## インストール
以下のコマンドを実行し、必要パッケージも纏めてインストールする。

    $ sudo apt-get install djbdns

## 設定

### ユーザの追加

必要なユーザーを追加する。

    $ sudo adduser --no-create-home --disabled-login --shell /bin/false dnslog
    $ sudo adduser --no-create-home --disabled-login --shell /bin/false tinydns
    $ sudo adduser --no-create-home --disabled-login --shell /bin/false dnscache

### tinydns

1. configuration

        $ sudo su -
        # tinydns-conf tinydns dnslog /etc/tinydns/ 127.0.0.1
        # cd /etc/service ; ln -sf /etc/tinydns/

1. tinydns レコードを追加

    data ファイルを記述し、`tinydns-data` コマンドで、データベースを作成する。

    localhost.localdomain. をローカルドメインとして管理して名前解決させる。

    以下、data ファイルの作成例を以下に提示します。

    1. data ファイルの作成

            # vi /etc/tinydns/root/data
            .localhost.localdomain.:192.168.0.7:ns.localhost.localdomain.
            .0.168.192.in-addr.arpa.:192.168.0.7:ns.localhost.localdomain.
            
            =ns.localhost.localdomain.:192.168.0.7
            =gate.localhost.localdomain.:192.168.0.1
            =www.localhost.localdomain.:192.168.0.32

    1. `tinydns-data` コマンドでデータベースを作成

            # cd /etc/tinydns/root
            # tinydns-data
            # ls -al data.cdb

### dnscache

1. confiuration

        $ sudo su -
        # dnscache-conf dnscache dnslog /etc/dnscache 192.168.0.7
        # cd /etc/service ; ln -sf /etc/dnscache/

1. 外部キャッシュサーバーのアドレスを設定

    適宜自環境に合わせ、外部キャッシュサーバーに問い合わせする様に設定します。

    例として、 OpenDNS を問い合わせ先に設定する場合を記載します。

        # echo 208.67.222.222> /etc/dnscache/root/servers/@
        # echo 208.67.220.220>> /etc/dnscache/root/servers/@

1. 外部キャッシュサーバーに問い合わせするように設定

        # echo 1 > /etc/dnscache/env/FORWARDONLY

1. ローカルネットワークの接続を許可

    ローカルネットワーク内（今回は192.168.0.0/16）からのアクセスを許可

        $ sudo touch /etc/dnscache/root/ip/192.168

1. ローカルドメインとローカルアドレスの問い合わせ先設定

    localhost.localdomain ローカルドメインと、192.168.0.0/24 のローカルアドレス
    の逆引きは、tinydns に問い合わせするように設定。

        # echo 127.0.0.1>/etc/service/dnscache/root/servers/localhost.localdomain.
        # echo 127.0.0.1>/etc/service/dnscache/root/servers/0.168.192.in-addr.arpa.

## 起動
サービスの起動を行い、ステータスを確認する。

    # initctl start svscan
    svscan start/running, process 1612
    # svstat /etc/service/tinydns
    /etc/service/tinydns: up (pid 1619) 31 seconds
    # svstat /etc/service/dnscache
    /etc/service/dnscache: up (pid 2133) 11 seconds

## 個別のサービス起動・停止方法
tinydns, dnscache のサービスを個別に開始・停止する場合は以下のコマンドを実行す
る。

### tinydns

- start

        $ sudo svc -u /etc/service/tinydns

- stop

        $ sudo svc -d /etc/service/tinydns

### dnscache

- start

        $ sudo svc -u /etc/service/dnscache

- stop

        $ sudo svc -d /etc/service/dnscache

# 参考文献

- [DJBDNS (TinyDNS) Install From Packages](http://ubuntuforums.org/showthread.php?t=1630044)
- [djbdnsでローカルドメインの名前解決をおこなう](http://qiita.com/metheglin/items/01d3334c19ca559e25cf)

