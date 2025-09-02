# uses bibgallery env

from Shelf import Shelf

if __name__ == "__main__":
    shelf = Shelf("https://yefan-zhi.github.io/shelf/")

    shelf.generate_html_file()
