# -*- coding: utf-8 -*-
import os
import shutil


class MoveFile:
    @staticmethod
    def move_file(source, target):
        if not os.path.exists(source) or not os.path.exists(target):
            raise Exception("Source folder or target folder doesn't exist")
        if not os.path.isdir(source) or not os.path.isdir(target):
            raise Exception("parameter should be a folder")

        for root, dirs, files in os.walk(source, topdown=True):
            for dir in dirs:
                shutil.copy(root+ os.sep + dir, target)
            for file in files:
                shutil.copy(root + os.sep + file, target)


if __name__ == "__main__":
    m = MoveFile()
    m.move_file(r'E:\_Automation\autoblog\articles', r'E:\autoblog\source\_posts')