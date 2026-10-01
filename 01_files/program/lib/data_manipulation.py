import os

# == INSTRUCTIONS ==
#
# Below, you'll find lots of incomplete functions.
#
# Your job: Implement each function so that it does its job effectively.
#
# Tips:
# * Use the material, Python Docs and Google as much as you want
#
# * A warning: the data you are using may not contain quite what you expect;
#   cleaning data (or changing your program) might be necessary to cope with
#   "imperfect" data

# == EXERCISES ==

# Purpose: return a boolean, False if the file doesn't exist, True if it does
# Example:
#   Call:    does_file_exist("nonsense")
#   Returns: False
#   Call:    does_file_exist("AirQuality.csv")
#   Returns: True
# Notes:
# * Use the already imported "os" module to check whether a given filename exists
def does_file_exist(filename):
    return os.path.exists(filename)

# Purpose: get the contents of a given file and return them; if the file cannot be
# found, return a nice error message instead
# Example:
#   Call: get_file_contents("AirQuality.csv")
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;[...]
#     [...]
#   Call: get_file_contents("nonsense")
#   Returns: "This file cannot be found!"
# Notes:
# * Learn how to open file as read-only
# * Learn how to close files you have opened
# * Use readlines() to read the contents
# * Use should use does_file_exist()
def get_file_contents(filename):
    if does_file_exist(filename):
        with open(filename, "r") as contents:
            return contents.readlines()
    else:
        return "This file cannot be found!"

# Purpose: fetch Christmas Day (25th December) air quality data rows, and if
# boolean argument "include_header_row" is True, return the first header row
# from the filename as well (if it is False, omit that row)
# Example:
#   Call: christmas_day_air_quality("AirQuality.csv", True)
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
#   Call: christmas_day_air_quality("AirQuality.csv", False)
#   Returns:
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
# Notes:
# * should use get_file_contents() - N.B. as should any subsequent
# functions you write, using anything previously built if and where necessary
def christmas_day_air_quality(filename, include_header_row):
    contents = get_file_contents(filename)
    
    christmas_day = [row for row in contents if row.startswith('25/12/')]

    if include_header_row:
        christmas_day.insert(0, contents[0])

    return christmas_day

# Purpose: fetch Christmas Day average of "PT08.S1(CO)" values to 2 decimal places
# Example:
#   Call: christmas_day_average_air_quality("AirQuality.csv")
#   Returns: 1439.21
# Data sample:
# Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH;;
# 10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;13,6;48,9;0,7578;;
def christmas_day_average_air_quality(filename):

    christmas_day = christmas_day_air_quality(filename, True)

    column_names = christmas_day[0].split(";")
    column_index = column_names.index("PT08.S1(CO)")

    air_qual_list = [float(row.split(";")[column_index]) for row in christmas_day[1:]]

    return round(sum(air_qual_list) / len(air_qual_list), 2)

# Purpose: scrape all the data and calculate average values for each of the 12 months
#          for the "PT08.S1(CO)" values, returning a dictionary of keys as integer
#          representations of months and values as the averages (to 2 decimal places)
# Example:
#   Call: get_averages_for_month("AirQuality.csv")
#   Returns: {1: 1003.47, [...], 12: 948.71}
# Notes:
# * Data from months across multiple years should all be averaged together

def get_all_data_for_month(filename, month):
    return [row for row in get_file_contents(filename) if row[3:5] == month]

def get_air_quality_data_for_month(filename, month):
    air_qual_list = [float(row.split(";")[3]) for row in get_all_data_for_month(filename, month)]
    return round(sum(air_qual_list) / len(air_qual_list), 2)

def get_averages_for_month(filename):
    return {int(month): get_air_quality_data_for_month(filename, month) for month in [f"{x:02d}" for x in range(1, 13)]}

filename = "/Users/alisonkieselack/Projects/python_extension_challenges/01_files/program/AirQuality.csv"

#print(get_all_data_for_month(filename, "01"))
#print(get_air_quality_data_for_month(filename, "10"))
print(get_averages_for_month(filename))

# Purpose: write only the rows relating to March (any year) to a new file, in the same
# location as the original, including the header row of labels
# Example
#   Call: create_march_data("AirQuality.csv")
#   Returns: nothing, but writes header + March data to file called
#            "AirQualityMarch.csv" in same directory as "AirQuality.csv"
import csv 

def create_march_data(filename):
    contents = get_file_contents(filename)
    march_data = [row for row in contents if row[3:5] == "03"]
    march_data.insert(0, contents[0])
    with open("/Users/alisonkieselack/Projects/python_extension_challenges/01_files/program/AirQualityMarch.csv", "w") as file:
        file.writelines(f"{item}" for item in march_data)

#create_march_data(filename)

# Purpose: write monthly responses files to a new directory called "monthly_responses",
# in the same location as AirQuality.csv, each using the name format "mm-yyyy.csv",
# including the header row of labels in each one.
# Example
#   Call: create_monthly_responses("AirQuality.csv")
#   Returns: nothing, but files such as monthly_responses/05-2004.csv exist containing
#            data matching responses from that month and year
def create_monthly_responses(filename):
    contents = get_file_contents(filename)
    os.makedirs("/Users/alisonkieselack/Projects/python_extension_challenges/01_files/program/monthly_responses", exist_ok=True)

    ### my first attempt is below:
    # list_of_months = list(set([row.split(";")[0][3:10] for row in contents[1:]]))
    # for month in list_of_months:
    #     if month != "":
    #         month_data = [row for row in contents if row[3:10] == month]
    #         month_data.insert(0, contents[0])
    #         month_file_name = month.replace("/", "-")
    #         with open(f"/Users/alisonkieselack/Projects/python_extension_challenges/01_files/program/monthly_responses/{month_file_name}.csv", "w") as file:
    #             file.writelines(f"{item}" for item in month_data)

    ### my second attempt after asking chatgpt how to make it more efficient:
    header = contents[0]
    monthly_data = {}
    
    for row in contents[1:]:
        month = row.split(";")[0][3:10]
        if month:
            if month not in monthly_data:
                monthly_data[month] = []
            monthly_data[month].append(row)

    for month, rows in monthly_data.items():
        month_file_name = month.replace("/", "-")

        with open(f"/Users/alisonkieselack/Projects/python_extension_challenges/01_files/program/monthly_responses/{month_file_name}.csv", "w") as file:
            file.write(header)
            file.writelines(rows)


print(create_monthly_responses(filename))