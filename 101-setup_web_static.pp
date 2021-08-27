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

file { '/data/web_static/shared':
  ensure => 'directory',
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
}

file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/data/',
}

exec { 'permissions':
  path     => ['/usr/bin', '/sbin', '/bin', '/usr/sbin', 'usr/local/bin'],
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

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $var,
}

exec { 'start_server':
  require  => Exec['configuration'],
  path     => ['/usr/bin', '/sbin', '/bin', '/usr/sbin'],
  command  => 'sudo service nginx start',
  provider => 'shell',
  returns  => [0,1],
}