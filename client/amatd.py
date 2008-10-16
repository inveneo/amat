#!/usr/bin/env python

# amatd.py
# (c) Inveneo 2008

import os, daemonize

if __name__ == "__main__":

    retCode = daemonize.createDaemon(os.getcwd())

    procParams = """
    return code = %s
    process ID = %s
    parent process ID = %s
    process group ID = %s
    session ID = %s
    user ID = %s
    effective user ID = %s
    real group ID = %s
    effective group ID = %s
    """ % (retCode, os.getpid(), os.getppid(), os.getpgrp(), os.getsid(0),
    os.getuid(), os.geteuid(), os.getgid(), os.getegid())

    open("createDaemon.log", "w").write(procParams + "\n")

    # uncomment this if you want daemon to stay alive
    import time
    while 1:
        time.sleep(1)

    sys.exit(retCode)

