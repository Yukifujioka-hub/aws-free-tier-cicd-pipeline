#!/bin/bash
set -eux

# パッケージ更新
apt-get update -y

# Docker インストール
apt-get install -y docker.io

# Docker 自動起動
systemctl start docker
systemctl enable docker

# ubuntu ユーザーを docker グループに追加
usermod -aG docker ubuntu

# Docker Compose v2 インストール
mkdir -p /usr/local/lib/docker/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.25.0/docker-compose-linux-x86_64 \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose