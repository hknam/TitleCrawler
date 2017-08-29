
import sys
from selenium import webdriver
import configparser
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800,600))
display.start()

config = configparser.ConfigParser()
config.read('config.ini')

driver_path = config['webdriver']['path']
base_url = config['webdriver']['base_url']

def get_content_title(page_url):
    driver = webdriver.Firefox(executable_path=driver_path)
    try:
        global outout_file
        driver.get(page_url)

        clip_info_area = driver.find_element_by_id('clipInfoArea')
        clip_title_info = clip_info_area.find_element_by_class_name('watch_title ')
        clip_title = clip_title_info.find_element_by_css_selector('h3')
        clip_title_text = clip_title.get_attribute('title')

        output_file.write(clip_title_text + '\n')
        print(clip_title_text)

        driver.quit()

    except Exception as e:
        print(e)
    finally:
        driver.quit()

if len(sys.argv[1]) == 0:
    print('NEED TITLE LIST')
    sys.exit(1)



title_list_file = sys.argv[1]
output_filename = 'title_list.txt'


with open(title_list_file, 'r') as f:
    titles = f.read().split('\n')

if len(sys.argv[2]) == 0:
    print('NEED START TITLE INDEX')
    print("total title-list length : ", len(titles))
    sys.exit(1)


if len(sys.argv[3]) == 0:
    print('NEED END TITLE INDEX')
    print("total title-list length : ", len(titles))
    sys.exit(1)

output_file = open(output_filename, 'w')

start_index = int(sys.argv[2])
end_index = int(sys.argv[3])


for index in range(start_index, end_index):
    try:
        get_content_title(titles[index])
    except Exception as e:
        print(e)


'''
for title in titles:
    try:
        get_content_title(title)
    except Exception as e:
        print(e)
'''
output_file.close()
display.stop()