import time


# Function to read the file in a RAW format
def read_file_raw(file):
    f = open(file + '/w1_slave', 'r')
    file_lines = f.readlines()
    f.close()
    return file_lines


# Function to find the temperature in RAW format
def read_temp_raw(file):
    lines = read_file_raw(file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_raw = temp_string
        return temp_raw.rstrip("\n")
