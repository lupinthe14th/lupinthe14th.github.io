Title: ext4 root パーティションのサイズを変更する方法
Date: 2019-10-18 12:00
Modified: 2019-10-18 12:00
Category: memo
Tags: aws, archlinux, ext4, fdisk, growpart, resize2fs
Author: Hideo Suzuki
Summary: awsで運用しているArchlinuxサーバのルートパーティションが100%近くなってきたのでディスクサイズの拡張を行った際のメモ

# 要件
- なるべく簡単
- なるべくサーバ再起動なし

   - 今回の手順ではサーバ再起動が必要となった

# 手順

1. 作業前状態

    ```console
    # df -h
    ファイルシス   サイズ  使用  残り 使用% マウント位置
    dev              992M     0  992M    0% /dev
    run             1000M  436K 1000M    1% /run
    /dev/xvda1        16G   15G  211M   99% /
    tmpfs           1000M  4.0K 1000M    1% /dev/shm
    tmpfs           1000M     0 1000M    0% /sys/fs/cgroup
    tmpfs           1000M  1.1M  999M    1% /tmp
    tmpfs            200M     0  200M    0% /run/user/0
    ```

    ```console
    # lsblk
    NAME    MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
    xvda    202:0    0  32G  0 disk 
    └─xvda1 202:1    0  16G  0 part /
    ```

1. EBSボリュームの変更

    [Elastic Volumes を使用して EBS ボリュームを変更する (コンソール)](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/requesting-ebs-volume-modifications.html#modify-ebs-volume) を参考にサイズ変更のみ実施。

1. `resize2fs` で拡張（失敗）

    ```console
    # resize2fs /dev/xvda1
    resize2fs 1.43.4 (31-Jan-2017)
    The filesystem is already 4194048 (4k) blocks long.  Nothing to do!
    ```

    簡単に `resize2fs` コマンド一発では拡張出来なかった。

    調べたら、[オンラインでEC2のルートディスクを拡張する](https://qiita.com/ikeisuke/items/125ed240c3881036a287) 同じようなメッセージが出力されている記事を発見したので、`growpart` コマンドでパーティションを拡張してみます。 [^1]

1. `growpart` でパーティションを拡張

    ```console
    # growpart /dev/xvda 1
    NOCHANGE: partition 1 could only be grown by -32125898 [fudge=20480]
    ```

    あら。拡張出来ないみたい。いろいろ調べたけど `fdisk` なりで手動でパーティションを拡張するしかなさそう。


1. EBSボリュームのスナップショット作成

    [Amazon EBS スナップショットの作成](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/ebs-creating-snapshot.html) を参考にスナップショットを作成。

1. `fdisk` でパーティションを拡張

    ```console
    # fdisk /dev/xvda
 
    fdisk (util-linux 2.29.2) へようこそ。
    ここで設定した内容は、書き込みコマンドを実行するまでメモリのみに保持されます。
    書き込みコマンドを使用する際は、注意して実行してください。
 
 
    コマンド (m でヘルプ): p
    ディスク /dev/xvda: 32 GiB, 34359738368 バイト, 67108864 セクタ
    単位: セクタ (1 * 512 = 512 バイト)
    セクタサイズ (論理 / 物理): 512 バイト / 512 バイト
    I/O サイズ (最小 / 推奨): 512 バイト / 512 バイト
    ディスクラベルのタイプ: dos
    ディスク識別子: 0xfd1cae39
 
    デバイス   起動 開始位置 最後から   セクタ サイズ Id タイプ
    /dev/xvda1          2048 33554431 33552384    16G 83 Linux
 
    コマンド (m でヘルプ): d
    パーティション 1 を選択
    パーティション 1 を削除しました。
 
    コマンド (m でヘルプ): n
    パーティションタイプ
       p   基本パーティション (0 プライマリ, 0 拡張, 4 空き)
          e   拡張領域 (論理パーティションが入ります)
 	 選択 (既定値 p): p
 	 パーティション番号 (1-4, 既定値 1): 1
 	 最初のセクタ (2048-67108863, 既定値 2048): 2048
 	 最終セクタ, +セクタ番号 または +サイズ{K,M,G,T,P} (2048-67108863, 既定値 67108863): 
 
 	 新しいパーティション 1 をタイプ Linux、サイズ 32 GiB で作成しました。
 	 Partition #1 contains a ext4 signature.
 
 	 Do you want to remove the signature? [Y]es/[N]o: N
 
 	 コマンド (m でヘルプ): a
 
 	 パーティション 1 を選択
 	 パーティション 1 の起動フラグを有効にしました。
 
 	 コマンド (m でヘルプ): p
 	 ディスク /dev/xvda: 32 GiB, 34359738368 バイト, 67108864 セクタ
 	 単位: セクタ (1 * 512 = 512 バイト)
 	 セクタサイズ (論理 / 物理): 512 バイト / 512 バイト
 	 I/O サイズ (最小 / 推奨): 512 バイト / 512 バイト
 	 ディスクラベルのタイプ: dos
 	 ディスク識別子: 0xfd1cae39
 
 	 デバイス   起動 開始位置 最後から   セクタ サイズ Id タイプ
 	 /dev/xvda1 *        2048 67108863 67106816    32G 83 Linux
 
 	 コマンド (m でヘルプ): w
 	 パーティション情報が変更されました。
 	 ioctl() を呼び出してパーティション情報を再読み込みします。
 	 パーティション情報の再読み込みに失敗しました。: デバイスもしくはリソースがビジー状態です
 
 	 カーネルは古い情報を使用しています。新しい情報を利用するには、システムを再起動するか、もしくは partprobe(8) または kpartx(8) を実行してください。
    ```
 
    `partprobe` か `kpartx` を使えばサーバ再起動する必要なさそうでしたが、調査の過程でサーバー再起動していたので今回はサーバ再起動します。
 
    リブートプロセスで強制的に `fsck` を実行させるため以下コマンドを実行します。
 
 
    ```console
    # touch /forcefsck
    ```
 
    ```console
    # reboot
    ```

1. `resize2fs` でファイルシステムの拡張

    `reboot` 後、`resize2fs` コマンドでファイルシステムを拡張する。
 
    ```console
    # resize2fs /dev/xvda1
    resize2fs 1.43.4 (31-Jan-2017)
    Filesystem at /dev/xvda1 is mounted on /; on-line resizing required
    old_desc_blocks = 2, new_desc_blocks = 4
    The filesystem on /dev/xvda1 is now 8388352 (4k) blocks long.
 
    ```
 
    ```console
    # df -h
    ファイルシス   サイズ  使用  残り 使用% マウント位置
    dev              992M     0  992M    0% /dev
    run             1000M  444K 1000M    1% /run
    /dev/xvda1        32G   15G   16G   50% /
    tmpfs           1000M  4.0K 1000M    1% /dev/shm
    tmpfs           1000M     0 1000M    0% /sys/fs/cgroup
    tmpfs           1000M   12K 1000M    1% /tmp
    tmpfs            200M     0  200M    0% /run/user/0
    ```
 
    無事ファイルシステムの拡張が完了。作成したスナップショットは必要に応じて削除ください。


# 参考資料

- [How to resize ext4 root partition live without umount on Linux](https://linuxconfig.org/how-to-resize-ext4-root-partition-live-without-Aumount)
- [Elastic Volumes を使用して EBS ボリュームを変更する (コンソール)](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/requesting-ebs-volume-modifications.html#modify-ebs-volume)
- [ボリュームサイズ変更後の Linux ファイルシステムの拡張](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html#extend-linux-volume-partition)
- [オンラインでEC2のルートディスクを拡張する](https://qiita.com/ikeisuke/items/125ed240c3881036a287)

[^1]: 後で確認したら、AWSのドキュメント [パーティションの拡張 (必要な場合)](https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html#extend-linux-volume-partition) に記載がありますね
