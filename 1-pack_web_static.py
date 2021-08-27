#!/usr/bin/python3
"""
Generate a .tgz archive from the contents of web_static folder
The name of the archive created is:
       web_static_<year><month><day><hour><minute><second>.tgz
"""

import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """ Creates a .tgz archive from the contents of the web_static folder """
    now = datetime.now()
    now_str = now.strftime("%Y%m%d%H%M%S")
    now_str = now_str.replace('/', '')
    if not os.path.exists('versions'):
        local("mkdir versions")
    tar_name = "versions/web_static_{}.tgz".format(now_str)
    result = local("tar -cvzf {} web_static".format(tar_name))
    if result.succeeded:
        return tar_name
    else:
        return None
