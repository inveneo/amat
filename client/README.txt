README.txt for Automated Monitoring And Tunnels (AMAT) Client

amatd.py
--------
The AMAT client runs as a daemon.  It is written in Python.
So it is called amatd.py
It logs to /var/log/amatd.log

If sent SIGHUP, it will re-read its config file and re-register itself
with the new parameters and go back to regular checkins.

If sent SIGTERM, it will fold up its wings and die more or less gracefully.

Things to do before starting it up the first time
=================================================
# From the directory containing this README file...
$ sudo ln -s `pwd`/amatd-control /etc/init.d/amatd-control

# In the following command, turn on paster-control in runlevels 2-5
$ sudo sysv-rc-conf

# Run the daemon by hand...
$ sudo /etc/init.d/amatd-control start

Components
==========

amatd.conf
----------
The config file for this instance of the AMAT network.

amatd.py
--------
The actual AMAT daemon.  See above.

daemonize.py
------------
A library that creates a bona fide Unix daemon out of your code.  The
wheel reinvented yet again.  But why not?  Reinvention is fun.

tunnel.py
---------
A library for managing reverse ssh tunnels.  The meat.

utils.py
--------
Some handy utilities.

