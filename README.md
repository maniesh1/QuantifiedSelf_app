
# QuantifiedSelf App

A daily habit tracker system.



## Run Locally
open six wsl or ubuntu terminal.

In the backend directory, the following command to install requirements and 
setup flask server.

```bash
  sh local_setup.sh
  sh local_run.sh
```
Setup redis-server with following command
```bash
  source .env/bin/activate
  redis-server
```
If redis-server already running and gives error, first kill the server 
with following command, then run redis-server.
```bash
  ps aux | grep redis
  kill -9 3405
```

To setup celery run 
```bash
  source .env/bin/activate
  celery -A application.tasks.celery beat --max-interval 1 -l info
  celery -A application.tasks.celery worker -l info
```
Start Mailhog server 

```bash
  source .env/bin/activate
  ~/go/bin/MailHog
```
In the fronted directory, run

```bash
  npm install
  npm run serve
```



