# This file contains configuration parameters for the script

def files_content(current_day_name, current_day_name_US):
    return {
            f"Tasks_{current_day_name}.txt": [
                "--- Turnover of the prev. shift ---\n",
                "\n",
                "--- Tasks for today ---\n",
                "\n",
                "--- Turnover for today ---\n",
                f"Turnover {current_day_name_US}\n",
                "\n"
                ],
            f"Backups_{current_day_name}.txt": [
                f"Backups Failures for the day: \n", 
                "\n",
                ],
            f"ISP_1_Maintenances_{current_day_name}": [
                "--- In Progress Maintenance ---\n",
                "\n",
                "--- Upcoming Maintenance ---\n"
            ],
            f"ISP_2_Maintenances_{current_day_name}": [
                "--- In Progress Maintenance ---\n",
                "\n",
                "--- Upcoming Maintenance ---\n"
            ],
            f"ISP_1_Repair_Active_{current_day_name}": [
                "\n"
            ],
            f"ISP_2_Repair_Active_{current_day_name}": [
                "\n"
            ],
        }

os_path = {
    "windows": "\\",
    "linux": "/",
    "darwin": "/"
}