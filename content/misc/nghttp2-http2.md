Title: nghttpd HTTP/2 お試し
Date: 2015-12-17 10:30
Modified: 2015-12-17 10:30
Category: misc
Tags: http2, Ubuntu, nghttp2, nghttpd, Systemworks, h2load, Hyper-V 2012 R2, lubuntu, benchmark
Slug: nghttpd-http2
Author: Hideo Suzuki
Summary: C言語のHTTP/2 server の実装の一つ、 nghttpd を試しに構築してベンチマークを取得してみる。
Status: 

# 目次

[TOC]

# はじめに

`nginx` 、 `H2O` それぞれの HTTP/1.1 と HTTP/2 でのベンチマークを取得した。その
ベンチマークの取得に利用したツール `h2load` は、HTTP/2 の C 言語の実装例である
`nghttp2` のライブラリの一つ。

このライブラリには、HTTP/2 server の、`nghttpd` もあるので、これの HTTP/2 のベン
チマークを取得する。[^1]

# お試し内容

- `nghttpd` 実行環境を Hyper-V 2012 R2 上の仮想サーバー（Ubuntu 14.04） に構築する
- `h2load` を用いてベンチマークを取得する
- `h2load` 実行クライアント（以後、負荷発生元クライアントと表記）は、同セグメント
  で別筐体上のHyper-V 2012 R2 上の仮想サーバーに構築した lubuntu を用いる
- SWITHING-HUB は、 1GBits/sec 規格
- HTTP/2 で、 `nginx` のデフォルト `index.html` と、大量画像ファイル表示用 HTML
  でのベンチマークを取得する

## 機器情報

測定の際に利用する機器は以下の通り。

### nghttpd サーバー

- ハードウェア: [Systemworks Server S4032](https://www.systemworks.co.jp/pms_s403x.php)
- ハイパバイザー: Hyper-V 2012 R2
- OS: Ubuntu

        # cat /proc/cpuinfo
        processor   : 0
        vendor_id   : GenuineIntel
        cpu family  : 6
        model       : 60
        model name  : Intel(R) Celeron(R) CPU G1820 @ 2.70GHz
        stepping    : 3
        microcode   : 0xffffffff
        cpu MHz     : 2677.835
        cache size  : 2048 KB
        physical id : 0
        siblings    : 1
        core id     : 0
        cpu cores   : 1
        apicid      : 0
        initial apicid  : 0
        fpu     : yes
        fpu_exception   : yes
        cpuid level : 13
        wp      : yes
        flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
        pat pse36 clflush mmx fxsr sse sse2 ss syscall nx lm constant_tsc rep_good
        nopl eagerfpu pni pclmulqdq ssse3 cx16 sse4_1 sse4_2 movbe popcnt xsave
        rdrand hypervisor lahf_lm abm xsaveopt fsgsbase erms
        bogomips    : 5355.67
        clflush size    : 64
        cache_alignment : 64
        address sizes   : 39 bits physical, 48 bits virtual
        power management:
    
        # free -h
                     total       used       free     shared    buffers     cached
        Mem:          1.9G       1.3G       689M       4.8M       116M       660M
        -/+ buffers/cache:       526M       1.4G
        Swap:         2.0G         0B       2.0G
    
        # arch
        x86_64
    
        # cat /etc/lsb-release
        DISTRIB_ID=Ubuntu
        DISTRIB_RELEASE=14.04
        DISTRIB_CODENAME=trusty
        DISTRIB_DESCRIPTION="Ubuntu 14.04.3 LTS"

### 負荷発生元クライアント

- ハードウェア: [Systemworks Server S9772](http://www.systemworks.co.jp/pms_s977x.php)
- ハイパバイザー: Hyper-V 2012 R2
- OS: lubuntu

        # cat /proc/cpuinfo
        processor   : 0
        vendor_id   : GenuineIntel
        cpu family  : 6
        model       : 62
        model name  : Intel(R) Xeon(R) CPU E5-2420 v2 @ 2.20GHz
        stepping    : 4
        microcode   : 0xffffffff
        cpu MHz     : 2170.472
        cache size  : 15360 KB
        physical id : 0
        siblings    : 1
        core id     : 0
        cpu cores   : 1
        apicid      : 0
        initial apicid  : 0
        fpu     : yes
        fpu_exception   : yes
        cpuid level : 13
        wp      : yes
        flags       : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
        pat pse36 clflush mmx fxsr sse sse2 ss syscall nx lm constant_tsc rep_good
        nopl eagerfpu pni pclmulqdq ssse3 cx16 sse4_1 sse4_2 popcnt aes xsave avx
        f16c rdrand hypervisor lahf_lm fsgsbase smep erms xsaveopt
        bugs        :
        bogomips    : 4340.94
        clflush size    : 64
        cache_alignment : 64
        address sizes   : 42 bits physical, 48 bits virtual
        power management:
    
        # free -h
                     total       used       free     shared    buffers     cached
        Mem:          982M       287M       694M       8.7M        23M       116M
        -/+ buffers/cache:       147M       834M
        Swap:         1.0G         0B       1.0G
    
        # arch
        x86_64
    
        # cat /etc/lsb-release
        DISTRIB_ID=Ubuntu
        DISTRIB_RELEASE=15.04
        DISTRIB_CODENAME=vivid
        DISTRIB_DESCRIPTION="Ubuntu 15.04"

### SWITCHING-HUB

- ハードウェア情報: [コレガ CG-SW16GTXLP](http://corega.jp/prod/sw16gtxlp/index.htm)

# nghttpd 実行環境の構築

## 前提パッケージのインストール

ソースからビルドする為の前提パッケージをインストールする。

```console
$ sudo apt-get install g++ make binutils autoconf automake autotools-dev \
                       libtool pkg-config zlib1g-dev libcunit1-dev \
                       libssl-dev libxml2-dev libev-dev libevent-dev \
                       libjansson-dev libjemalloc-dev cython python3-dev \
                       python-setuptools
```

ソースをダウンロードしてビルドおよびインストールを行う。

```console
$ cd /usr/local/src
$ sudo git clone https://github.com/tatsuhiro-t/nghttp2.git
$ cd nghttp2/
$ sudo autoreconf -i
$ sudo automake
$ sudo autoconf
$ sudo ./configure
$ sudo make
$ sudo make install
```

`nghttpd` コマンドが実行可能か確認する。
以下の様にコマンドを実行し、`nghttpd` コマンドのヘルプが表示されることを確認する。

```console
$ LD_LIBRARY_PATH=/usr/local/lib; export LD_LIBRARY_PATH
$ nghttpd --help
```

## nghttpd の設定

`nghttpd` の設定について以下に記載する。

1. ディレクトリの作成

    ドキュメントルートおよび証明書ファイルの格納ディレクトリを作成する。

        # mkdir -p /var/www/nghttpd
        # mkdir /usr/local/etc/nghttpd

1. 自己署名証明書の作成

    OpenSSL コマンドにて自己署名証明書を作成する。

    途中、証明書要求ファイルを作成する際に入力を求められるが、FQDN のみ適切な値
    を入力する。

        # cd /usr/local/etc/nghttpd
        # openssl genrsa 2048 > cert.key
        # openssl req -new -key cert.key  > cert.csr
        # openssl x509 -days 3650 -req -signkey cert.key < cert.csr > cert.pem

1. Supervisor のインストールおよび設定

    Supervisor のインストールを行い、nghttpd を登録して自動起動および起動停止を楽に
    出来る様にする。

    `apt-get` にて Supervisor のインストールを行う。

        # apt-get install supervisor

    `/etc/supervisor/conf.d/nghttpd.conf` の編集を行い Supervisor に、 `nghttpd`
    の設定を行う。

        [program:nghttpd]
        command=/usr/local/bin/nghttpd -m 1024 -d /var/www/nghttpd/ 443 /usr/local/etc/nghttpd/cert.key /usr/local/etc/nghttpd/cert.pem
        autostart=true
        autorestart=true
        environment=LD_LIBRARY_PATH="/usr/local/lib"

    Supervisor の再起動

        # service supervisor restart

    `nghttpd` の起動

        # supervisorctl start nghttpd

1. nginx デフォルト index.html の取得

    nginx サーバーから、 `wget` で `index.html` を取得する。

    nginx.localdomain
    :   nginx サーバーのFQDN

        # cd /var/www/nghttpd
        # wget https://nginx.localdomain/ --no-check-certificate

1. 大量画像表示サイトの構築

    大量の画像を表示するサイトを以下の方法で作成する。

    テスト画像を、[Caltech 101](http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ObjectCategories.tar.gz)
    からダウンロードして、解凍する。

        # cd /var/www/nghttpd
        # wget http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ObjectCategories.tar.gz
        # tar xfz 101_ObjectCategories.tar.gz

    画像数: 9144
    容量: 151MByte

    img.html (513KBytes) を以下の様に作成する。

        <html>
        <head>
        </head>
        <body>
        <h1>HTTP2 TEST</h1>
        <img src="101_ObjectCategories/BACKGROUND_Google/image_0001.jpg">
        <img src="101_ObjectCategories/BACKGROUND_Google/image_0002.jpg">
        <img src="101_ObjectCategories/BACKGROUND_Google/image_0003.jpg">
        <img src="101_ObjectCategories/BACKGROUND_Google/image_0004.jpg">
        <img src="101_ObjectCategories/BACKGROUND_Google/image_0005.jpg">
        ・
        ・
        ・
        <img src="101_ObjectCategories/yin_yang/image_0053.jpg">
        <img src="101_ObjectCategories/yin_yang/image_0054.jpg">
        <img src="101_ObjectCategories/yin_yang/image_0055.jpg">
        <img src="101_ObjectCategories/yin_yang/image_0056.jpg">
        <img src="101_ObjectCategories/yin_yang/image_0057.jpg">
        <img src="101_ObjectCategories/yin_yang/image_0058.jpg">
        <img src="101_ObjectCategories/yin_yang/image_0059.jpg">
        <img src="101_ObjectCategories/yin_yang/image_0060.jpg">
        </body>
        </html>

## ベンチマークの取得

試験内容と得られたベンチマーク値をそれぞれ記載する。

### nginx との比較用

後で nginx の結果と比較するので、同じ index.html (612bytes) を用いてベンチマークを
取得する。

1. リクエストコマンドの決定

    nginx で使用したリクエスト数を生成するコマンドにて実行する。

    - コマンド

        h2load -n 100000 -c 50 -m 50 https://www.example.com/

    - h2load オプション説明

        -n
        : 総リクエスト数

        -c
        : クライアント数

        -m
        : クライアント当たりの、最大ストリーム並列数

1. ベンチマーク

    `h2load` 実行結果は以下の通り。

        $ h2load -n 100000 -c 50 -m 50 https://www.example.com
        starting benchmark...
        spawning thread #0: 50 total client(s). 100000 total requests
        TLS Protocol: TLSv1.2
        Cipher: ECDHE-RSA-AES128-GCM-SHA256
        Server Temp Key: ECDH P-256 256 bits
        Application protocol: h2
        progress: 10% done
        progress: 20% done
        progress: 30% done
        progress: 40% done
        progress: 50% done
        progress: 60% done
        progress: 70% done
        progress: 80% done
        progress: 90% done
        progress: 100% done
        
        finished in 1.62s, 61841.20 req/s, 37.81MB/s
        requests: 100000 total, 100000 started, 100000 done, 100000 succeeded, 0 failed, 0 errored, 0 timeout
        status codes: 100000 2xx, 0 3xx, 0 4xx, 0 5xx
        traffic: 64106550 bytes total, 1105350 bytes headers (space savings 93.82%), 61200000 bytes data
                             min         max         mean         sd        +/- sd
        time for request:    12.82ms     97.39ms     33.33ms      9.64ms    89.78%
        time for connect:   240.24ms    282.18ms    259.50ms     12.82ms    54.00%
        time to 1st byte:   283.93ms    336.99ms    309.15ms     15.10ms    56.00%
        req/s (client)  :    1237.36     1255.62     1244.26        3.76    66.00%

### 大量画像表示での比較

大量に画像を表示する img.html (513Kbytes) を用いてベンチマークを取得する。

1. リクエストコマンドの決定

    クライアント数 = クライアント当たりの、最大ストリーム並列数 = 1021 から
    `client could not connect to host` が出始める [^2] ので、
    コマンドは以下を用いる。

    - コマンド
    
        h2load -n 100000 -c 1020 -m 1020 https://www.example.com/img.html

    - h2load オプション説明

        -n
        : 総リクエスト数

        -c
        : クライアント数

        -m
        : クライアント当たりの、最大ストリーム並列数

1. ベンチマーク

    `h2load` 実行結果は以下の通り。なお、 `H2O` の場合のベンチマークは、5秒毎に3
    回実行し、3回とも全てのリクエストが成功していた為、3回目の実行結果を採用し
    ていたが、 `nghttpd` では2回目3回目は HTTP4xx エラーが発生。

    そこで実行結果は以下に全て記載する。

    1回目

        $ h2load -n 100000 -c 1020 -m 1020 https://www.example.com/img.html
        starting benchmark...
        spawning thread #0: 1020 total client(s). 100000 total requests
        TLS Protocol: TLSv1.2
        Cipher: ECDHE-RSA-AES128-GCM-SHA256
        Server Temp Key: ECDH P-256 256 bits
        Application protocol: h2
        progress: 10% done
        progress: 20% done
        progress: 30% done
        progress: 40% done
        progress: 50% done
        progress: 60% done
        progress: 70% done
        progress: 80% done
        progress: 90% done
        progress: 100% done
        
        finished in 450.73s, 221.86 req/s, 111.22MB/s
        requests: 100000 total, 100000 started, 100000 done, 100000 succeeded, 0 failed, 0 errored, 0 timeout
        status codes: 100000 2xx, 0 3xx, 0 4xx, 0 5xx
        traffic: 52562510160 bytes total, 1485680 bytes headers (space savings 91.84%), 52530400000 bytes data
                             min         max         mean         sd        +/- sd
        time for request:     56.83s     446.96s     429.17s      34.98s    98.04%
        time for connect:   561.03ms     393.84s       5.30s      34.22s    99.22%
        time to 1st byte:      1.44s     394.08s       5.89s      34.19s    99.22%
        req/s (client)  :       0.22        0.26        0.23        0.01    76.47%

    2回目

        starting benchmark...
        spawning thread #0: 1020 total client(s). 100000 total requests
        TLS Protocol: TLSv1.2
        Cipher: ECDHE-RSA-AES128-GCM-SHA256
        Server Temp Key: ECDH P-256 256 bits
        Application protocol: h2
        progress: 10% done
        progress: 20% done
        progress: 30% done
        progress: 40% done
        progress: 50% done
        progress: 60% done
        progress: 70% done
        progress: 80% done
        progress: 90% done
        progress: 100% done
        
        finished in 72.37s, 1381.70 req/s, 106.76MB/s
        requests: 100000 total, 100000 started, 100000 done, 15386 succeeded, 84614 failed, 0 errored, 0 timeout
        status codes: 15386 2xx, 0 3xx, 84614 4xx, 0 5xx
        traffic: 8101811032 bytes total, 620554 bytes headers (space savings 94.87%), 8094934830 bytes data
                             min         max         mean         sd        +/- sd
        time for request:   220.26ms      69.56s      11.09s      24.84s    84.61%
        time for connect:      2.41s       3.50s       2.71s    209.69ms    61.67%
        time to 1st byte:      2.87s       3.55s       3.22s    178.49ms    60.20%
        req/s (client)  :       1.35       34.17       26.35       10.77    84.61%

    3回目

        starting benchmark...
        spawning thread #0: 1020 total client(s). 100000 total requests
        TLS Protocol: TLSv1.2
        Cipher: ECDHE-RSA-AES128-GCM-SHA256
        Server Temp Key: ECDH P-256 256 bits
        Application protocol: h2
        progress: 10% done
        progress: 20% done
        progress: 30% done
        progress: 40% done
        progress: 50% done
        progress: 60% done
        progress: 70% done
        progress: 80% done
        progress: 90% done
        progress: 100% done
        
        finished in 250.96s, 398.47 req/s, 110.43MB/s
        requests: 100000 total, 100000 started, 100000 done, 55272 succeeded, 44728 failed, 0 errored, 0 timeout
        status codes: 55272 2xx, 0 3xx, 44728 4xx, 0 5xx
        traffic: 29060038344 bytes total, 1028368 bytes headers (space savings 93.13%), 29041267160 bytes data
                             min         max         mean         sd        +/- sd
        time for request:   388.56ms     248.25s     132.46s     118.83s    55.27%
        time for connect:      1.48s       3.52s       2.72s    186.34ms    68.63%
        time to 1st byte:      2.75s       3.68s       3.23s    134.29ms    66.57%
        req/s (client)  :       0.39       35.69       14.20       15.37    57.94%

# 考察

## nginx と比較用

`nginx` との比較用でのベンチマークは、以下の表の通り。

Time (sec) | Requests/sec | succeeded/Requests
---------- | ------------ | ------------------
1.62       | 61841.20     | 1                 



## 大量画像表示での比較

大量画像表示でのベンチマークは、計測回毎に以下の表の通り。

計測回 | Time (sec) | Requests/sec | succeeded/Requests
------ | ---------- | ------------ | ------------------
1      | 450.73     | 221.86       | 1                 
2      | 72.37      | 1381.70      | 0.15386
3      | 250.96     | 398.47       | 0.55272

## まとめ

- `nginx` との比較用では、`H2O` とほぼ同じベンチマークが出た
- 大量画像表示でも、 `H2O` とほぼ同じベンチマークが出たが、2〜3回と繰り返すと
  HTTP4xx のエラーが発生。この条件だと信頼性は、`H2O` に軍配があがった

# 参考資料

- [Nghttp2: HTTP/2 C Library - nghttp2.org](https://nghttp2.org)
- [tatsuhiro-t/nghttp2](https://github.com/tatsuhiro-t/nghttp2)
- [Supervisor: A Process Control System &mdash; Supervisor 3.2.0 documentation](http://supervisord.org/)

[^1]:
    nghttpd は HTTP/2 プロトコルのみ動作するので HTTP/1.1 との比較検証は不可。

    nghttpx で可能かと思ったが、Reverse Proxy の為、単体での動作が不可なので
    HTTP/1.1 のベンチマーク取得はやめた。

[^2]: 負荷発生クライアント側の open files の上限値 `ulimit -n 1024` の為。
