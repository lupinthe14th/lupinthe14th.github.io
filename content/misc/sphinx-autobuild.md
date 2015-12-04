Title: sphinx-autobuild によるドキュメントのリビルド
Date: 2015-12-04 18:00
Modified: 2015-12-04 18:00
Category: misc
Tags: Sphinx, Mac,
Slug: sphinx-autobuild
Author: Hideo Suzuki
Summary: Sphinx を用いたドキュメント作成でのローカル確認に便利なsphinx-autobuildについて

# はじめに

日々の作業記録として自分向け日報を Sphinx を用いて作成している。この時、ローカル
環境で確認する手段として、`watch` コマンドを用いて `make html` を実行させるよう
にし、生成されたhtml ファイルを直接ブラウザで開いて確認していた。

そんな中、ふと技術系ブログをみていたら、`sphinx-autobuild` なるツールが存在する
ことを知りものは試しに導入してみた。

# 目的

確認したい時に最新のドキュメントが確認出来る。

この目的を満たすだけなら、`watch make html` でも十分なのですが、なんとなくド
キュメント更新していないのに、コマンドが実行されるのがエコじゃないと思っていたの
もあります。

# 手順

## 前提条件

この手順は、Mac OS X Yosemite の場合についてです。
なお、Python の Virtualenvwrapper で、Sphinx の専用環境を作成しています。

## sphinx-autobuild のインストール

以下コマンドを実行します。なお、Python の Virtualenvwrapper で、Sphinx の専用環
境を作成しています。

```console
% workon report
% pip install sphinx-autobuild
```

## sphinx-autobuild の使い方

```console
sphinx-autobuild <ソースディレクトリ> <ビルド成果物出力ディレクトリ>
```

ツールの公式ドキュメントには、Makefile に、コマンドを追加する例もあるようです。

# 所感

`watch make html` で、ファイルの出力先をブラウザで表示しているのと、ローカルhttp
サーバーを起動したままなのはどちらがエコなのかは、考えないことにしよう。

# 参考資料

- [sphinx-autobuildで再ビルド、ブラウザの再リロードの手間を省いてSphinx文書をサクサク作成](http://qiita.com/mikanbako/items/28a3fc5d1da42939f941)
- [Sphinx + Jenkins で始めるドキュメントの継続的インテグレーション](http://www.techscore.com/blog/2015/04/01/sphinx-jenkins-で始めるドキュメントの継続的インテグレー/)
