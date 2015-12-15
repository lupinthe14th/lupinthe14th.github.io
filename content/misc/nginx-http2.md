Title: nginx HTTP/2 お試し
Date: 2015-12-09 17:40
Modified: 2015-12-15 16:41
Category: misc
Tags: http2, Ubuntu, nginx, Systemworks, h2load, Hyper-V 2012 R2,
Slug: nginx-http2
Author: Hideo Suzuki
Summary: nginx 1.9.5 で HTTP/2 がサポートされたので試しに構築してベンチマーク取
得してみた。

この記事は、[nginx Advent Calendar 2015](http://qiita.com/advent-calendar/2015/nginx)
の9日目の記事です。

# はじめに

HTTP/2 が nginx 1.9.5 でサポートされた事を今更ながら知った。
どんなものかお試ししてみる。

この記事は、お試しする為の環境構築とお試し内容およびその考察について記載したもの
です。

# お試し内容

- nginx 1.9.5 のhttp2 が有効か無効かの違いのみで、 `h2load` を用いてベンチマーク
  を取得する。

- `h2load` 実行クライアント（以後、負荷発生元クライアントと表記）は、同セグメント
  で別筐体上のHyper-V 2012 R2 上の仮想サーバーに構築した lubuntu を用いる。

## 機器情報

測定の際に利用する機器は以下の通り。

### nginx サーバー

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


## 環境構築

測定を行う為に用いたnginx サーバーと 負荷発性元クライアントの構築方法をそれぞれ
以下に記載する。

### 負荷発生元クライアントの構築

負荷発生元クライアントに、`h2load` をソースからインストールする。

1. 必要パッケージのインストール

    以下コマンドにて事前に必要なパッケージをインストールする。

        $ sudo apt-get install g++ make binutils autoconf automake \
                       autotools-dev libtool pkg-config zlib1g-dev \
                       libcunit1-dev libssl-dev libxml2-dev libev-dev \
                       libevent-dev libjansson-dev libjemalloc-dev cython \
                       python3-dev python-setuptools

1. ソースの取得

    github リポジトリから、`git clone` にて、リポジトリのクローンを作成する。

        $ cd /usr/local/src
        $ sudo git clone https://github.com/tatsuhiro-t/nghttp2.git

1. make

    `make` コマンドにて、ビルド -> インストールを行う。

        $ cd nghttp2/
        $ sudo autoreconf -i
        $ sudo automake
        $ sudo autoconf
        $ sudo ./configure
        $ sudo make
        $ sudo make install

1. ライブラリへパスを通す

    ホームディレクトリの `.profile` を編集してライブラリへパスを通す。

        LD_LIBRARY_PATH=/usr/local/lib; export LD_LIBRARY_PATH

1. h2load コマンドの確認

    `.profile` 編集後、 `h2load` コマンドが実行可能か確認する。以下の様にコマンド
    を実行し、`h2load` コマンドのヘルプが表示されることを確認する。

        $ source ~/.profile
        $ h2load --help

### nginx サーバーの構築

nginx サーバーの構築方法を以下に記載する。

#### nginx 1.9.5 のインストール

nginx サーバーに、nginx 1.9.5 をソースからインストールする。

1. 前提パッケージのインストール

    `apt-get` にてビルドに必要なパッケージをインストールする。

        # sudo apt-get install build-essential libc6 libpcre3 libpcre3-dev \
                      libpcrecpp0 libssl0.9.8 libssl-dev zlib1g zlib1g-dev lsb-base

1. ソースのダウンロードと解凍

    以下のコマンドでソースをダウンロードし、解凍を行う。

        # cd /usr/local/src
        # wget http://nginx.org/download/nginx-1.9.5.tar.gz
        # tar xvfz nginx-1.9.5.tar.gz

1. make

    以下のコマンドにて、ビルドを行う。

        # ./configure --with-http_ssl_module \
                      --with-http_v2_module \
                      --with-debug
        # make
        # make install

####  nginx の設定

1. nginx.conf の作成

    お試し用の `/usr/local/nginx/conf/nginx.conf` の作成を行う。

    以下は、HTTP/2 を有効にした場合で、HTTP/2 を無効にする場合は、

    `listen       443 ssl http2;` を `listen       443 ssl;`
    に変更する。

        worker_processes  1;
        
        events {
            worker_connections  16384;
        }
        
        http {
            include       mime.types;
            default_type  application/octet-stream;
        
            sendfile        on;
        
            keepalive_timeout  65;
        
            server {
                listen       443 ssl http2;
        
                ssl_certificate      cert.pem;
                ssl_certificate_key  cert.key;
        
                ssl_session_cache    shared:SSL:1m;
                ssl_session_timeout  5m;
        
                ssl_ciphers  AESGCM:HIGH:!aNULL:!MD5;
                ssl_prefer_server_ciphers  on;
        
                location / {
                    root   html;
                    index  index.html index.htm;
                }
            }
        }

1. 自己署名証明書の作成

    OpenSSL コマンドにて自己署名証明書を作成する。

    途中、証明書要求ファイルを作成する際に入力を求められるが、FQDN のみ適切な値
    を入力する。

        # cd /usr/local/nginx/conf/
        # openssl genrsa 2048 > cert.key
        # openssl req -new -key cert.key  > cert.csr
        # openssl x509 -days 3650 -req -signkey cert.key < cert.csr > cert.pem

1. nginx Upstart の設定

    Upstart に登録して自動起動および起動停止を楽に出来る様にする。

    `/etc/init/nginx.conf` ファイルを作成する。

         # nginx
         
         description "nginx http daemon"
         author "George Shammas <georgyo@gmail.com>"
         
         start on (filesystem and net-device-up IFACE=lo)
         stop on runlevel [!2345]
         
         env DAEMON=/usr/local/nginx/sbin/nginx
         env PID=/var/run/nginx.pid
         
         expect fork
         respawn
         respawn limit 10 5
         #oom never
         
         pre-start script
                 $DAEMON -t
                 if [ $? -ne 0 ]
                         then exit $?
                 fi
         end script
         
         exec $DAEMON

     Upstart の設定の再読み込み

         # initctl reload-configuration

     Upstar Job list の確認

         # initctl list | grep nginx

     nginx の起動

         # initctl start nginx

#### 備考: nginx 1.9.X のパッケージからのインストール

パッケージ探すのが面倒で、「いいや、ソースからビルドしてインストールしよう。」
と思い上記の通りとなったのだが、調べている内にパッケージインストールの方法も
見つかったし、後の設定も楽だなと再認識。

調べてる内にヒットしたサイトを元に試したパッケージインストールの方法も簡単に記載する。
なお、お試しはソースインストールした場合で実施している。

1. 公式リポジトリを追加

    nginxサイトが配布するPGPキーを追加する。

        $ curl http://nginx.org/keys/nginx_signing.key | sudo apt-key add -

    リポジトリを一覧に追加する。この時、stable ではなく、 mainline を追加しま
    す。

        $ sudo sh -c "echo 'deb http://nginx.org/packages/mainline/ubuntu/ trusty nginx' >> /etc/apt/sources.list"
        $ sudo sh -c "echo 'deb-src http://nginx.org/packages/mainline/ubuntu/ trusty nginx' >> /etc/apt/sources.list"

1. インストール

    公式リポジトリの最新のパッケージをインストールします。

        $ sudo apt-get update
        $ sudo apt-get install nginx

    インストール後の設定ファイルと自己署名証明書の設定は上記の通り。

    今回パッケージインストールした後の `nginx -V` コマンドの結果は以下の通り。

        $ nginx -V
        nginx version: nginx/1.9.8
        built by gcc 4.8.4 (Ubuntu 4.8.4-2ubuntu1~14.04)
        built with OpenSSL 1.0.1f 6 Jan 2014
        TLS SNI support enabled
        configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx
        --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log
        --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid
        --lock-path=/var/run/nginx.lock
        --http-client-body-temp-path=/var/cache/nginx/client_temp
        --http-proxy-temp-path=/var/cache/nginx/proxy_temp
        --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp
        --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp
        --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx
        --with-http_ssl_module --with-http_realip_module --with-http_addition_module
        --with-http_sub_module --with-http_dav_module --with-http_flv_module
        --with-http_mp4_module --with-http_gunzip_module
        --with-http_gzip_static_module --with-http_random_index_module
        --with-http_secure_link_module --with-http_stub_status_module
        --with-http_auth_request_module --with-threads --with-stream
        --with-stream_ssl_module --with-http_slice_module --with-mail
        --with-mail_ssl_module --with-file-aio --with-http_v2_module
        --with-cc-opt='-g -O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat
        -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2'
        --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro -Wl,--as-needed'
        --with-ipv6

## ベンチマークの取得

nginx デフォルトの index.html (612bytes) を用いてベンチマークを取得する。

1. リクエストコマンドの決定

    まず、HTTP/2 の場合に全て成功する場合のリクエストを生成する
    コマンドを決定する。

    今回構築した環境で全て成功するリクエストと失敗が発生するリクエストの境界値は
    以下コマンドにて生成したリクエストだった。

        $ h2load -n 100000 -c 50 -m 50 https://nginx/

    - -n: 総リクエスト数
    - -c: クライアント数
    - -m: クライアント当たりの、最大ストリーム並列数
    
    なお、総リクエスト数は変更せず、クライアント数＝最大ストリーム並列数として境
    界値を探った。

1. HTTP/2 でのベンチマーク

    HTTP/2 の場合に取得した値は以下の通り。

        $ h2load -n 100000 -c 50 -m 50 https://nginx/
        starting benchmark...
        spawning thread #0: 50 total client(s). 100000 total requests
        TLS Protocol: TLSv1.2
        Cipher: ECDHE-RSA-AES256-GCM-SHA384
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
    
        finished in 3.69s, 27122.09 req/s, 19.76MB/s
        requests: 100000 total, 100000 started, 100000 done, 100000 succeeded, 0 failed, 0 errored, 0 timeout
        status codes: 100000 2xx, 0 3xx, 0 4xx, 0 5xx
        traffic: 76402450 bytes total, 13400000 bytes headers (space savings 23.86%), 61200000 bytes data
                             min         max         mean         sd        +/- sd
        time for request:     1.09ms    283.45ms     75.19ms     32.83ms    77.78%
        time for connect:   173.30ms       1.75s    496.19ms    487.37ms    80.00%
        time to 1st byte:   212.51ms       1.83s    592.09ms    482.91ms    80.00%
        req/s (client)  :     542.83      616.43      567.14       14.13    72.00%

1. HTTP/1.1 でのベンチマーク

    HTTP/1.1 の場合に取得した値は以下の通り。

        $ h2load -n 100000 -c 50 -m 50 https://nginx/
        starting benchmark...
        spawning thread #0: 50 total client(s). 100000 total requests
        TLS Protocol: TLSv1.2
        Cipher: ECDHE-RSA-AES256-GCM-SHA384
        Server Temp Key: ECDH P-256 256 bits
        Application protocol: http/1.1
        progress: 20% done
        progress: 30% done
        progress: 90% done
        progress: 100% done
    
        finished in 2.08s, 23729.25 req/s, 19.04MB/s
        requests: 100000 total, 73062 started, 100000 done, 49365 succeeded, 50635 failed, 50635 errored, 0 timeout
        status codes: 49365 2xx, 0 3xx, 0 4xx, 0 5xx
        traffic: 41526288 bytes total, 9179625 bytes headers (space savings 0.00%), 30211380 bytes data
                             min         max         mean         sd        +/- sd
        time for request:      916us    253.71ms     17.18ms     30.66ms    92.47%
        time for connect:    22.45ms    165.97ms     74.17ms     43.27ms    74.00%
        time to 1st byte:    23.37ms    174.92ms     78.54ms     45.33ms    74.00%
        req/s (client)  :     291.79      667.97      545.61      122.03    80.00%

### ご参考

当初、HTTP/1.1 で全て処理できるリクエスト数を探り、同じリクエストを発行して
HTTP/2の場合と比較するつもりだったが、HTTP/1.1 の場合は
クライアント数＝最大ストリーム数＝１となった為、このリクエストでは負荷を与え
られてないと判断したので、この観点からの検証はやめることにした。

なお、その時のコマンドの実行結果は以下の通り。

```console
$ h2load -n 100000 -c 1 -m 1 https://nginx/
starting benchmark...
spawning thread #0: 1 total client(s). 100000 total requests
TLS Protocol: TLSv1.2
Cipher: ECDHE-RSA-AES256-GCM-SHA384
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

finished in 103.20s, 968.98 req/s, 795.35KB/s
requests: 100000 total, 100000 started, 100000 done, 100000 succeeded, 0 failed, 0 errored, 0 timeout
status codes: 100000 2xx, 0 3xx, 0 4xx, 0 5xx
traffic: 84051000 bytes total, 18595000 bytes headers (space savings 0.00%), 61200000 bytes data
                      min         max         mean        sd        +/- sd
time for request:      778us      8.32ms      1.01ms       121us    97.33%
time for connect:     2.28ms      2.28ms      2.28ms         0us   100.00%
time to 1st byte:     3.44ms      3.44ms      3.44ms         0us   100.00%
req/s (client)  :     968.98      968.98      968.98        0.00   100.00%
```

# 考察

HTTP/1.1 および HTTP/2 はそれぞれ以下の表の通り。

HTTP Version | Time (sec) | Requests/sec | Requests/succeeded
------------ | ---------- | ------------ | ------------------
1.1          | 2.08       | 23729.25     | 0.49365           
2            | 3.69       | 27122.09     | 1                 

このお試しにより得られた結果としては以下のことが言えると思う。多少荒っぽい感も否
めないが……。

- 表より、HTTP/2 が耐えられるリクエスト数は、HTTP/1.1 では半分が耐えられない
- ご参考に記載しているが、HTTP/1.1 では、全てのリクエストが成功するのは、
  クライアント数＝最大ストリーム並列数＝1 の場合のみ
- HTTP/2 でも、クライアント数＝最大ストリーム並列数＝70でも全て成功する場合も
  あったが、何度繰り返しても成功するのは、50の場合
- よって全てのリクエストを処理する能力を単純比較すると、HTTP/2 は、HTTP/1.1 の50倍

# 参考資料

- [NGINX Open Source 1.9.5 Released with HTTP/2 Support](https://www.nginx.com/blog/nginx-1-9-5/)
- [tatsuhiro-t/nghttp2](https://github.com/tatsuhiro-t/nghttp2)
- [nghttp2を使用する #1](http://qiita.com/0xfffffff7/items/c8f195c9f1782ca64e92)
- [Nginx 1.9.5 でHTTP2を試そう！ - あすのかぜ](http://d.hatena.ne.jp/ASnoKaze/20150923/1442937121)
- [Ubuntu Upstart | NGINX](https://www.nginx.com/resources/wiki/start/topics/examples/ubuntuupstart/)
- [nginxでhttp2を有効にする](https://sudosan.net/nginx-http2-enable/)
- [[HTTP2] WindowsServerでHTTP2のベンチマーク](http://qiita.com/0xfffffff7/items/dc41cf560e0e0ea4bdbc)
- [ServerBenchmarkRoundH210](https://github.com/tatsuhiro-t/nghttp2/wiki/ServerBenchmarkRoundH210)
