NRC API Wrapper
===============

This is a simple Nike Run Club (NRC) API wrapper implemented in Python. 

This API implements a small subset of HTTP GET requests to the NRC API, along with a
bare minimum set of parsing utilities for extracting run summary data from the raw
JSON responses from the NRC HTTP-based web server.

Usage
-----

First, you will need to [get your bearer token](https://gist.github.com/niw/858c1ecaef89858893681e46db63db66) for the NikePlus API. 
You will then need to populate the `bearer.py` config file with your token. Now 
simply run the example usage script with

    $ python3 main.py

or

    $ chmod +x main.py
    $ ./main.py

## Python Version / OS

All development and testing was done on a Fedora 30 machine using Python 3.7.6.

## Acknowledgements
* https://github.com/niw - for the above linked gist, whose [bash script](https://gist.github.com/niw/858c1ecaef89858893681e46db63db66#file-fetch_nike_puls_all_activities-bash) I used as a reference

