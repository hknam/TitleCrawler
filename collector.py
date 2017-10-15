from selenium import webdriver

import configparser
from make_config import initialize_config, initialize_logger, detect_gui, add_virtual_display
import os
import sys
from bs4 import BeautifulSoup
import urllib.request


#logger


logger = initialize_logger()

#read config file
logger.debug("read config file")
initialize_config()
config = configparser.ConfigParser()
config.read('config.ini')


driver_path = config['webdriver']['path']


try:
    start_page_number = int(sys.argv[2])
    end_page_number = int(sys.argv[3])
except Exception as e:
    print(e)
    sys.exit(1)


def search(dirname):
    '''
    folder_path = os.path.expanduser('~') + '/titles/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    '''
    filenames = os.listdir(dirname)
    # for filename in filenames:

    for index in range(start_page_number, end_page_number):

        full_filename = os.path.join(dirname, filenames[index])
        print(full_filename)
        logger.debug('read saved file : ' + full_filename)
        #open_clip_list(folder_path+filename, full_filename)
        open_clip_list(full_filename)

def open_clip_list(file):


    #output_file = open(folder_path, 'w')

    with open(file, 'r') as f:
        urls = f.read().split('\n')


        for url in urls:
            #save_title(output_file, url)
            save_folder_name = file.split('/')[-1]
            folder_path = os.path.expanduser('~') + '/titles/'
            save_folder_path = folder_path +  save_folder_name
            if not os.path.exists(save_folder_path):
                os.makedirs(save_folder_path)
                save_html_bs4(save_folder_path, url)
            else:
                logger.debug('exists clip titles')
                continue

    #output_file.close()

def run_web_browser():

    driver = webdriver.Firefox(executable_path=driver_path)
    #driver.set_page_load_timeout(15)

    return driver

def save_html(folder_path, page_url):
    filename = page_url.split('/')[-1]
    if len(filename) == 0:
        logger.debug('no url')
        return
    output_file = open(folder_path + '/' + filename, 'w')
    driver = run_web_browser()
    try:
        logger.debug("get html from video clip")
        driver.get(page_url)
        output_file.write(driver.page_source)
        logger.debug('save page source')
    except Exception as e:
        logger.error(e)
    finally:
        driver.quit()
        output_file.close()


def save_html_bs4(folder_path, page_url):
    filename = page_url.split('/')[-1]
    if len(filename) == 0:
        logger.debug('no url')
        return
    output_file = open(folder_path + '/' + filename, 'w')

    try:
        logger.debug("get html from video clip")
        url_open = urllib.request.urlopen(page_url)
        soup = BeautifulSoup(url_open, 'html.parser', from_encoding='utf-8')
        page_source = soup.prettify()
        output_file.write(page_source)
        logger.debug('save page source')
    except Exception as e:
        logger.error(e)
    finally:
        output_file.close()


def save_title(output_file, page_url):
    logger.debug("open filefox webdriver")
    driver = run_web_browser()

    try:
        logger.debug("get title from video clip")
        driver.get(page_url)

        clip_info_area = driver.find_element_by_id('clipInfoArea')
        clip_title_info = clip_info_area.find_element_by_class_name('watch_title ')
        clip_title = clip_title_info.find_element_by_css_selector('h3')
        clip_title_text = clip_title.get_attribute('title')
        logger.debug(driver.current_url)
        output_file.write(clip_title_text + '\n')

        driver.quit()
        logger.debug('close firefox webdriver')

    except Exception as e:
        logger.debug(e)
    finally:
        driver.quit()



def main():

    try:
        dirname = sys.argv[1]
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    if detect_gui():
        logger.info("Detect GUI Environment")
        search(dirname)
    else:
        logger.info("Detect CLI Environment")
        display = add_virtual_display()
        display.start()
        search(dirname)
        display.stop()


if __name__ == '__main__':
    main()
