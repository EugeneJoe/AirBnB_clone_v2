#!/usr/bin/env bash
# Sets up a web server for deployment of a static website with the following requirements:
# Install Nginx if not already installed
# Create the folder /data/ if it doesn't already exist
# Crea the folder /data/web_static/ if it doesn’t already exist
# Create the folder /data/web_static/releases/ if it doesn’t already exist
# Create the folder /data/web_static/shared/ if it doesn’t already exist
# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
# Create a fake HTML file /data/web_static/releases/test/index.html
# (with simple content, to test your Nginx configuration)
# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
# If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
# Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and gro\up exist).
# This should be recursive; everything inside should be created/owned by this user/group.
# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static (ex: https://mydomainname.tech/hbnb_static).
# Restart Nginx after updating the configuration:

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

# Create a symbolic link named /data/web_static/current to /data/web_static/releases/test folder
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

# Configure Nginx configuration to serve content of /data/web_static/current to hbnb_static
#new_str="\\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"
#sed -i "18 a $new_str" /etc/nginx/sites-available/default
echo "
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        location /hbnb_static {
            alias /data/web_static/current/;
        }

        add_header X-Served-By $HOSTNAME;

        rewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGU1\wu4 permanent;
}" > /etc/nginx/sites-available/default

# Restart nginx
service nginx restart
