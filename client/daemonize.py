#!/usr/bin/env python

import os
import sys

MAXFD     = 1024
DEV_NULL  = "/dev/null"
DEV_PTS_0 = "/dev/pts/0"

def becomeDaemon(workdir="/"):
    """Detach a process from the controlling terminal and run it in the
    background as a daemon.
    """

    # create child process
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)

    if (pid == 0):
        # this is the child

        os.setsid()

        # import signal           # Set handlers for asynchronous events.
        # signal.signal(signal.SIGHUP, signal.SIG_IGN)

        # create grandchild process (see literature for why)
        try:
            pid = os.fork()
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)

        if (pid == 0):
            # this is the grandchild
            os.chdir(workdir)
            os.umask(0)
        else:
            # child exits
            os._exit(0)

    else:
        # parent exits
        os._exit(0)

    # determine max number of file descriptors
    import resource
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if (maxfd == resource.RLIM_INFINITY):
        maxfd = MAXFD
  
    # Iterate through and close all file descriptors.
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:
            pass

    # reopen first three
    os.open(DEV_NULL, os.O_RDONLY)
    os.open(DEV_NULL, os.O_WRONLY)
    os.open(DEV_NULL, os.O_WRONLY)
    return(0)

if __name__ == "__main__":

    retCode = becomeDaemon(os.getcwd())

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

    open("becomeDaemon.log", "w").write(procParams + "\n")

    # uncomment this if you want daemon to stay alive
    import time
    while 1:
        time.sleep(1)

    sys.exit(retCode)

