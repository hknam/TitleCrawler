
# coding: utf-8

# In[14]:

import configparser
import platform
import os
import sys


# In[15]:

def detect_os():
    platform_name = platform.system()
    if platform_name == 'Linux':
        return 'geckodriver_linux'
    elif platform_name == 'Darwin':
        return 'geckodriver_macos'
    else:
        print('Do not support this platform')
        sys.exit(1)


# In[16]:

config = configparser.ConfigParser()
config['filename'] = {}


# In[17]:

config['filename']['controller'] = 'controller.log'
config['filename']['browser'] = detect_os()
config['filename']['output'] = 'title.txt'


# In[18]:

config['webdriver'] = {}


# In[19]:

config['webdriver']['path'] = './webdriver/' + detect_os()
config['webdriver']['base_url'] = 'http://tv.naver.com/t/all/popular'


# In[20]:

with open('config.ini', 'w') as configfile:
    config.write(configfile)


# In[ ]:



