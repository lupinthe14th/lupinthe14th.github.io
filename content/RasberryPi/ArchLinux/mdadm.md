Title: Rasberry Pi2 の ルートファイルシステムを HDD 化（ついでにRAID1 化）
Date: 2016-01-14 15:00
Modified: 2016-01-14 15:00
Category: Rasberry Pi
Tags: raid, raid1, mdadm, USB-HDD, Rasberry Pi2
Slug: USB-HDD boot
Author: Hideo Suzuki
Summary: Rasberry Pi2 のルートファイルシステムを、USB-HDD にする。ついでに、mdadm で、RAID1 構成にして、データ保存の冗長化を行う。

# 目的

1. ルートファイルシステムの USB-HDD 化

    Raserry Pi2 のディスクは、SDメモリカード。これは消去・書き込み可能回数が
    限られている。
    そこで、ルートファイルシステムを USB-HDD にすることにより、
    消去・ 書き込み可能回数制限の制約を無くす。[^1]

1. RAID1 によるデータ保存の冗長化

    USB-HDD を 冗長可能な構成にすることにより、データ保存の冗長化を図る。

    なお調達の都合上、最初はUSB-HDD 一つでディグレード(片肺運転)のRAID構成を作成
    する。


# Install 手順

## 前提条件

以下に作業の前提条件を記載する。

1. Rasberry Pi2 のSDメモリカード boot 済み

    [ARM/RaspberryPi - Ubuntu Wiki](https://wiki.ubuntu.com/ARM/RaspberryPi) 
    でSDメモリカードを作成し、Rasberry Pi2 で起動済み。

1. クライアント

    Mac OS X El Capitan (version 10.11.2) で作業



## mdadm の Install

以下のコマンドをターミナルで実行する。

なお、途中で、postfix の設定画面が表示されるが、設定なしで抜ける。

```console
$ sudo -i
# apt-get install -y mdadm
```

## USB-HDD の構成

USB-HDD の構成を確認し、パーティションを再作成する。

### 現状の確認

`fdisk` コマンドで、USB-HDD の現状の構成を確認する。

```console
# fdisk -l

Disk /dev/mmcblk0: 15.8 GB, 15804137472 bytes
ヘッド 4, セクタ 16, シリンダ 482304, 合計 30867456 セクタ
Units = セクタ数 of 1 * 512 = 512 バイト
セクタサイズ (論理 / 物理): 512 バイト / 512 バイト
I/O サイズ (最小 / 推奨): 512 バイト / 512 バイト
ディスク識別子: 0x00000000

  デバイス ブート      始点        終点     ブロック   Id  システム
/dev/mmcblk0p1   *        2048      133119       65536    c  W95 FAT32 (LBA)
/dev/mmcblk0p2          133120    30867455    15367168   83  Linux

Disk /dev/sda: 500.1 GB, 500107862016 bytes
ヘッド 81, セクタ 63, シリンダ 191411, 合計 976773168 セクタ
Units = セクタ数 of 1 * 512 = 512 バイト
セクタサイズ (論理 / 物理): 512 バイト / 512 バイト
I/O サイズ (最小 / 推奨): 512 バイト / 512 バイト
ディスク識別子: 0x75ee47c1

デバイス ブート      始点        終点     ブロック   Id  システム
/dev/sda1            2048   976773167   488385560   83  Linux
```

```console
# df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/root       15100208 2903300  11550832  21% /
devtmpfs          468772       4    468768   1% /dev
none                   4       0         4   0% /sys/fs/cgroup
none               94612     292     94320   1% /run
none                5120       0      5120   0% /run/lock
none              473052       0    473052   0% /run/shm
none              102400       0    102400   0% /run/user
/dev/mmcblk0p1     65390   20334     45056  32% /boot/firmware
```

### パーティションの再作成

`fdisk` コマンドで、パーテーションを一度削除してパーテーションを新規作成し
パーテーションタイプをRAID 自動認識:0xfdに書き換える。

```console
# fdisk /dev/sda

d コマンドで削除
n　コマンドで
p プライマリパーテーションを　全領域に設定
t コマンド　パーテーション　タイプは0xfd RAID auto
p コマンドで確認後
w コマンドで書き込み終了
```

新規に作成したパーテーションテーブルを再起動せずに更新する。

```console
# partprobe
```


## RAID デバイスの作成

USB-HDD 一つでディグレード(片肺運転)のRAIDデバイスを作成する。

### RAID デバイスの作成

以下のコマンドを実行し、RAIDデバイスを作成する。


```console
# mdadm -C /dev/md0 -l1 -n2 missing /dev/sda1
```

### RAID デバイスの確認

以下のコマンドで、作成したRAIDデバイスの状態を確認する。

```console
# cat /proc/mdstat
Personalities : [raid1]
md0 : active raid1 sda1[1]
      488254336 blocks super 1.2 [2/1] [_U]

unused devices: <none>
```

### ファイルシステムの作成

作成したRAIDデバイスにファイルシステムを作成する。

```console
# mkfs /dev/md0 -t ext4
mke2fs 1.42.9 (4-Feb-2014)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
30523392 inodes, 122063584 blocks
6103179 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=0
3726 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
        4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968,
        102400000

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

#
```


### mdadm 設定ファイルへ反映

作成したRAIDデバイスを `mdadm.conf` に反映する。

```console
# mdadm -D -s
ARRAY /dev/md0 metadata=1.2 name=ubuntu:0 UUID=243a78c7:63ef7642:af4a8dfe:5f1bc4ca
```

```console
# cat /etc/mdadm/mdadm.conf
# mdadm.conf
#
# Please refer to mdadm.conf(5) for information about this file.
#

# by default (built-in), scan all partitions (/proc/partitions) and all
# containers for MD superblocks. alternatively, specify devices to scan, using
# wildcards if desired.
#DEVICE partitions containers

# auto-create devices with Debian standard permissions
CREATE owner=root group=disk mode=0660 auto=yes

# automatically tag new arrays as belonging to the local system
HOMEHOST <system>

# instruct the monitoring daemon where to send mail alerts
MAILADDR root

# definitions of existing MD arrays
ARRAY /dev/md0 metadata=1.2 name=ubuntu:0 UUID=243a78c7:63ef7642:af4a8dfe:5f1bc4ca

# This file was auto-generated on Thu, 14 Jan 2016 16:50:47 +0900
# by mkconf $Id$
```

### mdadm 詳細確認

以下のコマンドを実行し、作成したRAIDデバイスの詳細を確認する。


```console
# mdadm --detail /dev/md0
/dev/md0:
        Version : 1.2
  Creation Time : Thu Jan 14 17:07:36 2016
     Raid Level : raid1
     Array Size : 488254336 (465.64 GiB 499.97 GB)
  Used Dev Size : 488254336 (465.64 GiB 499.97 GB)
   Raid Devices : 2
  Total Devices : 1
    Persistence : Superblock is persistent

    Update Time : Thu Jan 14 17:15:21 2016
          State : clean, degraded
 Active Devices : 1
Working Devices : 1
 Failed Devices : 0
  Spare Devices : 0

           Name : ubuntu:0  (local to host ubuntu)
           UUID : 243a78c7:63ef7642:af4a8dfe:5f1bc4ca
         Events : 2

    Number   Major   Minor   RaidDevice State
       0       0        0        0      removed
       1       8        1        1      active sync   /dev/sda1
```

## ルートファイルシステムの変更

以下の作業を行いルートファイルシステムをUSB-HDD に作成したRAIDデバイスに変更する。

### マウントするデバイスの変更

ルートファイルシステムとしてUSB-HDDのRAIDデバイスを使うように /etc/fstab を修正する。

まず、UUIDを調べる。[^2]

```console
# blkid
/dev/mmcblk0p1: SEC_TYPE="msdos" UUID="AB3E-B34D" TYPE="vfat"
/dev/mmcblk0p2: UUID="3aee2e0f-21f9-43c8-a4d3-e864f5d72d37" TYPE="ext4"
/dev/sda1: UUID="243a78c7-63ef-7642-af4a-8dfe5f1bc4ca" UUID_SUB="c7d6abc9-e769-f9c2-2800-23713e71baed" LABEL="ubuntu:0" TYPE="linux_raid_member"
/dev/md0: UUID="1e34d0a9-5481-48c1-a51e-3b1e2230b0c5" TYPE="ext4"
```

`/etc/fstab` を編集する。編集後は以下の通り。

```console
# cat /etc/fstab
proc            /proc           proc    defaults          0       0
#/dev/mmcblk0p2  /               ext4    defaults,noatime  0       1
UUID=1e34d0a9-5481-48c1-a51e-3b1e2230b0c5 /  ext4 defaults,noatime 0 1
/dev/mmcblk0p1  /boot/firmware  vfat    defaults          0       2
# a swapfile is not a swap partition, no line here
#   use  dphys-swapfile swap[on|off]  for that
```

### 起動ファイルシステムの指定の変更

`/boot/cmdline.txt` には起動時のルートファイルシステムとして SDカードの領域を
指定されている。
これをUSB-HDDのRAIDデバイスに変更する。

```console
# cp /boot/cmdline.txt /boot/cmdline.txt.org
# cat /boot/cmdline.txt
dwc_otg.lpm_enable=0 console=tty1 root=UUID=1e34d0a9-5481-48c1-a51e-3b1e2230b0c5 rootfstype=ext4 elevator=deadline rootwait rootdelay=5
```

### ルートファイルシステムのコピー

作成したRAIDデバイスのファイルシステムに、ルートファイルシステムの内容をコピーする。


```console
# mount /dev/md0 /mnt
# cd /mnt
# cp -ax / .
```



# 参考資料

- [RASPBERRY PI RAID ARRAY WITH USB HDDS](http://projpi.com/diy-home-projects-with-a-raspberry-pi/raspberry-pi-raid-array-with-usb-hdds/)
- [RAID1 によるraspberry pi のデータ保存の冗長化 Raspberry PI model B+](http://www.palm-dreams.com/blog/?p=829)
- [Raspberry Pi メモ (44) ハードディスク起動とヘアピンNAT](http://www.mztn.org/rpi/rpi44.html)

[^1]: USB-HDD で、USB2.0接続なので速度は落ちる。
[^2]: USB-HDD なので、接続を変更するとデバイス名が変更となる場合があるのでUUIDを利用する。


