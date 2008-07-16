AMAT: Automated Monitoring And Tunnels

Preliminaries
=============

How we got to here...

As root:
* apt-get update
* apt-get install python-pylons
* apt-get install python-sqlalchemy
* paster create -t pylons amat

How to run the server...
* paster serve --reload development.ini

Controllers:
* reg
* checkin
* dump

Installation and Setup
======================

Install ``amat`` using easy_install::

    easy_install amat

Make a config file as follows::

    paster make-config amat config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.
