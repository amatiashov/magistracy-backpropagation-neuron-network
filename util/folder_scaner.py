import os
"""
    Данный метод сканирует целевую папку (target_folder) и формирует
    список всех файлов, входящих в нее
"""


def folder_scan(target_folder="digit_templates"):
    file_list = []
    for file in os.listdir(path=target_folder):
        if not file.startswith(".") and not file.startswith("README"):
            file_list.append(file)
    return file_list
