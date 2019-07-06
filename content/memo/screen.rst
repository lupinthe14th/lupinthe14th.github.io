Macでシリアル接続
################################################################################

:Date: 2016-10-11 00:00
:Modified: 2016-10-11 00:00
:Category: memo
:Tags: Mac OS X, シリアル, USBシリアルケーブル, Console, memo
:Author: Hideo Suzuki
:Summary: Mac OS Xからコンソール接続するときの方法をすぐ忘れるのでメモ。

接続方法
===============================================================================

#. デバイスの確認

   .. code-block:: console
   
      % ls /dev/tty.usb*
      /dev/tty.usbserial-FTK1SOHS
   

#. 接続

   .. code-block:: console

      % screen /dev/tty.usbserial-FTK1SOHS

#. 切断

   `Control-a k` で、 `Really kill this window [y/n]` と表示されるので、 y を押して
   screen を終了する。

参考資料
===============================================================================

- `Mac の screen コマンドでシリアル通信 <http://qiita.com/hideyuki/items/9258f33180d98ad0cb1e>`_
