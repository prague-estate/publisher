# Prague Estate publisher

[![tests](https://github.com/prague-estate/publisher/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/prague-estate/publisher/actions/workflows/tests.yml)
[![linters](https://github.com/prague-estate/publisher/actions/workflows/linters.yml/badge.svg?branch=main)](https://github.com/prague-estate/publisher/actions/workflows/linters.yml)

### Pre-requirements
- [Python 3.12+](https://www.python.org/downloads/)
- [Redis](https://redis.io/docs/getting-started/installation/)


### Local setup
```shell
git clone git@github.com:prague-estate/publisher.git prague-publisher
cd prague-publisher
python3.12 -m venv venv
source venv/bin/activate
pip install -U poetry pip setuptools
poetry config virtualenvs.create false --local
poetry install
```

### Local run tests
```shell
pytest --cov=publisher
```

### Local run linters
```shell
flake8 publisher/
mypy publisher/
```

### Run publisher session
```shell
python -m publisher.publisher
```

### Run subscription downgrade session
```shell
python -m publisher.subs_downgrade
```

### Run bot service
```shell
python -m publisher.bot
```


### Host setup
```shell
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt install -y software-properties-common python3.12 python3.12-dev python3.12-venv 
apt install -y libpq-dev gcc python3-pip redis supervisor
apt-get upgrade
adduser publisher

vi /etc/logrotate.d/prague-publisher

groupadd supervisor
usermod -a -G supervisor root
usermod -a -G supervisor publisher

vi /etc/supervisor/supervisord.conf  # change chown and chmod params
vi /etc/supervisor/conf.d/publisher.conf
service supervisor restart


```
