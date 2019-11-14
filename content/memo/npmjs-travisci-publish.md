Title: npm releasing
Date: 2019-11-14 21:11
Modified: 2019-11-14 22:06
Category: memo
Tags: yarn, git, npm
Author: Hideo Suzuki
Summary: npm package の継続的リリース作業をTravis ci使って自動化したのに動かなくなったので直したメモ

[TOC]

# Trigger

そろそろパッチ当てたのリリースしようかと思って、・・・tag打てばCD走るよな・・・と思い `git tag` 使ったけどCD走る気配がなく・・・

# TL;DR

`.travis.yml` のbranchesの定義を追加した為、動かなかった。動くよう修正したのは以下。

```
---
language: node_js
node_js:
  - "10"
  - "node"
  - "lts/*"
branches:
  only:
    - master
    - develop
    - /^greenkeeper/.*$/
    - /^v?[0-9\\.]+/
cache: yarn
before_install:
  - curl -o- -L https://yarnpkg.com/install.sh | bash
  - export PATH="$HOME/.yarn/bin:$PATH"
  - yarn global add greenkeeper-lockfile@1
  - yarn global add codecov
install: yarn
before_script:
  - greenkeeper-lockfile-update
script:
  - yarn test
after_script:
  - codecov
  - greenkeeper-lockfile-upload
jobs:
  include:
    - stage: npm release
      if: tag IS present
      node_js: "node"
      deploy:
        provider: npm
        email: "$NPM_EMAIL"
        api_key: "$NPM_TOKEN"
        skip_cleanup: true
        on:
          tags: true
```

```
git commit
yarn version
git push origin master --tag
```

原因判明して解決するまでパッチバージョン9もあげる事に。なんとも情けない。

# Process

- なんで動かないのか。
   - コマンド間違っているのか？と、git tagをつけたり消したり・・・
   - travis ciの構成ファイルの `jobs` の定義をいろいろいじったけど、動かず・・・
- travis ciのRequestsをみてみると `Branch "v0.1.10" not included per configuration.` なんてのが
- あゝ、tagがbranch名になってて、ちょっと前に追加した、branchesの定義でジョブ動かないようになってしまっていたのだなと 

# SeeAlso

- [yarn version](https://yarnpkg.com/en/docs/cli/version)
- [Automated npm releases with Travis CI](https://tailordev.fr/blog/2018/03/15/automated-npm-releases-with-travis-ci/)
