#! Python 3
# In this file described features for aggregation of directories:
# - monthly aggregation
# - yearly aggregation

# It is expected that this class would be lunched monthly, without gaps

# A class, that takes directories names in current directory,
# 1) then it converts each directory name to datetime object,                                                              
#       - DONE ( def __get_current_directories() => subdirs_dates )
# 2) then it compares each datetime object with current date,                                                              
# and decides if the object needs to be archived, if yes
#       - DONE ( def __get_aggregation_scale(dirs_list) => aggregation_scale )
# 3) then it creates an archive directory (if it hasn't been created yet),
#    and creates inside of archive directory a directory corresponding to aggregation time limit (monthly, yearly),    
#       - DONE ( def __archive_directories_creator() )                                    
# 4) then it moves all necessary directories (with their content) to the appropriate archive directory                     
#       - DONE

import os
from datetime import datetime
from pprint import pprint
import re
import shutil
import config

class Aggregator:
    def __init__(self, path=os.getcwd(), current_os='linux'):
        self.__path = path
        self.__date_format = "%d-%m-%Y"
        self.__aggregation_scale = {}
        self.__archive_dir_structure = {}
        self.__current_os = current_os

    # Method that takes directory names which current directory contains,
    # then it converts each directory name to datetime object,
    # and returns a collection of datetime objects
    def __get_current_directories(self):
        try:
            os.chdir(self.__path)
            print("Current working directory: {0}".format(os.getcwd()))
        except FileNotFoundError:
            print("Directory '{0}' does not exist".format(self.__path))
        except NotADirectoryError:
            print("{0} is not a directory".format(self.__path))
        except PermissionError:
            print("You do not have permissions to change to {0}".format(self.__path))
        
        subdirectories = os.listdir()

        subdirs_dates = []
        for subdirectory in subdirectories:
            if self.__dir_name_converter_helper(subdirectory):
                subdirs_dates.append(self.__dir_name_converter_helper(subdirectory))

        
        return subdirs_dates
    def __dir_name_converter_helper(self, dirname):
        date_format = self.__date_format
        p = re.compile('\d\d-\d\d-\d\d\d\d')
        m = p.match(dirname)
        if m:
            return datetime.strptime(dirname, date_format)


    # Method that compares each datetime object with current date,
    # and prints which aggregation scale it is possible to do (by month or by year)
    # and returns an object aggregation_scale:
    # { 
    #   aggregation_needed: <True/False>,
    #   year_aggregation_list: <year_aggregation_list>,
    #   month_aggregation_list: <month_aggregation_list>
    # }
    def __get_aggregation_scale(self, dirs_list):
        today = datetime.today()
        current_year = today.year
        current_month = today.month
        year_aggregation_list = []
        month_aggregation_list = []
        for directory in dirs_list:
            if directory.year < current_year:
                year_aggregation_list.append(directory)
            if directory.month < current_month and directory.year == current_year:
                month_aggregation_list.append(directory)

        aggregation_scale = {
            "aggregation_needed": '',
            "year_aggregation_list": '',
            "month_aggregation_list": '',
        }

        # Print aggregation check to user
        if year_aggregation_list:
            print("Aggregation available: by year.")
            aggregation_scale["aggregation_needed"] = True
            aggregation_scale["year_aggregation_list"] = year_aggregation_list
            aggregation_scale["month_aggregation_list"] = month_aggregation_list
        else:
            if month_aggregation_list:
                print("Aggregation available: by month.")
                aggregation_scale["aggregation_needed"] = True
                aggregation_scale["month_aggregation_list"] = month_aggregation_list
            else:
                print("Aggregation is not needed today.")
                aggregation_scale["aggregation_needed"] = False
        
        pprint(aggregation_scale)
        return aggregation_scale
    
    # Helper method, that checks and existence of a directory, 
    # and creates the directory if it is absent
    def __dir_checker_creator_helper(self, current_dir, new_dirname):
            if os.path.exists(f"{current_dir}{config.os_path[self.__current_os]}{new_dirname}"): # Check existence of directory needed
                print (f"'{new_dirname}' directory is present.")
            else: # If needed dir is absent - create it
                print(f"A '{new_dirname}' directory is absent. Creating it...", end=" ")
                new_dir_name = new_dirname
                parent_dir = current_dir
                needed_path = os.path.join(parent_dir, new_dir_name)
                os.mkdir(needed_path)
                print(f"Directory '{new_dirname}' created.")
    
    # Method that checks archive directories structure,
    # and creates an archive directory (if it haven't been created yet),
    # - a directory for archive year
    # - a directory for archive month
    # ./archive/<year>/
    # ./archive/<year>/<archived month 1>
    # ./archive/<year>/<archived month 2>
    # ./archive/<year>/<archived month ...>
    # ./archive/<year>/<archived month 12>
    # It returns an object, which describes a structure of the 'archive' directory, like:
    # {<year>: [<month 1>, <month 2>, ...], ...}
    def __archive_directories_creator(self):
        # Create a general archive folder
        self.__dir_checker_creator_helper(os.getcwd(), 'archive')        
       
        # Check existence of the archive year directory
        # Go to archive dir
        os.chdir('./archive/')
        current_year = datetime.today().year
        # Create a folder for current year
        self.__dir_checker_creator_helper(os.getcwd(), str(current_year))
        # Create folder(s) for archive year(s)
        archive_years = []
        for date in self.__aggregation_scale["year_aggregation_list"]:
            if date.year not in archive_years:
                archive_years.append(date.year)
        # Create folders for archive year(s)
        for archive_year in archive_years:
            self.__dir_checker_creator_helper(os.getcwd(), str(archive_year))
        
        # Check existence of the archive month directory(s), and create if absent
        print(os.listdir())
        archive_years_moths_dict = {}
        for archive_year in archive_years:
            archive_years_moths_dict[archive_year] = []
        archive_years_moths_dict[current_year] = []

        for scale in ['month_aggregation_list', 'year_aggregation_list']:
            for archive_date in self.__aggregation_scale[f"{scale}"]:
                if archive_date.month not in archive_years_moths_dict[archive_date.year]:
                    archive_years_moths_dict[archive_date.year].append(archive_date.month)

        for key in archive_years_moths_dict:
            print(key, '=>', archive_years_moths_dict[key])
            for month in archive_years_moths_dict[key]:
                self.__dir_checker_creator_helper(f"{os.getcwd()}{config.os_path[self.__current_os]}{key}", f"{month}")
        # Go up to the dir 'directories' 
        os.chdir("..")

        return archive_years_moths_dict
    
    # Method that moves needed directories to needed archive directory
    def __move__old_directories_to_archive_directories(self):
        """Moves old directories to the appropriate archive directories."""
        
        # Moving directories for the previous years
        years_to_archive = []
        for year_to_archive in self.__aggregation_scale["year_aggregation_list"]:
            years_to_archive.append(year_to_archive.year)

        years_to_archive_deduplicated = list(dict.fromkeys(years_to_archive))
        for old_year in years_to_archive_deduplicated:
            for old_directory in self.__aggregation_scale["year_aggregation_list"]:
                if old_directory.year == old_year:
                    old_directory_path = os.path.join(
                        os.getcwd(),
                        str(f"{'{:02d}'.format(old_directory.day)}-{'{:02d}'.format(old_directory.month)}-{old_year}"),
                        )
                    
                    archive_directory_path = os.path.join(
                        os.getcwd(),
                        "archive",
                        str(old_directory.year),
                        str(old_directory.month),
                    )

                    # Additional check if the day directory is already archived
                    if os.path.exists(archive_directory_path):
                        if os.path.isdir(os.path.join(
                            archive_directory_path,
                            f"{'{:02d}'.format(old_directory.day)}-{'{:02d}'.format(old_directory.month)}-{old_year}"
                        )):
                            print(f"The folder for the day {old_directory.date()} is already archived")
                        else:
                            shutil.move(old_directory_path, archive_directory_path)
        
        # Moving directories for the current year  
        for old_directory in self.__aggregation_scale["month_aggregation_list"]:
            old_directory_path = os.path.join(
                os.getcwd(),
                str(f"{'{:02d}'.format(old_directory.day)}-{'{:02d}'.format(old_directory.month)}-{old_directory.year}"),
            )
            
            archive_directory_path = os.path.join(
                os.getcwd(),
                "archive",
                str(old_directory.year),
                str(old_directory.month),
            )
            
            # Additional check if the day directory is already archived
            if os.path.exists(archive_directory_path):
                if os.path.isdir(os.path.join(
                    archive_directory_path,
                    f"{'{:02d}'.format(old_directory.day)}-{'{:02d}'.format(old_directory.month)}-{old_directory.year}"
                )):
                    print(f"The folder for the day {old_directory.date()} is already archived")
                else:
                    shutil.move(old_directory_path, archive_directory_path)
    
    # Method to run the aggregation
    def run_aggregation(self):
        print(" Aggregation check started ".center(90, '-'))
        list_of_dirs_to_check = self.__get_current_directories()
        pprint(f'list_of_dirs_to_check: {list_of_dirs_to_check}')
        self.__aggregation_scale = self.__get_aggregation_scale(list_of_dirs_to_check)
        self.__archive_dir_structure = self.__archive_directories_creator()
        self.__move__old_directories_to_archive_directories()
