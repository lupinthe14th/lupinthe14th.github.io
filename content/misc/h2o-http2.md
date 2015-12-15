Title: H2O HTTP/2 お試し
Date: 2015-12-15 16:00
Modified: 2015-12-15 16:00
Category: misc
Tags: http2, Ubuntu, h2o, Systemworks, h2load, Hyper-V 2012 R2, lubuntu
Slug: h2o-http2
Author: Hideo Suzuki
Summary: HTTP/1.x HTTP/2 に最適化された Web サーバーの実装の一つ、H2O を試しに構築してベンチマークを取得してみる。

# 目次

[TOC]

# はじめに

nginx HTTP/2 お試しを行った際に検索にヒットした
[H2O](https://h2o.examp1e.net) 。

nginx HTTP/2 のベンチマークもあることだし、IoT 時代のHTTPサーバーとの触れ込みも
あったのでモノは試しに検証してみます。

当初は、HTTP/1.1 と HTTP/2 で性能差が如実に出て終了となると思っていましたが、あ
まり性能差が出ないので、大量の画像ファイルの表示での性能差もお試ししてみました。

# H2O とは

> H2Oは現在ディー・エヌ・エーに勤める奥一穂氏を中心に、2014年から開発されている
> Webサーバー。プロジェクトの目的として、「クラウド、HTTP/2、常時TLS時代に最適化
> されたHTTPサーバーを目指す」としている。H2OはMITライセンスを採用したオープン
> ソースプロダクトで、ソースコードはGitHubで公開されている。

引用元: [Nginxより高速、HTTP/2 サーバー「H2O」](http://www.atmarkit.co.jp/ait/articles/1512/08/news037.html)

# お試し内容

- H2O サーバーを Hyper-V 2012 R2 上の仮想サーバー（Ubuntu 14.04） に構築する
- `h2load` を用いてベンチマークを取得する
- `h2load` 実行クライアント（以後、負荷発生元クライアントと表記）は、同セグメント
  で別筐体上のHyper-V 2012 R2 上の仮想サーバーに構築した lubuntu を用いる
- SWITHING-HUB は、 1GBit/sec 規格
- HTTP/1.1 と HTTP/2 での接続の違いによる性能差を比べる

## 機器情報

測定の際に利用する機器は以下の通り。

### H2O サーバー

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

# H2O 環境の構築

## 前提パッケージのインストール

ソースからビルドする為の前提パッケージをインストールする。

```console
$ sudo apt-get install cmake build-essential zlib1g zlib1g-dev
```

## OpenSSL 1.0.2 のインストール

前提であるOpenSSL をソースからインストールする。

その為に不要なパッケージを削除する。

```console
$ sudo apt-get remove --purge openssl libssl-dev
```

ソースをダウンロードしてビルドおよびインストールを行う。

```console
# cd /usr/local/src
# wget https://www.openssl.org/source/openssl-1.0.2e.tar.gz --no-check-certificate
# tar xfz openssl-1.0.2e.tar.gz
# cd openssl-1.0.2e/
# ./config --prefix=/usr/local --openssldir=/usr/local/openssl
# make
# make test
# make install
```


## H2O のビルドおよびインストール

以下のコマンドを実行して、ビルドおよびインストールを行う。

```console
$ sudo su -
# cd /usr/local/src
# wget https://github.com/h2o/h2o/archive/v1.6.0.tar.gz
# tar xfz v1.6.0.tar.gz
# cd h2o-1.6.0/
# cmake -DWITH_BUNDLED_SSL=on .
# make
# make install
```

## H2O の設定

H2O の設定について以下に記載する。

1. ディレクトリの作成

    ドキュメントルート、設定ファイルおよびログ出力先のディレクトリを作成する。

        # mkdir -p /var/www/h2o
        # mkdir /usr/local/etc/h2o
        # mkdir /var/log/h2o

1. 自己署名証明書の作成

    OpenSSL コマンドにて自己署名証明書を作成する。

    途中、証明書要求ファイルを作成する際に入力を求められるが、FQDN のみ適切な値
    を入力する。

        # cd /usr/local/etc/h2o
        # openssl genrsa 2048 > cert.key
        # openssl req -new -key cert.key  > cert.csr
        # openssl x509 -days 3650 -req -signkey cert.key < cert.csr > cert.pem

1. h2o.conf の作成

    お試し用の `/usr/local/etc/h2o/h2o.conf` の作成を行う。

        hosts:
          "www.example.com":
            listen:
              port: 443
              ssl:
                certificate-file: /usr/local/etc/h2o/cert.pem
                key-file:         /usr/local/etc/h2o/cert.key
            paths:
              "/":
                file.dir: /var/www/h2o
        
        http2-reprioritize-blocking-assets: ON   # performance tuning option

1. Supervisor のインストールおよび設定

    Supervisor のインストールを行い、H2O を登録して自動起動および起動停止を楽に
    出来る様にする。

    `apt-get` にて Supervisor のインストールを行う。

        # apt-get install supervisor

    `/etc/supervisor/conf.d/h2o.conf` の編集を行い Supervisor に、 H2O の設定を
    行う。

        [program:h2o]
        command=/usr/local/bin/h2o -c /usr/local/etc/h2o/h2o.conf
        autostart=true
        autorestart=true

    Supervisor の再起動

        # service supervisor restart

    h2o の起動

        # supervisorctl start h2o


1. 大量画像表示サイトの構築

    大量の画像を表示するサイトを以下の方法で作成する。

    テスト画像を、[Caltech 101](http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ObjectCategories.tar.gz)
    からダウンロードして、解凍する。

        # cd /var/www/h2o
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

後でnginx の結果と比較するので、同じ index.html (612bytes) を用いてベンチマークを
取得する。

1. リクエストコマンドの決定

    nginx で使用したリクエスト数を生成するコマンドにて実行する。
    なお、H2O は サーバー側の設定で、 HTTP/1.1 で動作させる様に設定できないっぽ
    い。
    その為、HTTP/1.1 のベンチマーク取得の場合は、h2load のオプションに
    `--h1` を付与して、強制的に HTTP/1.1 接続する。

    - コマンド
    
        HTTP/2
        :    `h2load -n 100000 -c 50 -m 50 https://www.example.com/`

        HTTP/1.1
        :    `h2load -n 100000 -c 50 -m 50 --h1 https://www.example.com/`

    - h2load オプション説明

        -n
        : 総リクエスト数

        -c
        : クライアント数

        -m
        : クライアント当たりの、最大ストリーム並列数

        --h1
        : 接続プロトコルを HTTP/1.1 に強制

1. HTTP/2 でのベンチマーク

    HTTP/2 の場合に取得した値は以下の通り。

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
        
        finished in 1.62s, 61617.18 req/s, 37.79MB/s
        requests: 100000 total, 100000 started, 100000 done, 100000 succeeded, 0 failed, 0 errored, 0 timeout
        status codes: 100000 2xx, 0 3xx, 0 4xx, 0 5xx
        traffic: 64306650 bytes total, 1305150 bytes headers (space savings 92.50%), 61200000 bytes data
                             min         max         mean         sd        +/- sd
        time for request:     1.18ms    103.48ms     32.18ms     11.91ms    74.81%
        time for connect:   240.06ms    303.13ms    270.74ms     19.41ms    56.00%
        time to 1st byte:   302.93ms    368.81ms    327.42ms     17.43ms    74.00%
        req/s (client)  :    1233.07     1474.02     1275.80       52.54    80.00%

1. HTTP/1.1 でのベンチマーク

    HTTP/1.1 の場合に取得した値は以下の通り。

        $ h2load -n 100000 -c 50 -m 50 --h1 https://www.example.com
        starting benchmark...
        spawning thread #0: 50 total client(s). 100000 total requests
        TLS Protocol: TLSv1.2
        Cipher: ECDHE-RSA-AES128-GCM-SHA256
        Server Temp Key: ECDH P-256 256 bits
        Application protocol: http/1.1
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
        
        finished in 1.95s, 51409.78 req/s, 41.53MB/s
        requests: 100000 total, 100000 started, 100000 done, 100000 succeeded, 0 failed, 0 errored, 0 timeout
        status codes: 100000 2xx, 0 3xx, 0 4xx, 0 5xx
        traffic: 84700000 bytes total, 18400000 bytes headers (space savings 0.00%), 61200000 bytes data
                             min         max         mean         sd        +/- sd
        time for request:     1.83ms    176.01ms     41.44ms     14.27ms    88.34%
        time for connect:   153.23ms    304.62ms    261.51ms     39.09ms    84.00%
        time to 1st byte:   271.43ms    344.54ms    319.40ms     18.66ms    78.00%
        req/s (client)  :    1028.91     1064.36     1041.95        8.90    62.00%


### 大量画像表示での比較

大量に画像を表示する img.html (513Kbytes) を用いてベンチマークを取得する。

1. リクエストコマンドの決定

    クライアント数 = クライアント当たりの、最大ストリーム並列数 = 1021 から
    `client could not connect to host` が出始める [^1] ので、
    コマンドは以下を用いる。

    - コマンド
    
        HTTP/2
        :    `h2load -n 100000 -c 1020 -m 1020 https://www.example.com/img.html`

        HTTP/1.1
        :    `h2load -n 100000 -c 1020 -m 1020 --h1 https://www.example.com/img.html`

    - h2load オプション説明

        -n
        : 総リクエスト数

        -c
        : クライアント数

        -m
        : クライアント当たりの、最大ストリーム並列数

        --h1
        : 接続プロトコルを HTTP/1.1 に強制

1. HTTP/2 でのベンチマーク

    HTTP/2 の場合に取得した値は以下の通り。

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
        
        finished in 459.49s, 217.63 req/s, 109.09MB/s
        requests: 100000 total, 100000 started, 100000 done, 100000 succeeded, 0 failed, 0 errored, 0 timeout
        status codes: 100000 2xx, 0 3xx, 0 4xx, 0 5xx
        traffic: 52562722760 bytes total, 1682620 bytes headers (space savings 90.60%), 52530400000 bytes data
                             min         max         mean         sd        +/- sd
        time for request:    399.97s     457.42s     444.73s      10.91s    74.85%
        time for connect:   902.87ms       3.95s       2.43s    593.99ms    81.27%
        time to 1st byte:      2.06s       4.34s       3.01s    508.95ms    73.24%
        req/s (client)  :       0.21        0.24        0.22        0.01    75.78%


1. HTTP/1.1 でのベンチマーク

    HTTP/1.1 の場合に取得した値は以下の通り。

        $ h2load -n 100000 -c 1020 -m 1020 --h1 https://www.example.com/img.html
        starting benchmark...
        spawning thread #0: 1020 total client(s). 100000 total requests
        TLS Protocol: TLSv1.2
        Cipher: ECDHE-RSA-AES128-GCM-SHA256
        Server Temp Key: ECDH P-256 256 bits
        Application protocol: http/1.1
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
        
        finished in 459.23s, 217.75 req/s, 109.14MB/s
        requests: 100000 total, 100000 started, 100000 done, 100000 succeeded, 0 failed, 0 errored, 0 timeout
        status codes: 100000 2xx, 0 3xx, 0 4xx, 0 5xx
        traffic: 52554400000 bytes total, 18900000 bytes headers (space savings 0.00%), 52530400000 bytes data
                             min         max         mean         sd        +/- sd
        time for request:      3.29s     458.31s     230.99s     131.57s    57.74%
        time for connect:   877.84ms       3.80s       2.44s    526.48ms    87.55%
        time to 1st byte:      1.97s       4.28s       3.13s    460.73ms    82.16%
        req/s (client)  :       0.21        0.25        0.22        0.01    79.31%

# 考察

## nginx と比較用

nginx との比較用でのベンチマークは、HTTP/1.1 および HTTP/2 でそれぞれ
以下の表の通り。


HTTP Version | Time (sec) | Requests/sec | Requests/succeeded
------------ | ---------- | ------------ | ------------------
1.1          | 1.95       | 51409.78     | 1                 
2            | 1.62       | 61617.18     | 1                 



## 大量画像表示での比較

大量画像表示でのベンチマークは、HTTP/1.1 および HTTP/2 でそれぞれ
以下の表の通り。


HTTP Version | Time (sec) | Requests/sec | Requests/succeeded
------------ | ---------- | ------------ | ------------------
1.1          | 459.23     | 217.75       | 1                 
2            | 459.49     | 217.63       | 1                 

## まとめ

- H2O の場合だと、このリクエスト規模ではHTTP/1.1 と HTTP/2 の性能差は、 HTTP/2
  の方が若干速い程度

- 単純なHTMLを表示する場合でも、大量画像表示HTMLの場合でも、HTTP/1.1 と、HTTP/2
  の性能差は見られなかった

- つまり、HTTP/2 対応のブラウザのみがこの速度の恩恵を受けるものではない

- 爆速との記事を多数みてましたが、爆速。nginx との比較は後でやろうと思いますが約
  2倍の速さ

# 参考資料

- [H2O - the optimized HTTP/2 server](https://h2o.examp1e.net)
- [H2O - making HTTP better](http://www.slideshare.net/kazuho/h2o-43944586)
- [Home · h2o/h2o Wiki](https://github.com/h2o/h2o)
- [Kazuho's Weblog: H2O HTTP/2 server version 1.6.0 released](http://blog.kazuhooku.com/2015/12/h2o-http2-server-version-160-released.html)
- [h2o + supervisord で Munin を HTTP/2 でサーブさせてみた - mallowlabsの備忘録](http://d.hatena.ne.jp/mallowlabs/20150828/h2o_supervisord_munin)
- [Supervisor: A Process Control System &mdash; Supervisor 3.2.0 documentation](http://supervisord.org/)
- [[HTTP2] WindowsServerでHTTP2のベンチマーク - Qiita](http://qiita.com/0xfffffff7/items/dc41cf560e0e0ea4bdbc)


[^1]: 負荷発生クライアント側の open files の上限値 `ulimit -n 1024` の為。

