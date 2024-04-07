from textnode import TextNode
import shutil
import os

def main():
    copy_contents("static", "public")

def copy_contents(from_directory, to_directory):
    # remove contents from old directory    
    shutil.rmtree(f"{to_directory}", True)
    os.mkdir("public")

    print(os.listdir(from_directory))

if __name__ == '__main__':
    main()