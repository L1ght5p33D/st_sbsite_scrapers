import json
import time
import datetime
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from elasticsearch import Elasticsearch, exceptions, TransportError
import binascii
from os import urandom
import requests
import urllib3

import sys
reload(sys)
sys.setdefaultencoding('ascii')

