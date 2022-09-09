
# Deployments

## Heroku
1. Create an account on heroku.
2. Install heroku in machine.
	> sudo snap install heroku --classic
3. Login from heorku-cli
	> heroku login
	
	This will present an popup browser tab to confirm the login.
4. Update heroku to the latest version
	> heorku --update
5. Create an application on heroku. This will add a remote repo to local repo.
	> heroku create demo-fastapi-app<br>
	
	List apps present on the heroku
	> heroku apps
6. Push remote git repo code to the heroku git repo. This will build and deploy the code and give a endpoint URL to communicate.
	> git push heroku main
7. Add environment variables from setting in the web interface.
8. Adding an addon for postgresql (free one which will not be free after sometime)
	> heroku addons:create heroku-postgresql:hobby-dev

	List addons being used
	> heroku addons
9. Restart the heroku app instance
	> heroku ps:restart

10.  Show Logs 
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
	> listen_addresses = '*'                  # what IP address(es) to listen on;

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