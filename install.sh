#!/bin/bash
pip install virtualenv && \
virtualenv ./venv && \
source ./venv/bin/activate && \
pip install -r requirements.txt && \
deactivate && \
ln -s $PWD/irsend.service /etc/systemd/system/irsend.service && \
systemctl daemon-reload && \
chown -R www-data:www-data $PWD && \
ln -s $PWD/irsend.conf /etc/nginx/sites-enabled/irsend.conf
