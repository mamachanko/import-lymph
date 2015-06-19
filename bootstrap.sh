#!/bin/bash

pushd /europython

echo "Updating package cache..."
apt-get update

echo "Installing requirements..."
apt-get install -y python-dev
pip install -U pip
pip install -r requirements.txt

echo "Installing tmuxinator..."
gem install tmuxinator
ln -s `pwd`/tmuxinator.yml /home/vagrant/.tmuxinator/europython.yml
echo "export EDITOR=vim" >> /home/vagrant/.profile
ln -s `pwd`/vimrc /home/vagrant/.vimrc
ln -s `pwd`/tmux.conf /home/vagrant/.tmux.conf

echo "Installing middleware..."
apt-get install -y zookeeper rabbitmq-server

