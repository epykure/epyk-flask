
![](https://raw.githubusercontent.com/epykure/epyk-flask/blob/master/epyk_flask/static/images/epyk-flask.PNG)

### First Version out now!

Web Server embedding the `Epyk`_ Python Framework to allow you to leverage on the power of HTML and JS all from python

Installation:
==================

.. code-block:: text
    pip install epyk_flask


Get Started:
==============
.. code-block:: text
    epyk-flask new -p server_path

This will create a new server structure at the path of your choice

.. code-block:: text
    epyk-flask env -p server_path/epyk_flask/UI/scripts

This will create a new environments where you want to store scripts that will use Epyk

.. code-block:: text
    epyk-flask run -p server_path

This will run your server and render your HTML pages

If you want to know all the options and commands available in the epyk-flask CLI please run:

.. code-block:: text

epyk-flask -h

Configuration:
=================

The configuration for your server is located under:

.. code-block:: text
    server_path/epyk_flask/config

Please be aware the epyk_flask is the name of your project by default but it can be different if you chose to create it with a different name



Documentation:
==================

Please refer to the documentation from the package Epyk to get started with your first pages.


.. _Epyk: https://pypi.org/project/epyk