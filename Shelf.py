__author__ = "Yefan Zhi"

import codecs
import os
import pathlib

from PIL import Image


# https://www.clcindex.com/
class Shelf():
    def __init__(self,
                 remote_folder,
                 root_folder_path="",
                 catalog_folder="catalog",
                 ):
        self.remote_folder = remote_folder
        self.root_folder_path = root_folder_path
        if not os.path.isabs(root_folder_path):
            self.root_folder_path = pathlib.Path(os.path.realpath(__file__)).parent.absolute()
        self.catalog_folder = catalog_folder
        # self.catalog_path = os.path.join(self.root_folder_path, catalog_folder)
        self.html_main_local = ""
        self.html_main_remote = ""

    def generate_html_file(self):

        html_begin_1 = '''<html>
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
	<title>'''
        html_begin_2 = '''</title>
	</head>
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

        self.count = 0

        def collect_folder(current_folder):
            current_path = os.path.join(self.root_folder_path, current_folder)
            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)
                if os.path.isfile(item_path):
                    try:
                        with Image.open(item_path) as img:
                            img.verify()  # Verify if it's an image
                            width, height = img.size
                            height = min(3000, height)
                            self.count += 1
                            pdf = None
                            if os.path.isfile(item_path[:-4] + ".pdf"):
                                pdf = item_path[:-4] + ".pdf"
                            elif os.path.isdir(item_path[:-4] + ".PDF"):
                                pdf = item_path[:-4] + ".PDF"
                            if pdf:
                                write_string_to_htmls('<div class="image"><a href="')
                                self.html_main_local += os.path.join(current_path, pdf)
                                self.html_main_remote += self.remote_folder + "/" + current_folder + "/" + pdf
                                write_string_to_htmls('"><img src="')
                                self.html_main_local += item_path
                                self.html_main_remote += self.remote_folder + "/" + current_folder + "/" + item
                                write_string_to_htmls('" height={}></a></div>'.format(int(height ** 0.8)))
                            else:
                                write_string_to_htmls('<div class="image"><img src="')
                                self.html_main_local += item_path
                                self.html_main_remote += self.remote_folder + "/" + current_folder + "/" + item
                                write_string_to_htmls('" height={}></div>'.format(int(height ** 0.8)))
                    except:
                        pass
                else:
                    collect_folder(os.path.join(current_folder, item))

        collect_folder(self.catalog_folder)
        write_string_to_htmls("<!-- {} books. -->".format(self.count))
        html_begin = html_begin_1 + "{} books".format(self.count) + html_begin_2
        with codecs.open(os.path.join(self.root_folder_path, "Shelf.html"), 'w',
                         "utf-8") as html_file:
            html_file.write(html_begin + self.html_main_local + html_end)

        with codecs.open(os.path.join(self.root_folder_path, "index.html"), 'w',
                         "utf-8") as html_file:
            html_file.write(html_begin + self.html_main_remote + html_end)

        print(self.count, "books.")
