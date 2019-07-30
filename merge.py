#!/usr/local/bin/python3

import os
from lang import Lang

dir_name = "ting_addons/"
base = Lang('ru_RU.po')
files_list = os.listdir(dir_name)
files_list.sort()
for file_name in files_list:
    base.merge(Lang(dir_name + file_name))
base.print_records()
