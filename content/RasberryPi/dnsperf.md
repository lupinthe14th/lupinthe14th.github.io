Title: Nominum dnsperf / resperf での DNS キャッシュサーバーのストレステスト
Date: 2015-12-03 15:00
Modified: 2015-12-03 15:00
Category: Rasberry Pi
Tags: dns, ndjbdns, Mac, dnsperf, resperf, Rasberry Pi2
Slug: dnsperf
Author: Hideo Suzuki
Summary: DNS ストレスツール Nominum dnsperf / resperf を用いた Rasberry Pi2 で作ったNDJBDNS キャッシュサーバーのストレステスト

# 動機

[Raspberry PiでつくるDNS キャッシュサーバ](http://blog.watercloud.net/article/430549899.html) という記事
を読んで、自分もRasberry Pi で、NDJBDNS キャッシュサーバーを作っているので、ストレス
テストを実施してみようと思った。

# 目的

- Rasberry Pi2 で作った、NDJBDNS キャッシュサーバーのストレステスト
- Mac OS X からストレス付与出来るようにする。

# Install 手順

## 前提条件

このインストール手順は、Mac OS X Yosemite の場合についてです。

## dnsperf / resperf の Install

以下のコマンドをターミナルで実行する。

```console
% ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null
% brew install dnsperf
```

## gunplot の install

`resperf` の実行結果レポートを作成する `resperf-report` コマンドで使用する
`gunplot` をインストールする。


### AquaTerm、X11のインストール

`gunplot` で利用する出力先ターミナルを事前にインストールする。


#### AquaTerm のインストール

[AquaTermのダウンロードページ](http://sourceforge.net/projects/aquaterm/files/latest/download?source=files)
から、インストーラーをダウンロードしインストールする。



#### X11 のインストール

[Mac用の X11ライブラリ XQuartz のダウンロードページ](http://www.xquartz.org)
から、インストーラーをダウンロードして胃インストールする。



### gunplot のインストール

以下のオプションを付与したコマンドでインストールする。

```console
% brew install gnuplot --with-aquaterm --with-x11
```



# ストレステスト

ストレスツールのインストールが完了したので、目的であるRasberry Pi2 の DNS
キャッシュサーバーへストレステストを行う。

## dnsperf と resperf それぞれの特徴について

dnsperf と、resperf はそれぞれ以下の特徴がある。

- dnsperf

    - 権威サーバや、LAN環境でのキャッシュサーバのテストではO.K.
    - キャッシュのテストでWAN回線を使用した場合は結果が不十分になる可能性あり

        レスポンス状況でdnsperfの出す負荷(qps)が変化するため

- resperf

    - レスポンス状態にかかわらず負荷を上げていくことができる
    
        したがって、テスト時にWAN環境の影響を受けにくい

今回はLAN環境のDNSキャッシュサーバーのストレステストだが、レスポンス状態に関わら
ず負荷をあげたい為、 `resperf` を用いる。


## 事前準備

事前準備として、ストレステストで用いるクエリファイルを作成する。
クエリファイルの書式は、`queryperf` と同じ書式で以下の様に記載する。

```
domain type
```

サンプルは以下の通り。
試験の為に対象レコードは 100,000 規模で作成する。

```vim
example.com a
example.com soa
example.com ns
example.com mx
```

## ストレステストの実行

以下のコマンドを用いて、ストレステストを実行する。
192.168.0.7 は、ストレステスト対象のDNS キャッシュサーバーのIPアドレス。


```console
% resperf-report -s 192.168.0.7 -d query.txt -m 30000
```

## ストレステストの結果

### Statistics:

```
Queries sent:         222878
Queries completed:    222878
Queries lost:         0
Run time (s):         100.000000
Maximum throughput:   9612.000000 qps
Lost at that point:   17.32%
```

### Plots

![rate](./images/rate.png)
![latency](./images/latency.png)

# 参考資料

- [Raspberry PiでつくるDNS キャッシュサーバ](http://blog.watercloud.net/article/430549899.html)
- [DNSの評価と計測の話](https://www.nic.ad.jp/ja/materials/iw/2013/proceedings/d2/d2-hattori.pdf)
- [Install dnsperf on Mac OSX](http://macappstore.org/dnsperf/)
- [DNS BIND queryperf インストール 設定 利用](http://www.geocities.jp/yasasikukaitou/queryperf.html)
