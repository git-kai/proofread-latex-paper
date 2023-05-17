# Import libraries
import os, datetime


# Save the data in the text file
def save_txt_file(in_file_path, in_data):
    all_lines = in_data.split('\n')
    f = open(in_file_path, 'w')
    f.write('\n'.join(all_lines))
    f.close()


# Get the data from the text file
def get_file_text(in_file_path, in_encode):
    f = open(in_file_path, 'r', encoding=in_encode)
    data = f.read()
    f.close()
    return data


# Get the output file name with date
def get_output_file_name_with_date(in_output_file_name):
    now = datetime.datetime.now()
    basename, extension = os.path.splitext(in_output_file_name)
    new_filename = f'{basename}_{now:%Y%m%d_%H%M%S}{extension}'
    return new_filename
