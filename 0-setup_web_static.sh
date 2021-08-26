#!/usr/bin/env bash
# Sets up a web server for deployment of a static website:

# Check if nginx is installed and if not, install it
if ! which nginx > /dev/null 2>&1;
then
    sudo apt-get update
    sudo apt-get -y install nginx
    sudo ufw allow 'Nginx HTTP'
fi

# Check if the required files exist. If not, create them
if [[ ! -e /data/web_static/releases/test ]];
then
    mkdir -p /data/web_static/releases/test
fi

if [[ ! -e /data/web_static/shared ]];
then
    mkdir -p /data/web_static/shared
fi

# Create a symbolic link named /data/web_static/current to
# /data/web_static/releases/test folder
ln -sfn /data/web_static/releases/test /data/web_static/current

# Create a fake HTML file /data/web_static/releases/test/index.html
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Change the owner and group of /data/
chown -R ubuntu:ubuntu /data/

# Configure Nginx configuration to serve content of
# /data/web_static/current to hbnb_static
#new_str="\\\tlocation/hbnb_static{\n\t\talias /data/web_static/current/;\n\t}"
#sed -i "18 a $new_str" /etc/nginx/sites-available/default
echo "
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        location /hbnb_static {
            alias /data/web_static/current/;
        }

        add_header X-Served-By $HOSTNAME;

        rewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGU1\wu4 \
permanent;
}" > /etc/nginx/sites-available/default

# Restart nginx
service nginx restart
