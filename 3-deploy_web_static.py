#!/usr/bin/python3
"""
Creates and distributes an archive to web servers
"""

from datetime import datetime
from fabric.api import *
import os


env.hosts = [
    '34.139.119.72',
    '34.139.135.201'
]


def do_pack():
    """ Creates a .tgz archive from the contents of the web_static folder """
    now = datetime.now()
    now_str = now.strftime("%Y%m%d%H%M%S")
    now_str = now_str.replace('/', '')
    if not os.path.exists('versions'):
        os.makedirs('versions')
    tar_name = "versions/web_static_{}.tgz".format(now_str)
    print("Packing web_static to {}".format(tar_name))
    result = local("tar -cvzf {} web_static".format(tar_name))
    if result.succeeded:
        return tar_name
    else:
        return None


def do_deploy(archive_path):
    """ Distributes an archive to web servers """
    if not os.path.exists(archive_path):
        return False
    else:
        localpath = archive_path.split('/')[1]
        newpath = localpath.split('.')[0]
        rempath = "/data/web_static/releases/"
        put("{}".format(archive_path), "/tmp/{}".format(localpath))
        run("mkdir -p /data/web_static/releases/{}/".format(newpath))
        run("tar -xzf /tmp/{} -C {}{}/".format(localpath, rempath, newpath))
        run("rm /tmp/{}".format(localpath))
        run("mv {r}{l}/web_static/* {r}{l}/".format(r=rempath, l=newpath))
        run("rm -rf {}{}/web_static".format(rempath, newpath))
        run("rm -rf /data/web_static/current")
        rr = run("ln -s {}{} /data/web_static/current".format(rempath, newpath))
        if rr.succeeded:
            return True
        else:
            return False


def deploy():
    """ Call the do_pack() function and based on its return value,
        call do_deploy or return False
    """
    result = do_pack()
    if result:
        return do_deploy(result)
