import configparser
import platform
import os
import sys



def detect_os():
    platform_name = platform.system()
    if platform_name == 'Linux':
        return 'geckodriver_linux'
    elif platform_name == 'Darwin':
        return 'geckodriver_macos'
    else:
        print('Do not support this platform')
        sys.exit(1)

def initialize_config():

    config = configparser.ConfigParser()
    config['filename'] = {}


    config['filename']['controller'] = 'controller.log'
    config['filename']['browser'] = detect_os()
    config['filename']['output'] = 'title.txt'


    config['webdriver'] = {}


    config['webdriver']['path'] = './webdriver/' + detect_os()
    config['webdriver']['base_url'] = 'http://tv.naver.com/t/all/popular'


    with open('config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    initialize_config()