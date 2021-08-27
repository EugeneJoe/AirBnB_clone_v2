# Set up a web server for deployment of web files

exec { 'Update':
  path     => ['/usr/bin', '/sbin', '/bin', '/usr/sbin'],
  command  => 'sudo apt-get update -y',
  provider => 'shell',
  returns  => [0,1],
}

exec { 'Install_nginx':
  require  => Exec['Update'],
  path     => ['/usr/bin', '/sbin', '/bin', '/usr/sbin'],
  command  => 'sudo apt-get install nginx -y',
  provider => 'shell',
  returns  => [0,1],
}

exec { '/data/':
  path     => ['/usr/bin', '/sbin', '/bin', '/usr/sbin'],
  command  => 'sudo mkdir -p /data/web_static/releases/test',
  provider => 'shell',
  returns  => [0,1],
}

$html="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => $html,
  require => Exec['/data/']
}

exec { 'link':
  path     => ['/usr/bin', '/sbin', '/bin', '/usr/sbin'],
  command  => 'ln -sfn /data/web_static/releases/test /data/web_static/current',
  provider => 'shell',
  return   => [0,1],
  require  => Exec['/data/']
}

exec { 'permissions':
  path     => ['/usr/bin', '/sbin', '/bin', '/usr/sbin'],
  command  => 'chown -R ubuntu:ubuntu /data/',
  provider => 'shell',
  returns  => [0,1],
  require  => Exec['/data/'],
}

$var="server {
        listen 80 default_server;
        listen [::]:80 default_server;
        location /hbnb_static {
            alias /data/web_static/current/;
        }
        add_header X-Served-By ${hostname};
        rewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGU1\wu4 \
permanent;
}"

exec { 'configuration':
  path     => ['/usr/bin', '/sbin', '/bin', '/usr/sbin'],
  command  => 'echo $var > /etc/nginx/sites-available/default'
  provider => 'shell',
  returns  => [0,1],
  require  => Exec['Install_nginx'],
}

exec { 'start_server':
  require  => Exec['configuration'],
  path     => ['/usr/bin', '/sbin', '/bin', '/usr/sbin'],
  command  => 'sudo service nginx start',
  provider => 'shell',
  returns  => [0,1],
}