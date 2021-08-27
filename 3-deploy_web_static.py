#!/usr/bin/python3
"""
Creates and distributes an archive to web servers
"""

from datetime import datetime
from fabric.api import run, local, env, put, sudo
from os.path import isfile, exists


env.hosts = [
    '34.139.119.72',
    '34.139.135.201'
]


def do_pack():
    """ Creates a .tgz archive from the contents of the web_static folder """
    now = datetime.now()
    now_str = now.strftime("%Y%m%d%H%M%S")
    now_str = now_str.replace('/', '')
    if not exists('versions'):
        local("mkdir versions")
    tar_name = "versions/web_static_{}.tgz".format(now_str)
    result = local("tar -cvzf {} web_static".format(tar_name))
    if result.succeeded:
        return tar_name
    else:
        return None


def do_deploy(archive_path):
    """ Distributes an archive to web servers """
    if not isfile(archive_path):
        return False
    try:
        localpath = archive_path.split('/')[1]
        newpath = localpath.split('.')[0]
        rempath = "/data/web_static/releases/"

        put(archive_path, "/tmp/")
        sudo("mkdir -p {}{}".format(rempath, newpath))
        sudo("tar -xzf /tmp/{} -C {}{}".format(localpath, rempath, newpath))
        sudo("rm /tmp/{}".format(localpath))
        sudo("cp -r {0}{1}/web_static/* {0}{1}/".format(rempath, newpath))
        sudo("rm -rf {}{}/web_static".format(rempath, newpath))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {}{}/ /data/web_static/current".format(rempath, newpath))
        return True
    except:
        return False


def deploy():
    """ Call the do_pack() function and based on its return value,
        call do_deploy or return False
    """
    result = do_pack()
    if result:
        return do_deploy(result)
    else:
        return False
