
# coding: utf-8

# In[43]:

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import configparser


# In[44]:

#read config file
config = configparser.ConfigParser()
config.read('config.ini')


# In[45]:

driver_path = config['webdriver']['path']
base_url = config['webdriver']['base_url']
output_filename = config['filename']['output']


# In[46]:

output_file = open(output_filename, 'w')


# In[47]:

driver = webdriver.Firefox(executable_path = driver_path)
driver.set_page_load_timeout(15)


# In[48]:

def get_contents_list():
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


# In[49]:

def get_detail_page(page_url):
    driver = webdriver.Firefox(executable_path = driver_path)
    driver.set_page_load_timeout(15)
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
                        get_content_title(href)
    
    driver.quit()
    
    


# In[50]:

def get_content_title(page_url):
    
    global output_file
    driver = webdriver.Firefox(executable_path = driver_path)
    driver.set_page_load_timeout(15)
    driver.get(page_url)
    
    clip_info_area = driver.find_element_by_id('clipInfoArea')
    clip_title_info = clip_info_area.find_element_by_class_name('watch_title ')
    clip_title = clip_title_info.find_element_by_css_selector('h3')
    clip_title_text = clip_title.get_attribute('title')
    print(clip_title_text)
    output_file.write(clip_title_text + '\n')
    
    driver.quit()


# In[51]:

driver.get(base_url)
driver.implicitly_wait(10)
get_contents_list()

output_file.close()


# In[ ]:



