# Python 3
# This scirpt intended for manage the whole process
# The general flow is next:
# 1. Check today's date to check a need of aggregation of folders
# 1.1. If today is a new month - run mothly folders aggregation
# 1.2. If today is a new year - run yearly folders aggregation
# 2. Create a folder for today.

import create_folder_files
import config
import aggregation
import platform


if __name__ == "__main__":
    current_os = platform.system().lower()
    print(f"Current OS: {current_os}")
    aggregator = aggregation.Aggregator(f'.{config.os_path[current_os]}.{config.os_path[current_os]}directories', current_os)
    workday_today = create_folder_files.TodayTemplate(config.files_content, 'directories')
    workday_today.run_creation()
    aggregator.run_aggregation()
    
    