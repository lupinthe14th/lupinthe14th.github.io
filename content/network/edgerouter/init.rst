EdgeRouter X 
################################################################################

:Date: 2016-11-11 00:00
:Modified: 2016-11-11 00:00
:Category: network
:Tags: network, Edge Router X,
:Author: Hideo Suzuki
:Summary: `EdgeRouter X がすごい <http://yabe.jp/gadgets/edgerouter-x/>`_ の記事
          を見つけてちょうど欲しいと思っていたのとマッチングしたので購入してみま
          した。
:Status: Draft

購入情報
================================================================================


参考にした `EdgeRouter X がすごい <http://yabe.jp/gadgets/edgerouter-x/>`_ では、`Ubiquiti Networks ER-X EdgeRouter X B&H Photo Video <https://www.bhphotovideo.com/c/product/1139738-REG/ubiquiti_networks_er_x_edgerouter_x_5_port_single.html>`_ が評判とありましたが、**Ships to USA only** なので日本への配送はしてくれないようなので、色々Twitterとかで検索したところ、ebayが良さそうだったので物は試しにebayで購入。

:ITEM PRICE: JPY 5,926.97
:SHIPPING PRICE: JPY 2,154.41
:TOTAL PRICE: JPY 8,081.38
:ORDER DATE: Oct 17, 2016
:DELIVERY DATE: Nov 06, 2016

支払いはPayPalを利用。実際の為替レートで、JPY 8,371 で約３週間かかりましたが、無事到着しました。

初期設定
================================================================================

早速開封。気にしていたコンセントも日本で使える物で安心。

`EdgeRouter X – 1. 初期設定 <http://yabe.jp/gadgets/edgerouter-x-01-set-up/>`_
を参考に初期設定を進めます。

上記以外で変更した部分は以下の通り。

#. ファームウェアのアップデート

   開封して、電源を入れて管理画面を表示したところ、ファームウェアのバージョンが、
   1.7.1でした。

   以下の手順でファームウェアを最新の1.9.0にします。

   #. `Ubiquiti Networks - Downloads <https://www.ubnt.com/download/edgemax/edgerouter-x>`_ からファームウェアをダウンロード

   #. 管理画面の下のSystem --> Upgrade System Image で、ダウンロードしたファイル
      をアップロード

   #. ポップアップ画面の指示に従い再起動



#. 証明書を常に信頼する

   Safariでアクセスすると、証明書の警告画面が表示されます。
   ここで、証明書を表示して、証明書を常に信頼するにチェックを入れます。
   
   入れないと、WebSocket Error が表示され、操作できません。



#. DHCP Server設定でレンジの設定

   LANに作成したネットワークでDHCPに割り当てるレンジを設定。

   そんなにDHCP割当対象の端末があるわけではないですが、第４オクテットを64-127で割当。




.. list-table:: ER-X 設定値
   :stub-columns: 1

   * - ER-X ファームウェア
     - 1.7.1

