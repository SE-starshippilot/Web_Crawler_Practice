# How to run

1. Clone this repository

   - ```shell
     git clone https://github.com/SE-starshippilot/Web_Crawler_Practice.git
     ```

2. Install necessary packages

   - ```shell
     pip install -r requirements.txt -i https://pypi.douban.com/simple
     ```

3. Run the script

   - ```shell
     python get_movies.py
     ```

(optional): You can check the options for this script, but by default they should be OK

- ```bash
  $python get_movies.py -h
  usage: get_movies.py [-h] [--baseURL BASEURL]
                       [--download_image DOWNLOAD_IMAGE]
                       [--save_html_folder SAVE_HTML_FOLDER]
                       [--excel_file_name EXCEL_FILE_NAME]
  
  options:
    -h, --help            show this help message and exit
    --baseURL BASEURL, -b BASEURL
                          base url
    --download_image DOWNLOAD_IMAGE, -d DOWNLOAD_IMAGE
                          download image
    --save_html_folder SAVE_HTML_FOLDER, -s SAVE_HTML_FOLDER
                          If specified, save html to this
                          folder.
    --excel_file_name EXCEL_FILE_NAME, -n EXCEL_FILE_NAME
                          excel file name
  ```
