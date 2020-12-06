Run following commands to get service up and running.

Running containers:

```bash
docker run -d -p 5672:5672 -p 15672:15672 --name rabbitmq rabbitmq
docker run -d -p 6379:6379 --name redis redis
```

Running environment:

```bash
virtualenv venv
pip install pip-tools
pip install -r requirements/base.txt -r requirements/test.txt
nameko run temp_messenger.service --config config.yaml
```

Enter redis container cli:

```bash
docker exec -it redis /bin/bash
redis-cli
```
