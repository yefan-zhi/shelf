__author__ = "Yefan Zhi"

import codecs
import os
import pathlib

from PIL import Image


# https://www.clcindex.com/
class Shelf():
    def __init__(self,
                 root_folder_path="",
                 catalog_folder="catalog",
                 ):
        self.root_folder_path = root_folder_path
        if not os.path.isabs(root_folder_path):
            self.root_folder_path = pathlib.Path(os.path.realpath(__file__)).parent.absolute()
        self.catalog_path = os.path.join(self.root_folder_path, catalog_folder)
        self.html_main_local = ""
        self.html_main_remote = ""

    def generate_html_file(self, count_every=0):

        html_begin = '''<html>
<head>
    <meta charset="UTF-8">
    <style>
        .image {
            display: inline-block;
            margin: 25px 0px 0px 0px;
            padding: 0px;
            vertical-align: bottom;
            position: relative; 
        }
        .image img {
            border-radius: 3px;
        }
        .caption-left {
            position: absolute; 
            bottom: -18px; 
            left: 0px;
            right: 0px;
            color: black;
            text-align: center;
            font-size: 14px;
        }
    </style>
</head>
<body>
'''
        html_end = '''
</body>
</html>'''

        self.html_main_local = ""
        self.html_main_remote = ""

        def write_string_to_htmls(s):
            self.html_main_local += s
            self.html_main_remote += s

        count = 0
        for category in os.listdir(self.catalog_path):
            category_path = os.path.join(self.catalog_path, category)
            if not os.path.isfile(category_path):
                for pic in os.listdir(category_path):
                    pic_path = os.path.join(category_path, pic)
                    if os.path.isfile(pic_path):
                        img = Image.open(pic_path)
                        width, height = img.size
                        height = min(3000, height)
                        count += 1
                        write_string_to_htmls('<div class="image"><img src="')
                        self.html_main_local += pic_path
                        self.html_main_remote += "https://yefan-zhi.github.io/shelf/catalog/" + category + "/" + pic
                        write_string_to_htmls('" height={}>'.format(int(height ** 0.6 * 3)))
                        if count_every > 0 and count % count_every == 0:
                            write_string_to_htmls("<div class='caption-left'>{}</div>".format(count))
                        write_string_to_htmls("</div>")

        with codecs.open(os.path.join(self.root_folder_path, "Shelf.html"), 'w',
                         "utf-8") as html_file:
            html_file.write(html_begin + self.html_main_local + html_end)

        with codecs.open(os.path.join(self.root_folder_path, "index.html"), 'w',
                         "utf-8") as html_file:
            html_file.write(html_begin + self.html_main_remote + html_end)

        print(count, "books.")
