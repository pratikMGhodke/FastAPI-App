# Deployments

## Heroku

1. Create an account on heroku.
2. Install heroku in machine.
    > sudo snap install heroku --classic
3. Login from heroku-cli

    > heroku login

    This will present an popup browser tab to confirm the login.

4. Update heroku to the latest version
    > heroku --update
5. Add a `Procfile` with below contents which shows heroku how to run the API application.

    > web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}

6. Create an application on heroku. This will add a remote repo to local repo.

    > heroku create demo-fastapi-app<br>

    List apps present on the heroku

    > heroku apps

7. Push remote git repo code to the heroku git repo. This will build and deploy the code and give a endpoint URL to communicate.
    > git push heroku main
8. Add environment variables from setting in the web interface.
9. Adding an addon for postgresql (free one which will not be free after sometime)

    > heroku addons:create heroku-postgresql:hobby-dev

    List addons being used

    > heroku addons

10. Restart the heroku app instance

    > heroku ps:restart

11. Show Logs
    > heroku logs -t

## EC2

1. Create an EC2 instance.
2. Allow all traffic.
3. Add the code from the github (clone).
4. Add .env file in the `/home/user`
5. Add `set -o allexport; source /home/pratik/.env; set +o allexport` to `~/.profile` file.
6. Install postgresql.
    > sudo apt install postgresql postgres-contrib
7. Edit `/etc/postgresql/14/main/postgresql.conf` file by updating below line

    > listen_addresses = '\*' # what IP address(es) to listen on;

    which allows outside postgres connections to communicate.

8. Edit `/etc/postgresql/14/main/pg_hba.conf` file by updating below lines

    ```none
    # Database administrative login by Unix domain socket
    local   all             postgres                                scram-sha-256

    # TYPE  DATABASE        USER            ADDRESS                 METHOD

    # "local" is for Unix domain socket connections only
    local   all             all                                     scram-sha-256
    # IPv4 local connections:
    host    all             all             0.0.0.0/0               scram-sha-256
    # IPv6 local connections:
    host    all             all             ::/0                    scram-sha-256
    # Allow replication connections from localhost, by a user with the
    # replication privilege.
    local   replication     all                                     peer
    host    replication     all             127.0.0.1/32            scram-sha-256
    host    replication     all             ::1/128                 scram-sha-256
    ```

### Using gunicorn

This is a process manager. Create workers and use load balancing.

1. Install gunicorn and some libraries
    > pip install gunicorn httptools uvloop
2. Run with `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8001`

### Running gunicorn as system service

1. Create a service file

    ```bash
    [Unit]
    Description=demo fastapi application
    After=network.target

    [Service]
    User=pratik
    Group=pratik
    WorkingDirectory=/home/pratik/FastAPI-App
    Environment="PATH=/home/pratik/FastAPI-App/venv/bin"
    EnvironmentFile=/home/pratik/.env
    ExecStart=/home/pratik/FastAPI-App/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000

    [Install]
    WantedBy=multi-user.target
    ```

2. Add this file to `/etc/systemd/system` with name `demo-fastapi-app.service`.
3. Run this as a service
    > sudo systemctl start demo-fastapi-app.service
4. Enable this service to start at the startup
    > sudo systemctl enable demo-fastapi-app.service

### Nginx

1. Install nginx
    > sudo apt install nginx
2. Start nginx service
    > sudo systemctl start nginx
3. Change default service config for nginx in `/etc/nginx/sites-available`
    ```none
    server_name _;
    location / {
            proxy_pass http://localhost:8000;
            proxy_http_version 1.1;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $http_host;
            proxy_set_header X-NginX-Proxy true;
            proxy_redirect off;
        }
    ```
4. Restart nginx
    > sudo systemctl restart nginx

### SSL Certificate

1. Install certbot
    > sudo snap install certbot --classic
2. Config nginx with certbot (auto)
    > sudo certbot --nginx

### Firewall

1. Check firewall status
    > sudo ufw status
2. Allow traffic

    > sudo ufw allow http <br>
    > sudo ufw allow https <br>
    > sudo ufw allow ssh <br>
    > sudo ufw allow 5432 <br>

3. Start firewall
    > sudo ufw enable


### CI/CD

#### CI - Continuos Integration

#### Github Actions
see `.github/workflows/build-deploy.yml` for config file

1. Whenever code is pushed(configurable), github actions runs.
2. Add env variables, from setting>environments>(after creating new env)>add secrets.

### Docker Hub
1. Register
2. Account setting > Security > Get that access token!
3. In github environment secrets, add `DOCKER_HUB_USERNAME` and `DOCKER_HUB_ACCESS_TOKEN`.

#### CD - Continuos Deployment
1. Deploy code to heroku via git (see `.github/workflows/build-deploy.yml`)
