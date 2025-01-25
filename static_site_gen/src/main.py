import os
from os.path import isdir
import shutil


def wipe_dir_contents(dir):
    for item in os.listdir(dir):
        item_path = os.path.join(dir, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


def main():
    static_dir = "/Users/kiga/bootDev/static_site_gen/static/"
    pub_dir = "/Users/kiga/bootDev/static_site_gen/public/"
    wipe_dir_contents(pub_dir)
    shutil.copytree(static_dir, pub_dir, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
