README for AMAT Client

amatd.py
--------
The AMAT client runs as a daemon.  It is written in Python.
So it is called amatd.py

If sent SIGHUP, it will re-read its config file and re-register itself
with the new parameters and go back to regular checkins.

If sent SIGTERM, it will fold up its wings and die more or less gracefully.

daemonize.py
------------
A library that creates a bona fide Unix daemon out of your code.  The
wheel reinvented yet again.  But why not?  Reinvention is fun.

The rest of these...
-rwxr-xr-x 1 inveneo inveneo  148 2008-07-14 18:13 getmac.sh
-rw-r--r-- 1 inveneo inveneo 3443 2008-10-14 18:14 old_amat_client.py
-rw-r--r-- 1 inveneo inveneo 1335 2008-10-14 18:14 old_amatd.py
-rw-r--r-- 1 inveneo inveneo 1671 2008-07-15 11:17 tunneler_client.py
-rw-r--r-- 1 inveneo inveneo  710 2008-07-14 18:13 tunneler.sh

...were written by Dillo, and I'm not sure what all they do, but seems
they are already superceded by the new amatd.  Thanks, Dillo!

