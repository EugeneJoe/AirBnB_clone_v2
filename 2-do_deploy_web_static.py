#!/usr/bin/python3
"""
Distributes an archive to web servers
"""

from fabric.api import run, put, env
import os


env.hosts = [
    '34.139.119.72',
    '34.139.135.201'
]


def do_deploy(archive_path):
    """ Distributes an archive to web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        localpath = archive_path.split('/')[1]
        newpath = localpath.split('.')[0]
        rempath = "/data/web_static/releases/"
        put(archive_path, "/tmp".format(localpath))
        run("mkdir -p {}{}/".format(rempath, newpath))
        run("tar -xzf /tmp/{} -C {}{}/".format(localpath, rempath, newpath))
        run("rm /tmp/{}".format(localpath))
        run("mv {r}{l}/web_static/* {r}{l}/".format(r=rempath, l=newpath))
        run("rm -rf {}{}/web_static".format(rempath, newpath))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(rempath, newpath))
        return True
    except:
        return False
