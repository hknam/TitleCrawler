from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import configparser
from make_config import initialize_config, initialize_logger, detect_gui, add_virtual_display
import os



#logger

logger = initialize_logger()

#read config file
logger.debug("read config file")
initialize_config()
config = configparser.ConfigParser()
config.read('config.ini')


driver_path = config['webdriver']['path']
base_url = config['webdriver']['base_url']



'''
def add_virtual_display():
    from pyvirtualdisplay import Display
    display = Display(size=(800,600), visible=0)
    return display
'''

def get_contents_list(driver):
    logger.debug("get channel list")

    get_next_content(driver)

    content = driver.find_element_by_id('content')
    program_wrap = content.find_element_by_class_name('program_wrap')
    program_list = program_wrap.find_element_by_id('cds_flick')
    container = program_list.find_element_by_class_name('flick-container')
    container_area = container.find_element_by_class_name('program_all')
    
    daily_program_list = container_area.find_elements_by_class_name('col')
    
    for col in daily_program_list:
        #anchors = col.find_elements_by_css_selector('a')
        try:
            anchors = col.find_elements_by_class_name('info_a')
            for anchor in anchors:
                href = anchor.get_attribute('href')
                get_detail_page(href)

        except Exception as e:
            logger.error(e)


def get_next_content(driver):

    while True:
        try:
            logger.debug("load more channels : click button" )
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.bt_more')))
            element.click()

        except Exception as e:
            logger.error(e)
            break

def get_detail_page(page_url):
    logger.debug("get video clips from channel : " + page_url)
    driver = webdriver.Firefox(executable_path=driver_path)

    folder_path = os.path.expanduser('~') + '/urls/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    output_filename = page_url.split('/')[-2]
    output_file = open(folder_path + output_filename, 'w')

    try:
        driver.set_page_load_timeout(30)
        driver.get(page_url)

        get_next_content(driver)
        logger.info('get more video clip lists')

        contents = driver.find_element_by_class_name('_infiniteCardArea')
        playlist = contents.find_elements_by_class_name('playlist')

        for weekly_list in playlist:
            clip_container = weekly_list.find_elements_by_class_name('playlist_container')
            for clip in clip_container:
                ul = clip.find_elements_by_css_selector('ul')
                for li in ul:
                    #dt = li.find_elements_by_css_selector('dt')
                    anchors = li.find_elements_by_css_selector('a')

                    for index in range(0, len(anchors)):
                        if index%2 == 1:
                            continue
                        else:
                            href = anchors[index].get_attribute('href')
                            output_file.write(href + "\n")
                            logger.info('save url to output file : ' + href)
                            #get_content_title(href)
                #roll_right(driver)

    except Exception as e:
        logger.debug(e)
    finally:
        output_file.close()
        driver.quit()

    
def roll_right(driver):
    try:
        logger.debug("load right clips")
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn_roll right _click')))
        element.click()

    except Exception as e:
        logger.error(e)


def get_content_title(page_url):
    logger.debug("get title from video clip")
    driver = webdriver.Firefox(executable_path=driver_path)
    try:
        global outout_file
        driver.get(page_url)

        clip_info_area = driver.find_element_by_id('clipInfoArea')
        clip_title_info = clip_info_area.find_element_by_class_name('watch_title ')
        clip_title = clip_title_info.find_element_by_css_selector('h3')
        clip_title_text = clip_title.get_attribute('title')
        logger.debug(driver.current_url)
        output_file.write(clip_title_text + '\n')

        driver.quit()

    except Exception as e:
        logger.debug(e)
    finally:
        driver.quit()


def run_web_browser():
    logger.debug("open filefox webdriver")
    driver = webdriver.Firefox(executable_path=driver_path)
    driver.set_page_load_timeout(15)

    logger.debug("get NaverTV page")
    driver.get(base_url)
    driver.implicitly_wait(10)

    get_contents_list(driver)

    logger.debug("close output file")



def main():
    if detect_gui():
        logger.info("Detect GUI Environment")
        run_web_browser()
    else:
        logger.info("Detect CLI Environment")
        display = add_virtual_display()
        display.start()
        run_web_browser()
        display.stop()


if __name__ == '__main__':
    main()




