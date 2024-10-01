#!/usr/env/python3

apt update -y && apt-get install libldap2-dev libsasl2-dev ldap-utils build-essential -y
pip3 install  -r ../requirements.txt