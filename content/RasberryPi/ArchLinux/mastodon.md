Title: ArchlinuxでMastdon
Date: 2017-04-14 00:00
Modified: 2017-04-14 00:00
Category: Rasberry Pi
Tags: mastodon, aws, , USB-HDD, 
Slug: mastodon
Author: Hideo Suzuki
Summary: Archlinuxでmastodon
Status: draft

# 目的
面白そうだからやってみる
- 一旦全く使わなくなったawsのアカウントを利用して試す
- 仕組みとかわかってきたらRasberryPiで自宅サーバとして運用も視野に入れる

# ドメインの登録とRRの作成
お手軽にawsのRoute53サービスから新規ドメイン作成し、グローバルIPアドレスを紐付ける

# Postfix環境の構築

## Postfix Install

## Postfix config

## Erastic IP aws Route53 RTRの定義とメール配信申請 

## DKIM config

- OpenDKIM Install

```console
sudo pacman -Sy opendkim
```

# Install 手順

## 前提条件
- aws環境にArchlinux環境の構築は省略
- yarnのインストール
- nftablesのインストール
- rbenvのインストール

## mastodonユーザーの作成

```console
useradd -m mastodon
```

```console
su - mastodon
```


## mastodon clone

```console
git clone https://github.com/tootsuite/mastodon.git
```

## Install rbenv

```
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
cd ~/.rbenv && src/configure && make -C src
echo 'export PATH = "$HOME/.rbenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(rbenv init -)"' >> ~/.bash_profile
```

```
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
```

```
export PATH = "$HOME/.rbenv/bin::$PATH"
eval "$(rbenv init -)"
```

```
cd mastodon
```

```
echo "Compiling Ruby $(cat .ruby-version): warning,  this takes a while!!!"
rbenv install $(cat .ruby-version)
rbenv global $(cat .ruby-version)
```



# Configure database

## init postgresql

```console
su - postgres
initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data'
```

## Configure database

```console
sudo -i -u postgres createuser -U postgres mastodon -s
```


# Install gems and node modules

```console
su - mastodon
cd mastodon
gem install bundler
bundle install
yarn install
```
# Configure redis

```console
systemctl enable redis
systemctl start redis
```

# 

# Build Mastodon

```console
bundle exec rails db:setup RAIS_ENV = production
bundle exec rails assets:precompile RAILS_ENV=production
```

## 推奨ビルド環境

```console
pacman -S --needed base-devel libffi libyaml openssl zlib
```

## mastodonのインストール
`pacman` を利用してパッケージインストールを行う。

```console
pacman -Sy ffmpeg imagemagick libpqxx libxml2 libxslt nodejs postgresql redis yaourt
```


