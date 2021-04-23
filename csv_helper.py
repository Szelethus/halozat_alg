import csv
from datetime import datetime

def create_new_file_with_column_names(filename, rownames):
    with open(filename + '.csv', mode='a') as test_data:
        data_writer = csv.writer(test_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(rownames)

def write_new_datas(filename, values):
    with open(filename + '.csv', mode='a', newline='') as test_data:
        data_writer = csv.writer(test_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(create_str_from_values(values))
    
def create_str_from_values(values):
    rowvalues = []
    for i in values:
        rowvalues.append(str(i))
    return rowvalues

def create_unique_filename(filename):
    return filename + str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))

def opencsv(filename):   
    create_new_file_with_column_names(filename, ['number of edges', 'number of nodes', 'graph density', 'number of spanning tree leaves'])

