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

        html_main = ""

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
                        html_main += '<div class="image"><img src="{}" height={}>'.format(
                            pic_path, int(height ** 0.6 * 3))
                        if count_every > 0 and count % count_every == 0:
                            html_main += "<div class='caption-left'>{}</div>".format(count)
                        html_main += "</div>"

            html = html_begin + html_main + html_end
            with codecs.open(os.path.join(self.root_folder_path, "Shelf.html"), 'w',
                             "utf-8") as html_file:
                html_file.write(html)

        print(count, "books.")