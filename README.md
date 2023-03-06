# Danbi

## Python

* Version required 3.9

## Installation

* Install library using pip command

```bash
pip install -r requirements.txt
```

## Environments

```bash
# .env 파일 참조
export MYSQL_HOST={database_ip}
export MYSQL_NAME={database_name}
export MYSQL_USER={username}
export MYSQL_PWD={password}
export MYSQL_PORT={port}
export SECRET_KEY={secret_key}
export JWT_ALGORITHM={jwt_algorithm}
```

## Database
- Docker container에 MYSQL 올려서 사용
- MYSQL version 8.0
```bash
docker run -v {VOLUME PATH}:/var/lib/mysql -p {CONTAINER PORT}:3306 --name danbi -e MYSQL_ROOT_PASSWORD={PASSWORD} -d mysql:8.0 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```