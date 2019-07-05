Title: Arch Linux ARM on Rasberry Pi2 の初期設定
Summary: Rasberry Pi2 インストールした Arch Linux ARM の初期設定を行う。
Author: Hideo Suzuki
Date: 2016-10-13 02:15
Modified: 2016-10-18 00:00
Tags: Rasberry Pi2, Arm Linux ARM, gvim, tmux, pacman, sysctl, netctl

[TOC]

# はじめに

## 前提
設定はMacBook AirからSSH接続にて実施する。

# 初期設定

## ルートパーティションのリサイズ

インストールデフォルトだと、ルートパーティションのサイズが1.8Gしかありません。
これをリサイズしてデバイスサイズ全て使うようにします。

```
# df -h
ファイルシス   サイズ  使用  残り 使用% マウント位置
/dev/root        1.8G  1.7G     0  100% /
devtmpfs         457M     0  457M    0% /dev
tmpfs            462M     0  462M    0% /dev/shm
tmpfs            462M  320K  461M    1% /run
tmpfs            462M     0  462M    0% /sys/fs/cgroup
tmpfs            462M     0  462M    0% /tmp
/dev/mmcblk0p1   100M   18M   82M   19% /boot
tmpfs             93M     0   93M    0% /run/user/1000
```

### パーティションテーブルの確認

```
# fdisk /dev/mmcblk0

fdisk (util-linux 2.28.2) へようこそ。
ここで設定した内容は、書き込みコマンドを実行するまでメモリのみに保持されます。
書き込みコマンドを使用する際は、注意して実行してください。

コマンド (m でヘルプ): p
ディスク /dev/mmcblk0: 14.7 GiB, 15804137472 バイト, 30867456 セクタ
単位: セクタ (1 * 512 = 512 バイト)
セクタサイズ (論理 / 物理): 512 バイト / 512 バイト
I/O サイズ (最小 / 推奨): 512 バイト / 512 バイト
ディスクラベルのタイプ: dos
ディスク識別子: 0xf6e75bf4

デバイス       起動 開始位置 最後から   セクタ サイズ Id タイプ
/dev/mmcblk0p1          2048   206847   204800   100M  c W95 FAT32 (LBA)
/dev/mmcblk0p2        206848 30867455 30660608  14.6G 83 Linux
```


### リサイズ

パーティションテーブルの確認するとルートパーティションを割り当てているデバイスは
14.6Gなのでリサイズします。


```
# resize2fs /dev/mmcblk0p2
resize2fs 1.43.3 (04-Sep-2016)
Filesystem at /dev/mmcblk0p2 is mounted on /; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 1
The filesystem on /dev/mmcblk0p2 is now 3832576 (4k) blocks long.

```

リサイズ確認すると、サイズが15Gに拡張されています。

```
# df -h
ファイルシス   サイズ  使用  残り 使用% マウント位置
/dev/root         15G  1.7G   13G   12% /
devtmpfs         457M     0  457M    0% /dev
tmpfs            462M     0  462M    0% /dev/shm
tmpfs            462M  320K  461M    1% /run
tmpfs            462M     0  462M    0% /sys/fs/cgroup
tmpfs            462M     0  462M    0% /tmp
/dev/mmcblk0p1   100M   18M   82M   19% /boot
tmpfs             93M     0   93M    0% /run/user/1000
```


## タイムゾーン

デフォルト設定の ```/etc/localtime``` のシンボリックリンクを削除し新しくタイムゾーンを設定する。

```
# rm -i /etc/localtime
rm: remove symbolic link '/etc/localtime'? y
# ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
```

## ロケール

```/etc/locale.gen``` を編集して使用するロケール（ja_JP.UTF-8 UTF-8) をアンコメントし、次のコマンドを実行する。

```
# locale-gen
Generating locales...
  ja_JP.UTF-8... done
Generation complete.
```

ロケールを /etc/locale.conf で設定する。

```
# echo LANG=ja_JP.UTF-8 > /etc/locale.conf
```

## ホスト名変更

### ```hostnamectl``` コマンドの実行

以下のコマンドを実行する。 ```newhostname``` は適宜変更。

```
# hostnamectl set-hostname newhostname
```

### ```/etc/hosts``` の修正

変更したホスト名を ```/etc/hosts``` に追記する。
後でIPv6を無効化するので、IPv6ホストをコメントアウトしておく。

```
# vi /etc/hosts

#
# /etc/hosts: static lookup table for host names
#

#<ip-address>   <hostname.domain.org>   <hostname>
127.0.0.1       localhost.localdomain   localhost newhostname
#::1             localhost.localdomain   localhost

# End of file
```


## 固定IPアドレス

プロファイルを使ってネットワーク接続を管理・設定する CLI ベースのツール ```netctl``` を使って固定IPアドレスの設定を行う。
このツールは ```netcfg``` ユーティリティを置き換える新しい Arch Linux の独自プロジェクトです。

### ```netctl``` のインストール

```
# pacman -Sy netctl

:: Synchronizing package databases...
error: failed retrieving file 'core.db' from mirror.archlinuxarm.org : Operation too slow. Less than 1 bytes/sec transferred the last 10 seconds
error: failed to update core (download library error)
 extra                      2.4 MiB  1976K/s 00:01 [########################] 100%
 community                  3.9 MiB  2.53M/s 00:02 [########################] 100%
 alarm                    110.2 KiB   393K/s 00:00 [########################] 100%
 aur is up to date          0.0   B  0.00B/s 00:00 [------------------------]   0%
warning: netctl-1.12-2 is up to date -- reinstalling
resolving dependencies...
looking for conflicting packages...

Packages (1) netctl-1.12-2

Total Download Size:   0.04 MiB
Total Installed Size:  0.18 MiB
Net Upgrade Size:      0.00 MiB

:: Proceed with installation? [Y/n] Y
:: Retrieving packages...
 netctl-1.12-2-any         36.1 KiB   361K/s 00:00 [########################] 100%
(1/1) checking keys in keyring                     [########################] 100%
(1/1) checking package integrity                   [########################] 100%
(1/1) loading package files                        [########################] 100%
(1/1) checking for file conflicts                  [########################] 100%
(1/1) checking available disk space                [########################] 100%
:: Processing package changes...
(1/1) reinstalling netctl                          [########################] 100%
```

### 設定

```netctl``` でネットワークの設定を行う。

#### プロファイルの設定

サンプルプロファイルを用いて、固定IPアドレス設定用のプロファイルを作成する。
なお、このプロファイルにはDNSの設定は行わない。

これはこのプロファイルにDNSの設定を行うと、
```/etc/resolv.conf``` の上書き処理が行われ、空の ```/etc/resolv.conf``` となって
しまうのを回避する為です。


```
# cp -p /etc/netctl/examples/ethernet-static /etc/netctl/eth0
# vi /etc/netctl/eth0

Description='A basic static ethernet connection'
Interface=eth0
Connection=ethernet
IP=static
Address=('192.168.1.2/24')
Gateway='192.168.1.1'
```

```
# netctl enable eth0
# systemctl enable netctl
```

#### 不要サービスの停止

```netctl``` でネットワークサービスを有効にする為、不要なネットワークサービスの
自動起動を無効にする。

```
# systemctl disable dhcpcd.service
# systemctl disable systemd-networkd.service
# systemctl disable systemd-resolved.service
```

#### ```/etc/resolv.conf``` の修正

```/etc/resolv.conf``` のシンボリックリンクを削除して、ファイルを作り直す。

```
# ls -al /etc/resolv.conf
lrwxrwxrwx 1 root root 32 Oct  1 02:23 /etc/resolv.conf -> /run/systemd/resolve/resolv.conf
# rm -i /etc/resolv.conf
rm: remove symbolic link '/etc/resolv.conf'? y
# vim /etc/resolv.conf

nameserver 192.168.1.1
```

#### 名前解決確認

```drill``` コマンドで名前解決可能か確認する。

```
# drill aol.com
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 48505
;; flags: qr rd ra ; QUERY: 1, ANSWER: 5, AUTHORITY: 4, ADDITIONAL: 4
;; QUESTION SECTION:
;; aol.com.    IN    A

;; ANSWER SECTION:
aol.com.    2197    IN    A    207.200.74.38
aol.com.    2197    IN    A    64.12.89.186
aol.com.    2197    IN    A    149.174.107.97
aol.com.    2197    IN    A    64.12.79.57
aol.com.    2197    IN    A    149.174.110.102

;; AUTHORITY SECTION:
aol.com.    661    IN    NS    dns-06.ns.aol.com.
aol.com.    661    IN    NS    dns-01.ns.aol.com.
aol.com.    661    IN    NS    dns-02.ns.aol.com.
aol.com.    661    IN    NS    dns-07.ns.aol.com.

;; ADDITIONAL SECTION:
dns-02.ns.aol.com.    267    IN    A    205.188.157.232
dns-06.ns.aol.com.    1901    IN    A    207.200.73.80
dns-07.ns.aol.com.    267    IN    A    64.236.1.107
dns-01.ns.aol.com.    552    IN    A    64.12.51.132

;; Query time: 14 msec
;; SERVER: 192.168.0.1
;; WHEN: Fri Oct 14 17:30:31 2016
;; MSG SIZE  rcvd: 256
```


### IPv6の無効化

#### IPv6の無効設定

Arch Linux ではIPv6はデフォルトで有効になっている。特に使用しないので無効化する。

```sysctl``` 設定を```/etc/sysctl.d/40-ipv6.conf``` に追加する。

```
# vi /etc/sysctl.d/40-ipv6.conf

# Disable IPv6
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.eth0.disable_ipv6 = 1
```

#### SSHサーバのIPv6無効化

特に無効化しなくても影響はないが不要なので無効化する。

```AddressFamily inet``` に変更する。

```
# vi /etc/ssh/sshd_config

AddressFamily inet
```

#### OS再起動

```reboot``` にてOS再起動し、SSHにて新しく設定したIPアドレスに接続する。

SSH接続を確認後、 ```ip a show``` コマンドで、IPv6のアドレスがないことを確認す
る。

## パスワードの変更

alarmユーザアカウントとrootアカウントのパスワードを```passwd```コマンドで変更する。

## パッケージの更新

パッケージを最新に更新して再起動する。

```
# pacman -Syu
(snip)
# reboot
```


# パッケージのインストール



以下にて好みのパッケージをインストールする。

## vimのインストール

```
# pacman -Sy gvim

:: Synchronizing package databases...
 core                     212.7 KiB   575K/s 00:00 [########################] 100%
 extra                      2.4 MiB   505K/s 00:05 [########################] 100%
 community                  3.9 MiB  1969K/s 00:02 [########################] 100%
 alarm                    110.2 KiB   734K/s 00:00 [########################] 100%
 aur is up to date
resolving dependencies...
:: There are 5 providers available for libgl:
:: Repository extra
   1) mesa-libgl
:: Repository alarm
   2) imx-gpu-viv-dfb  3) imx-gpu-viv-fb  4) imx-gpu-viv-wl  5) imx-gpu-viv-x11

Enter a number (default=1):
looking for conflicting packages...
warning: dependency cycle detected:
warning: harfbuzz will be installed before its freetype2 dependency

Packages (92) adwaita-icon-theme-3.20-2  at-spi2-atk-2.22.0-1
              at-spi2-core-2.22.0-1  atk-2.22+1+gd57f97d-1  avahi-0.6.32-2
              cairo-1.14.6-2  colord-1.3.3-1  compositeproto-0.4.2-3
              damageproto-1.2.1-3  dconf-0.26.0-2  desktop-file-utils-0.23-1
              elfutils-0.167-1  fixesproto-5.0-3  fontconfig-2.12.1-3
              freetype2-2.7-2  gdk-pixbuf2-2.36.0+2+ga7c869a-1
              glib-networking-2.50.0-1  gpm-1.20.7-7  graphite-1:1.3.8-1
              gsettings-desktop-schemas-3.22.0+1+g6f52ab5-1
              gtk-update-icon-cache-3.20.9-1  gtk3-3.20.9-1  harfbuzz-1.3.2-1
              hicolor-icon-theme-0.15-1  inputproto-2.3.2-1  jasper-1.900.2-1
              js17-17.0.0-3  json-glib-1.2.2+4+gd725fb5-1  kbproto-1.0.7-1
              lcms2-2.8-1  libcroco-0.6.11-1  libcups-2.2.1-1  libdaemon-0.14-3
              libdatrie-0.2.10-1  libdrm-2.4.71-1  libepoxy-1.3.1-1
              libgudev-230-1  libgusb-0.2.9-1  libice-1.0.9-1
              libjpeg-turbo-1.5.1-1  libomxil-bellagio-0.9.3-1
              libpciaccess-0.13.4-1  libpng-1.6.25-1  libproxy-0.4.12-2
              librsvg-2:2.40.16-1  libsm-1.2.2-2  libsoup-2.56.0-1
              libthai-0.1.24-1  libtiff-4.0.6-2  libtxc_dxtn-1.0.1-6
              libx11-1.6.4-1  libxau-1.0.8-2  libxcb-1.12-1
              libxcomposite-0.4.4-2  libxcursor-1.1.14-2  libxdamage-1.1.4-2
              libxdmcp-1.1.2-1  libxext-1.3.3-1  libxfixes-5.0.3-1
              libxft-2.3.2-1  libxi-1.7.7-1  libxinerama-1.1.3-2
              libxkbcommon-0.6.1-1  libxml2-2.9.4+4+g3169602-1  libxrandr-1.5.1-1
              libxrender-0.9.10-1  libxshmfence-1.2-1  libxt-1.1.5-1
              libxtst-1.2.3-1  libxxf86vm-1.1.4-1  llvm-libs-3.8.1-1
              mesa-12.0.3-3  mesa-libgl-12.0.3-3  nspr-4.12-1  pango-1.40.3-1
              pixman-0.34.0-1  polkit-0.113-4  randrproto-1.5.0-1
              recordproto-1.14.2-2  renderproto-0.11.1-3  rest-0.8.0-1
              shared-mime-info-1.7-1  vim-runtime-8.0.0013-1  wayland-1.12.0-1
              wayland-protocols-1.7-1  xcb-proto-1.12-2  xextproto-7.3.0-1
              xf86vidmodeproto-2.3.1-3  xineramaproto-1.2.1-3
              xkeyboard-config-2.19-1  xproto-7.0.31-1  gvim-8.0.0013-1

Total Download Size:     9.80 MiB
Total Installed Size:  297.91 MiB

:: Proceed with installation? [Y/n] Y
:: Retrieving packages...
 libx11-1.6.4-1-armv7h   1992.8 KiB  1253K/s 00:02 [########################] 100%
 atk-2.22+1+gd57f97d...   323.1 KiB   873K/s 00:00 [########################] 100%
 libxrender-0.9.10-1...    19.8 KiB  0.00B/s 00:00 [########################] 100%
 harfbuzz-1.3.2-1-armv7h  252.6 KiB   526K/s 00:00 [########################] 100%
 libdrm-2.4.71-1-armv7h   172.3 KiB   539K/s 00:00 [########################] 100%
 libxfixes-5.0.3-1-a...    10.5 KiB  0.00B/s 00:00 [########################] 100%
 mesa-12.0.3-3-armv7h       4.0 MiB   678K/s 00:06 [########################] 100%
 mesa-libgl-12.0.3-3...     4.0 KiB  0.00B/s 00:00 [########################] 100%
 libcups-2.2.1-1-armv7h   262.0 KiB  1008K/s 00:00 [########################] 100%
 libxrandr-1.5.1-1-a...    21.0 KiB  0.00B/s 00:00 [########################] 100%
 libxi-1.7.7-1-armv7h     139.0 KiB   927K/s 00:00 [########################] 100%
 jasper-1.900.2-1-armv7h  133.7 KiB  1215K/s 00:00 [########################] 100%
 gdk-pixbuf2-2.36.0+...   619.2 KiB  1126K/s 00:01 [########################] 100%
 colord-1.3.3-1-armv7h    539.6 KiB  1101K/s 00:00 [########################] 100%
 libxtst-1.2.3-1-armv7h    25.7 KiB  0.00B/s 00:00 [########################] 100%
 at-spi2-core-2.22.0...   209.4 KiB   582K/s 00:00 [########################] 100%
 at-spi2-atk-2.22.0-...    40.6 KiB  0.00B/s 00:00 [########################] 100%
 json-glib-1.2.2+4+g...   174.2 KiB   726K/s 00:00 [########################] 100%
 gsettings-desktop-s...   465.8 KiB   832K/s 00:01 [########################] 100%
 glib-networking-2.5...    81.9 KiB   682K/s 00:00 [########################] 100%
 libsoup-2.56.0-1-armv7h  486.5 KiB   954K/s 00:01 [########################] 100%
(92/92) checking keys in keyring                   [########################] 100%
(92/92) checking package integrity                 [########################] 100%
(92/92) loading package files                      [########################] 100%
(92/92) checking for file conflicts                [########################] 100%
(92/92) checking available disk space              [########################] 100%
:: Processing package changes...
( 1/92) installing vim-runtime                     [########################] 100%
( 2/92) installing gpm                             [########################] 100%
( 3/92) installing xproto                          [########################] 100%
( 4/92) installing libice                          [########################] 100%
( 5/92) installing libsm                           [########################] 100%
( 6/92) installing xcb-proto                       [########################] 100%
( 7/92) installing libxdmcp                        [########################] 100%
( 8/92) installing libxau                          [########################] 100%
( 9/92) installing libxcb                          [########################] 100%
(10/92) installing kbproto                         [########################] 100%
(11/92) installing libx11                          [########################] 100%
(12/92) installing libxt                           [########################] 100%
(13/92) installing atk                             [########################] 100%
(14/92) installing libpng                          [########################] 100%
(15/92) installing renderproto                     [########################] 100%
(16/92) installing libxrender                      [########################] 100%
(17/92) installing xextproto                       [########################] 100%
(18/92) installing libxext                         [########################] 100%
(19/92) installing graphite                        [########################] 100%
(20/92) installing harfbuzz                        [########################] 100%
Optional dependencies for harfbuzz
    cairo: hb-view program [pending]
(21/92) installing freetype2                       [########################] 100%
Optional dependencies for freetype2
    libx11: Some demo programs [installed]
(22/92) installing fontconfig                      [########################] 100%

  Fontconfig configuration is done via /etc/fonts/conf.avail and conf.d.
  Read /etc/fonts/conf.d/README for more information.

  Configuration via /etc/fonts/local.conf is still possible,
  but is no longer recommended for options available in conf.avail.

  Main systemwide configuration should be done by symlinks
  (especially for autohinting, sub-pixel and lcdfilter):

  cd /etc/fonts/conf.d
  ln -s ../conf.avail/XX-foo.conf

  Check also https://wiki.archlinux.org/index.php/Font_Configuration
  and https://wiki.archlinux.org/index.php/Fonts.

updating font cache... done.
(23/92) installing pixman                          [########################] 100%
(24/92) installing libpciaccess                    [########################] 100%
(25/92) installing libdrm                          [########################] 100%
(26/92) installing libxml2                         [########################] 100%
(27/92) installing wayland                         [########################] 100%
(28/92) installing xf86vidmodeproto                [########################] 100%
(29/92) installing libxxf86vm                      [########################] 100%
(30/92) installing fixesproto                      [########################] 100%
(31/92) installing libxfixes                       [########################] 100%
(32/92) installing damageproto                     [########################] 100%
(33/92) installing libxdamage                      [########################] 100%
(34/92) installing libxshmfence                    [########################] 100%
(35/92) installing elfutils                        [########################] 100%
(36/92) installing libomxil-bellagio               [########################] 100%
(37/92) installing libtxc_dxtn                     [########################] 100%
(38/92) installing llvm-libs                       [########################] 100%
(39/92) installing mesa                            [########################] 100%
Optional dependencies for mesa
    opengl-man-pages: for the OpenGL API man pages
    mesa-vdpau: for accelerated video playback
    libva-mesa-driver: for accelerated video playback
(40/92) installing mesa-libgl                      [########################] 100%
(41/92) installing cairo                           [########################] 100%
(42/92) installing libjpeg-turbo                   [########################] 100%
(43/92) installing libtiff                         [########################] 100%
Optional dependencies for libtiff
    freeglut: for using tiffgt
(44/92) installing libdaemon                       [########################] 100%
(45/92) installing avahi                           [########################] 100%
Optional dependencies for avahi
    gtk3: avahi-discover-standalone, bshell, bssh, bvnc [pending]
    gtk2: gtk2 bindings
    qt4: qt4 bindings
    pygtk: avahi-bookmarks, avahi-discover
    python2-twisted: avahi-bookmarks
    mono: mono bindings
    python2-dbus: avahi-discover
    nss-mdns: NSS support for mDNS
(46/92) installing libcups                         [########################] 100%
(47/92) installing libxcursor                      [########################] 100%
Optional dependencies for libxcursor
    gnome-themes-standard: fallback icon theme
(48/92) installing xineramaproto                   [########################] 100%
(49/92) installing libxinerama                     [########################] 100%
(50/92) installing randrproto                      [########################] 100%
(51/92) installing libxrandr                       [########################] 100%
(52/92) installing inputproto                      [########################] 100%
(53/92) installing libxi                           [########################] 100%
(54/92) installing libepoxy                        [########################] 100%
(55/92) installing jasper                          [########################] 100%
Optional dependencies for jasper
    freeglut: for jiv support
    glu: for jiv support
(56/92) installing gdk-pixbuf2                     [########################] 100%
(57/92) installing compositeproto                  [########################] 100%
(58/92) installing libxcomposite                   [########################] 100%
(59/92) installing libdatrie                       [########################] 100%
(60/92) installing libthai                         [########################] 100%
(61/92) installing libxft                          [########################] 100%
(62/92) installing pango                           [########################] 100%
(63/92) installing shared-mime-info                [########################] 100%
(64/92) installing lcms2                           [########################] 100%
(65/92) installing libgusb                         [########################] 100%
(66/92) installing nspr                            [########################] 100%
(67/92) installing js17                            [########################] 100%
(68/92) installing polkit                          [########################] 100%
(69/92) installing dconf                           [########################] 100%
(70/92) installing libgudev                        [########################] 100%
(71/92) installing colord                          [########################] 100%
Optional dependencies for colord
    sane: scanner support
    argyllcms: color profiling
(72/92) installing recordproto                     [########################] 100%
(73/92) installing libxtst                         [########################] 100%
(74/92) installing at-spi2-core                    [########################] 100%
(75/92) installing at-spi2-atk                     [########################] 100%
(76/92) installing xkeyboard-config                [########################] 100%
(77/92) installing libxkbcommon                    [########################] 100%
(78/92) installing hicolor-icon-theme              [########################] 100%
(79/92) installing gtk-update-icon-cache           [########################] 100%
(80/92) installing libcroco                        [########################] 100%
(81/92) installing librsvg                         [########################] 100%
(82/92) installing adwaita-icon-theme              [########################] 100%
(83/92) installing json-glib                       [########################] 100%
(84/92) installing libproxy                        [########################] 100%
Optional dependencies for libproxy
    networkmanager: NetworkManager configuration module
    perl: Perl bindings [installed]
    python2: Python bindings
    glib2: gsettings configuration module [installed]
    js17: PAC proxy support - Mozilla based pacrunner [installed]
    webkitgtk: PAC proxy support - Webkit based pacrunner
(85/92) installing gsettings-desktop-schemas       [########################] 100%
(86/92) installing glib-networking                 [########################] 100%
(87/92) installing libsoup                         [########################] 100%
(88/92) installing rest                            [########################] 100%
(89/92) installing wayland-protocols               [########################] 100%
(90/92) installing desktop-file-utils              [########################] 100%
(91/92) installing gtk3                            [########################] 100%
Optional dependencies for gtk3
    libcanberra: gtk3-widget-factory demo
(92/92) installing gvim                            [########################] 100%
Optional dependencies for gvim
    python2: Python 2 language support
    python: Python 3 language support
    ruby: Ruby language support
    lua: Lua language support
    perl: Perl language support [installed]
    tcl: Tcl language support
:: Running post-transaction hooks...
(1/8) Probing GDK-Pixbuf loader modules...
(2/8) Updating GIO module cache...
(3/8) Compiling GSettings XML schema files...
(4/8) Probing GTK3 input method modules...
(5/8) Updating icon theme caches...
(6/8) Updating the info directory file...
(7/8) Updating the desktop file MIME type cache...
(8/8) Updating the MIME type database...
```

当初以下のエラーが出力されパッケージインストールコマンドを
```pacman -Sy gvim``` に変更した。

```
The requested URL returned error: 404 warning: failed to retrieve some files
```


パッケージインストール後、 ```vim``` コマンドを実行しvimが起動することを確認する。

## tmux のインストール

```pacman``` にてパッケージインストールする。

```
# pacman -Sy tmux

:: Synchronizing package databases...
 core is up to date
 extra is up to date
 community is up to date
 alarm is up to date
 aur is up to date          0.0   B  0.00B/s 00:00 [------------------------]   0%
resolving dependencies...
looking for conflicting packages...

Packages (3) libevent-2.0.22-2  libutempter-1.1.6-2  tmux-2.3-1

Total Download Size:   0.34 MiB
Total Installed Size:  1.36 MiB

:: Proceed with installation? [Y/n] Y
:: Retrieving packages...
 libevent-2.0.22-2-a...   185.3 KiB   299K/s 00:01 [########################] 100%
 libutempter-1.1.6-2...     7.0 KiB  0.00B/s 00:00 [########################] 100%
 tmux-2.3-1-armv7h        155.1 KiB   431K/s 00:00 [########################] 100%
(3/3) checking keys in keyring                     [########################] 100%
(3/3) checking package integrity                   [########################] 100%
(3/3) loading package files                        [########################] 100%
(3/3) checking for file conflicts                  [########################] 100%
(3/3) checking available disk space                [########################] 100%
:: Processing package changes...
(1/3) installing libevent                          [########################] 100%
Optional dependencies for libevent
    python2: to use event_rpcgen.py
(2/3) installing libutempter                       [########################] 100%
(3/3) installing tmux                              [########################] 100%
```

## sudo のインストール

### インストール

```pacman``` にてパッケージインストールする。


```
# pacman -Sy sudo
:: Synchronizing package databases...
 core is up to date
 extra is up to date
 community is up to date
 alarm is up to date
 aur is up to date          0.0   B  0.00B/s 00:00 [------------------------]   0%
resolving dependencies...
looking for conflicting packages...

Packages (1) sudo-1.8.18-1

Total Download Size:   0.89 MiB
Total Installed Size:  4.08 MiB

:: Proceed with installation? [Y/n] y
:: Retrieving packages...
 sudo-1.8.18-1-armv7h     906.3 KiB   271K/s 00:03 [########################] 100%
(1/1) checking keys in keyring                     [########################] 100%
(1/1) checking package integrity                   [########################] 100%
(1/1) loading package files                        [########################] 100%
(1/1) checking for file conflicts                  [########################] 100%
(1/1) checking available disk space                [########################] 100%
:: Processing package changes...
(1/1) installing sudo                              [########################] 100%
```

### 設定

以下のコマンドを実行して、ユーザー USER_NAME が ```sudo``` で完全な root 権限を与える。

```
# visudo

USER_NAME ALL=(ALL) ALL
```

```/etc/pam.d/su``` と ```/etc/pam.d/su-l``` にある次の行をアンコメントして wheel グループのユーザ以外、 ```su``` 出来なくする。

```
auth required pam_wheel.so use_uid
```


# 参考文献

- [インストールガイド - ArchWiki](https://wiki.archlinuxjp.org/index.php/インストールガイド)
- [netctl - ArchWiki](https://wiki.archlinuxjp.org/index.php/Netctl)
- [resolv.conf - ArchWiki](https://wiki.archlinuxjp.org/index.php/Resolv.conf)
- [IPv6 - ArchWiki](https://wiki.archlinuxjp.org/index.php/IPv6)
- [pacman - ArchWiki](https://wiki.archlinuxjp.org/index.php/Pacman)
- [Vim - ArchWiki](https://wiki.archlinuxjp.org/index.php/Vim)
- [Secure Shell - ArchWiki](https://wiki.archlinuxjp.org/index.php/Secure_Shell)
- [Sudo - ArchWiki](https://wiki.archlinuxjp.org/index.php/Sudo)
- [su - ArchWiki](https://wiki.archlinuxjp.org/index.php/Su)
