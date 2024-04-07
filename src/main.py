from textnode import TextNode
import shutil
import os

def main():
    copy_contents("static", "public")

def copy_contents(from_directory, to_directory):
    # remove contents from old directory    
    shutil.rmtree(f"{to_directory}", True)
    os.mkdir("public")

    def copy(from_directory, to_directory):
        paths = os.listdir(from_directory)
        for path in paths:
            isFile = os.path.isfile(os.path.join(from_directory, path))
            src, dst = os.path.join(from_directory, path), os.path.join(to_directory, path)
            if isFile:
                print(f"Copying: {src} to {dst}")
                shutil.copy(src, dst)
            else:
                os.mkdir(dst)
                copy(f"{src}", f"{dst}")
    
    copy(from_directory, to_directory)
    



if __name__ == '__main__':
    main()