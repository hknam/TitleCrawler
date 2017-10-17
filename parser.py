from bs4 import BeautifulSoup
import urllib.request
import os
import sys

try:
    page_folder_path = sys.argv[1]
    start_page_number = int(sys.argv[2])
    end_page_number = int(sys.argv[3])
except IndexError as e:
    print('[FOLDER PATH] [START PAGE NUMBER] [END PAGE NUMBER]')
    sys.exit(1)

def search(dirname):

    filenames = os.listdir(dirname)
    

    for index in range(start_page_number, end_page_number):
        full_filename = os.path.join(dirname, filenames[index])
        save_clip_title(full_filename)


def save_clip_title(html_folder_path):
    save_folder_path = os.path.expanduser('~') + '/titles/'
    print(save_folder_path)
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)

    output_file = save_folder_path  + html_folder_path.split('/')[-1]



    with open(output_file, 'w') as outfile:
        for file in os.listdir(html_folder_path):
            page_url = 'file://' + html_folder_path + '/' + file
            url_open = urllib.request.urlopen(page_url)
            soup = BeautifulSoup(url_open, 'html.parser', from_encoding='utf-8')

            try:
                title_area_div = soup.find('div', attrs={'id':'clipInfoArea'})
                clip_title = title_area_div.find('h3', attrs={'class':'_clipTitle'}).text.strip()
                print(clip_title)
            except Exception as e:
                print(e)
                continue
            finally:
                outfile.write(clip_title + '\n')


search(page_folder_path)