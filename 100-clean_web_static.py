#!/usr/bin/python3
""" Deletes out-of-date archives """

from os import listdir
from fabric.api import run, local, cd, lcd, env

env.hosts = ['34.139.119.72', '34.139.135.201']


def do_clean(number=0):
    """ Deletes out-of-date archives locally and on my remote hosts """

    if int(number) == 0:
        number = 1
    else:
        number = int(number)

    old_new = sorted(listdir("versions"))
    for i in range(number):
        if old_new:
            old_new.pop()
    with lcd("versions"):
        for arch in old_new:
            local("rm -rf {}".format(arch))

    with cd("/data/web_static/releases"):
        files = run("ls -tr").split()
        old_new = [a for a in files if "web_static_" in a]
        [old_new.pop() for i in range(number) if old_new]
        for arch in old_new:
            run("rm -rf {}".format(arch))
