#! Python 3
# This script is intended to create a folder and files inside of it

import os
from datetime import date


class TodayTemplate:
    def __init__(self, files_content, dest_dir_for_creation = os.getcwd()):
        self.__today = date.today()
        self.__current_day_name = self.__today.strftime("%d-%m-%Y")
        self.__current_day_name_US = self.__today.strftime("%m/%d/%Y")
        self.__current_directory = dest_dir_for_creation
        self.__new_folder = str(self.__current_day_name)
        self.__today_working_directory = ''
        # A dictionary where we set which files (file names) we want to create, 
        # and set a content we populate them
        self.__files_content = files_content(self.__current_day_name, self.__current_day_name_US)
        # If 'directories' folder doesn't exist, it is necessary to create it
        if not os.path.exists(self.__current_directory):
            os.makedirs('directories')

    # Function to create a new directory. Aruguments of this function: 
    # 1) destination_dir    - a location where to create a new directory; 
    # 2) new_dir_name       - a name of new directory.
    # It returns a full path wich includes new created directory
    def __create_folder(self, destination_dir, new_dir_name):
        final_directory = os.path.join(destination_dir, new_dir_name)
        if not os.path.exists(final_directory):
            print(f' Creation of the new directory {new_dir_name} and files is started '.center(90, '-'))
            os.makedirs(final_directory)
        else:
            print(f' Directory with the name {new_dir_name} already exists '.center(90, '!'))
        
        return final_directory
    
    # A method to create a file. Its arguments: 
    # 1) directory_path         - a path of the directory, where we want to create a file; 
    # 2) name_of_file           - a name of file we want to create; 
    # 3) lines_of_text_to_file  - a list with strings, each element we write into the file, line by line. 
    # It returns None.
    def __create_files(self, directory_path, name_of_file, lines_of_text_to_file):
            file_path = os.path.join(directory_path, name_of_file)
            # check if the directory exists
            if os.path.exists (directory_path):
                # create the file
                if os.path.isfile(file_path) and os.path.exists(file_path):
                    print(f"A file \'{name_of_file}\' already exists. Creation is skipped.")
                else:
                    with open(file_path, "w") as f:
                        for line in lines_of_text_to_file:
                            f.write(line)
                        print(f"File \"{name_of_file}\" was created.")
            else:
                print("Directory doesn\'t exist.")
    
    # A method to start creation of a folder and files inside of it
    def run_creation(self):
        self.__today_working_directory = self.__create_folder(self.__current_directory, self.__new_folder)
        for key in self.__files_content:
            self.__create_files(self.__today_working_directory, key, self.__files_content[key])