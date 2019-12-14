Title: Arch Linux ARM on Nanopc t4
Date: 2019-12-14 20:55
Modified: 2019-12-14 22:00
Category: Kubernetes
Tags: Kubernetes, arm, single board computer, Nanopc T4, Rockchip RK3399, eMMC
Author: Hideo Suzuki
Summary: Cephクラスタ用に用意したFriendryElecのNanopc T4にArch Linux ARMをインストールする。Nanopc T4はM.2スロットがあり、M.2 SSDを搭載可能なのでこれでCephクラスタを構築します。今回はこのNanopc T4のeMMCにArch Linux ARMをインストールする手順について記載します。

[TOC]

## Summary
Cephクラスタ用に用意したFriendryElecのNanopc T4にArch Linux ARMをインストールする。Nanopc T4はM.2スロットがあり、M.2 SSDを搭載可能なのでこれでCephクラスタを構築します。今回はこのNanopc T4のeMMCにArch Linux ARMをインストールする手順について記載します。

## Install process

- この記事でのインストールプロセスは、Arch Linux ARMから起動するマイクロSDカードを作成し、そのマイクロSDカードで起動してeMMCにインストールします。
- マイクロSDカードの作成は、Archlinux on Rasberry pi 3bにて実施
- 作成したマイクロSDカードを使ってNanopc T4を起動しeMMCにArch Linux ARMをインストール


## Process details

以下の手順をマイクロSDとeMMCへのインストールの為、都合2回ずつ実施する。

### Preparation

事前準備として、Nanopc T4用のu-bootのコンパイルを行い、boot.scr, idbloader.img, uboot.img及びtrust.imgを作成します。

1. sudoパッケージのインストールと設定

    SeeAlso: 

    [https://lupinthe14th.github.io/arch-linux-arm-on-rasberry-pi2-nochu-qi-she-ding.html#sudo](https://lupinthe14th.github.io/arch-linux-arm-on-rasberry-pi2-nochu-qi-she-ding.html#sudo)

1. ホームディレクトリにbuildディレクトリを作成

        cd ~/      
        mkdir build
        cd build/

1. aspパッケージとbase-develパッケージグループをインストール

        sudo pacman -Sy asp base-devel

1. カーネルパッケージファイルの取得

    カスタマイズの起点となる綺麗なカーネルが必要になるのでABSからカーネルパッケージファイルを取得する

        ASPROOT=. asp checkout linux

1. PKGBUILDファイルのダウンロード

    [https://github.com/archlinuxarm/PKGBUILDs/pull/1728/files](https://github.com/archlinuxarm/PKGBUILDs/pull/1728/files) からPKGBUILDファイルをダウンロードする。ちなみにこのPRはArch Arch Linux ARMのメンバーからNot a supported system.でマージされずにクローズされています。

        curl -LO https://raw.githubusercontent.com/a-andre/PKGBUILDs/fc0c326d9fbf72a0b5c7280d46d95f397eab9cf4/alarm/uboot-nanopct4/PKGBUILD
        curl -LO https://raw.githubusercontent.com/a-andre/PKGBUILDs/fc0c326d9fbf72a0b5c7280d46d95f397eab9cf4/alarm/uboot-nanopct4/uboot-nanopct4.install
        curl -LO https://raw.githubusercontent.com/a-andre/PKGBUILDs/fc0c326d9fbf72a0b5c7280d46d95f397eab9cf4/alarm/uboot-nanopct4/rk3399trust.ini
        curl -LO https://raw.githubusercontent.com/a-andre/PKGBUILDs/fc0c326d9fbf72a0b5c7280d46d95f397eab9cf4/alarm/uboot-nanopct4/boot.txt
        curl -LO https://raw.githubusercontent.com/a-andre/PKGBUILDs/fc0c326d9fbf72a0b5c7280d46d95f397eab9cf4/alarm/uboot-nanopct4/mkscr

1. コンパイル

        makepkg -s

### Install to a micro SD card or eMMC

1. デバイスの初期化

    デバイス名は適宜変更してください。

        sudo dd if=/dev/zero of=/dev/sdX bs=1M count=32

1. デバイスのパーティショニング

        (echo g; echo p; echo n; echo 1; echo 32768; echo ""; echo w; echo q) | sudo fdisk /dev/sdX

1. デバイスにファイルシステムを作成

        sudo mkfs.ext4 /dev/sdX1

1. デバイスのファイルシステムのマウント

        mkdir root
        sudo mount /dev/sdX1 root

1. ダウンロードとルートファイルシステムへの拡張

    sudo経由でなく必ずrootユーザにスイッチして実行してください。

        su root
        curl -LO http://os.archlinuxarm.org/os/ArchLinuxARM-aarch64-latest.tar.gz
        bsdtar -xpf ArchLinuxARM-aarch64-latest.tar.gz -C root

1. boot.scrスクリプトの配置

    事前準備にて作成したU-Boot用のboot.scrスクリプトを/ bootディレクトリに配置します。

        cp pkg/uboot-nanopct4/boot/boot.scr root/boot/boot.scr

1. デバイスファイルのアンマウント

        umount root

1. U-Boot ブートローダーのインストール

        cd pkg/uboot-nanopct4/boot/
        sudo dd if=idbloader.img of=/dev/sdX seek=64 conv=notrunc
        sudo dd if=uboot.img of=/dev/sdX seek=16384 conv=notrunc
        sudo dd if=trust.img of=/dev/sdX seek=24576 conv=notrunc

1. 作成したデバイスから起動させる
    1. micro SDカードの場合
        1. デバイスをeject

                sudo eject /dev/sdX

        2. Nanopc T4のmicro SDカードスロットにmicro Sdカードを挿入
        3. 電源ON
            1. PWR LEDが点灯するのを確かめる
            1. 3分程度待ち、STAT LEDが点滅するのを確かめる
            1. LinkUpすることを確かめる
        4. SSHログイン

    1. eMMCの場合
        1. 電源OFF

                sudo poweroff

        1. micro SDカードを抜く
        1. 電源ON
            1. PWR LEDが点灯するのを確かめる
            1. 3分程度待ち、STAT LEDが点滅するのを確かめる
            1. LinkUpすることを確かめる
        1. SSHログイン

1. 初期設定
    1. pacmanキーリングを初期化し、Arch Linux ARMパッケージの署名キーを追加

            su
            pacman-key --init
            pacman-key --populate archlinuxarm

    1. パッケージの更新など適宜実施

## Refarence

- [Rock64 | Arch Linux ARM](https://archlinuxarm.org/platforms/armv8/rockchip/rock64)
- [Support for Nanopc t4](https://archlinuxarm.org/forum/viewtopic.php?f=67&t=13763&p=61487&hilit=NanoPC+T4#p61487)
- [カーネル/コンパイル/Arch Build System](https://wiki.archlinux.jp/index.php/カーネル/コンパイル/Arch_Build_System)
- [add alarm/uboot-nanopct4 by a-andre · Pull Request #1728 · archlinuxarm/PKGBUILDs](https://github.com/archlinuxarm/PKGBUILDs/pull/1728/files)
