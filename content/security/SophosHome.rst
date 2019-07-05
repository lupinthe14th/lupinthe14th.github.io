:Title: Sophos home 使ってみる
:Date: 2016-07-01 00:00
:Modified: 2016-07-01 00:00
:Category: security
:Tags: Sophos, Anti-virus, malware, Web Protection, Web Category Access
:Slug: SophosHome
:Author: Hideo Suzuki
:Summary: 最近ランサムウェアの情報が飛び交ってきているのでお試ししてみました。

はじめに
===============================================================================

最近ランサムウェアの情報が飛び交ってきているので気になっていろいろ調べたら
ちょっと面白そうなSophos Home for PCs and Macsを試してみます。

なぜ興味を持った？
===============================================================================

一番興味を持ったのはSophos XG Firewall Home Edition。 [#f1]_

これを自宅に構築してみようと思ったけど、この機能でSecurity Heartbeat™なんてのが
あるじゃないですか。
じゃ、手始めにエンドポイントのお試ししてみようと思ったわけです。


ダウンロード
===============================================================================


#. アカウントの作成

   `ここ <https://www.sophos.com/ja-jp/lp/sophos-home.aspx>`_ のダウンロードボタン
   をクリックします。
   すると、アカウント作成の画面になるので名前とE-mailアドレス、パスワードを入力して
   アカウントを作成します。（ダウンロードじゃないじゃん。）

#. E-Mail認証からのログイン

   登録したメールアドレスにメールが届きますので、Confirm Emailします。ログインの
   リンクを押してログイン画面を表示してE-mailとパスワードを入力してログインしま
   す。

#. やっとダウンロード

   Add Device -> Install で、インストールできます。

早速試してみます
===============================================================================

早速機能を試しました。ざっくり一通り確認しただけなのでこれからちょっと利用し続け
てみます。

- ウイルススキャン

  フルスキャン試してます。Mac book Air OS X EL Capitan 1.6 GHz ( GB 1600 MHz
  DDR3 ですが、２時間ほど経過して75％ぐらいまで終わりました。

- ウイルスダウンロード

  `テストウイルス EICAR <http://files.trendmicro.com/products/eicar-file/eicar.com>`_ をダウンロードしようとするときっちりブロックしてくれます。（当たり前だけどちょっと感動）

- マルウェア

  `The Anti-Malware Testfile <http://www.eicar.org/86-0-Intended-use.html>`_ の
  68byteの文字列を適当な名前のファイルで作成します。するときっちり削除してくれま
  す。（これにも当たり前だけど感動）

- Web フィルタ

  カテゴリ毎にAllow, Warn, Blockが選択できます。この制御はクラウドにある
  ダッシュボードでデバイス毎に制御が可能です。子供向けに見せたくないカテゴリを
  Blockとかできますね。

  Warnだと一旦警告画面が表示されて前画面に戻るかページを表示するか決めることがで
  きるようです。



.. rubric:: Footnotes

.. [#f1] `Sophos XG Firewall Home Edition <https://www.sophos.com/ja-jp/products/free-tools/sophos-xg-firewall-home-edition.aspx>`_
