import configparser
import platform
import logging
import sys
import datetime
import subprocess

def detect_os():
    platform_name = platform.system()
    if platform_name == 'Linux':
        return 'geckodriver_linux'
    elif platform_name == 'Darwin':
        return 'geckodriver_macos'
    else:
        print('Do not support this platform')
        sys.exit(1)

def detect_gui():
    command = "type Xorg"
    run_command = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = run_command.stdout.readline()
    if str(output).find('Xorg is') >= 0 :
        return True
    else:
        return False


def initialize_config():

    config = configparser.ConfigParser()
    config['filename'] = {}

    current_time = datetime.datetime.now()
    controller_log_name = str(current_time)
    config['filename']['controller'] = controller_log_name + '.log'
    config['filename']['browser'] = detect_os()


    config['webdriver'] = {}


    config['webdriver']['path'] = './webdriver/' + detect_os()
    config['webdriver']['base_url'] = 'http://tv.naver.com/t/all/like'


    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def initialize_logger():
    logger = logging.getLogger('TitleCrawler_logger')
    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    file_handler = logging.FileHandler('./TitleCrawler.log')
    stream_handler = logging.StreamHandler()

    file_handler.setFormatter(fomatter)
    stream_handler.setFormatter(fomatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.DEBUG)
    return logger

if __name__ == "__main__":
    initialize_config()