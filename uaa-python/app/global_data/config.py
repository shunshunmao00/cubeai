import os
import rsa
import yaml
from app.utils.loacl_ip import get_local_ip


class Config:
    def __init__(self):
        with open('./application.yml', 'r') as f:
            yml = yaml.load(f, Loader=yaml.SafeLoader)

        self.app_name = yml['service']['ename']

        try:
            self.app_version = yml['service']['version']
        except:
            self.app_version = '0.0.1'

        self.server_ip = get_local_ip()

        self.app_profile = os.environ.get('APP_PROFILE', 'dev').lower()

        if self.app_profile == 'dev':
            try:
                self.server_port = yml['service']['port']['dev']
            except:
                self.server_port = 80
            self.consul_address = '127.0.0.1'
            self.consul_tags = ['profile-dev']
            self.consul_http_check_url = 'http://{}:{}/management/health'.format(self.server_ip, self.server_port)
        else:
            try:
                self.server_port = yml['service']['port']['prod']
            except:
                self.server_port = 80
            self.consul_address = 'consul'
            self.consul_tags = ['profile-prod']
        self.consul_port = 8500
        self.consul_http_check_url = 'http://{}:{}/management/health'.format(self.server_ip, self.server_port)

        if self.app_profile == 'dev':
            self.db_host = '127.0.0.1'
            self.db_port = 3306
        else:
            self.db_host = 'uaa-mysql'
            self.db_port = 3306
        self.db_username = 'root'
        self.db_password = ''
        self.db_name = 'uaa'

        if not os.path.exists('app/resources/public_key.pem') or not os.path.exists('app/resources/private_key.pem'):
            public_key, private_key = rsa.newkeys(2048)
            self.public_key = public_key.save_pkcs1()
            self.private_key = private_key.save_pkcs1()
            with open("app/resources/public_key.pem", "wb") as file:
                file.write(self.public_key)
            with open("app/resources/private_key.pem", "wb") as file:
                file.write(self.private_key)
        else:
            with open("app/resources/public_key.pem", "rb") as file:
                self.public_key = file.read()
            with open("app/resources/private_key.pem", "rb") as file:
                self.private_key = file.read()
