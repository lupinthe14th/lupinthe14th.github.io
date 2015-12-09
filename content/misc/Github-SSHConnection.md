Title: Github SSH 接続手順 ~ 二段階認証対応 ~
Date: 2015-11-20 15:00
Modified: 2015-12-08 09:38
Category: misc
Tags: Github, SSH, Mac,
Slug: Github-SSHConnection
Author: Hideo Suzuki
Summary: Github を二段階認証にするとSSH 接続でしか Push 出来ないのでその方法をまとめる

Github を二段階認証にすると SSH 接続でしか Push 出来なくなる。
そこで、 SSH 接続する為の方法をまとめる。

# 目的

- Github に `git push` 可能になること

# 手順

## 前提条件

この手順は、Mac OS X Yosemite の場合についてです。

## SSH 認証鍵の作成

作成する鍵の種類と鍵長は以下表の通り。鍵の種類は、DSAのセキュリティレベルのおよ
そ2倍であると考えられる ECDSA（楕円曲線DSA）を用いる。


鍵の種類|鍵長
--------|-----
ECDSA鍵 |521bit

### OpenSSH のアップデートおよび設定

Mac OS X Yosemite のデフォルトのOpenSSH の `ssh-keygen` および `ssh-agent` では
ECDSA はサポートされていないので、以下の手順にてアップデートを行い、設定を行う。

```console
% brew tap homebrew/dupes
% brew install openssh --with-brewed-openssl --with-keychain-support
% launchctl stop org.openbsd.ssh-agent
% launchctl unload -w /System/Library/LaunchAgents/org.openbsd.ssh-agent.plist
```

`sudo vi /System/Library/LaunchAgents/org.openbsd.ssh-agent.plist`
で、`/usr/bin/ssh-agent` を `/usr/local/bin/ssh-agent` に置換する。


```console
% launchctl load -w -S Aqua /System/Library/LaunchAgents/org.openbsd.ssh-agent.plist
% export SSH_AUTH_SOCK=$(launchctl getenv SSH_AUTH_SOCK)
```

`.zshrc` を編集し、以下を追加する。

```vim
export PATH=/usr/local/bin/:${PATH}
eval $(ssh-agent) > /dev/null
```


## SSH 認証の公開鍵と秘密鍵の作成

以下コマンドにて、公開鍵: `id_ecdsa.pub` と秘密鍵: `id_ecdsa` を作成する。

```console
% cd ~/.ssh
% ssh-keygen -t ecdsa -b 521 -C test@example.com
```

## SSH クライアント側へのSSH認証鍵の設定

SSH 接続を簡単にする為、 `~/.ssh/config` の設定を行います。

```vim
Host github
  HostName github.com
  IdentityFile ~/.ssh/id_ecdsa
  User git
```

## Github へのSSH認証鍵の登録

SSH 公開鍵を登録します。

1. GitHubにブラウザでアクセス
1. 左側メニューのSSH Keys -> Add key を選択
1. Title: に任意文字列を入力
1. Key: に `pbcopy < ~/.ssh/id_ecdsa.pub` を実行後のクリップボードを貼り付け

## Github への接続確認

接続に成功すると以下の様に表示される。

```console
% ssh -T github
Hi lupinthe14th! You've successfully authenticated, but GitHub does not provide
shell access.
```

## ローカルリポジトリの設定を変更
リポジトリの設定ファイルを開き、URLの項目をgit@...からはじまるSSH接続方式に変更
する。


# 参考資料

- [GitHub Help - GitHub Enterprise  Documentation](https://help.github.com)
- [How to Update OpenSSH on Mac OS X](http://www.dctrwatson.com/2013/07/how-to-update-openssh-on-mac-os-x/)
- [GitHubユーザーのSSH鍵6万個を調べてみた](http://d.hatena.ne.jp/hnw/20140705)
- [GitHubにSSH接続できるようにする方法](http://qiita.com/katsukii/items/9fd5bbe822904d7cdd0a)
- [Updating OpenSSH on Mac OS X 10.10 Yosemite](https://mochtu.de/2015/01/07/updating-openssh-on-mac-os-x-10-10-yosemite/)
