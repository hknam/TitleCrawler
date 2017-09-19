from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import configparser
from make_config import initialize_config, initialize_logger
import time
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


logger.debug("open filefox webdriver")
driver = webdriver.Firefox(executable_path = driver_path)
driver.set_page_load_timeout(15)




def get_contents_list():
    logger.debug("get channel list")
    get_next_content(5)

    content = driver.find_element_by_id('content')
    program_wrap = content.find_element_by_class_name('program_wrap')
    program_list = program_wrap.find_element_by_id('cds_flick')
    container = program_list.find_element_by_class_name('flick-container')
    container_area = container.find_element_by_class_name('program_all')
    
    daily_program_list = container_area.find_elements_by_class_name('col')
    
    for col in daily_program_list:
        #anchors = col.find_elements_by_css_selector('a')
        anchors = col.find_elements_by_class_name('info_a')
        for anchor in anchors:
            href = anchor.get_attribute('href')
            get_detail_page(href)



def get_next_content(count):

    for cnt in range(0, count):
        logger.debug("load more channels : " + str(count) )
        load_contents_script = "document.querySelector('.bt_more').click()"
        driver.execute_script(load_contents_script)
        time.sleep(10)

def get_detail_page(page_url):
    logger.debug("get video clips from channel : " + page_url)
    driver = webdriver.Firefox(executable_path=driver_path)

    folder_path = os.path.expanduser('~') + '/title-list/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    output_filename = page_url.split('/')[-1]
    output_file = open(folder_path + output_filename, 'w')

    try:
        driver.set_page_load_timeout(30)
        driver.get(page_url)

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
    except Exception as e:
        logger.debug(e)
    finally:
        output_file.close()
        driver.quit()

    
    

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



logger.debug("get NaverTV page")
driver.get(base_url)
driver.implicitly_wait(10)

get_contents_list()

logger.debug("close output file")
