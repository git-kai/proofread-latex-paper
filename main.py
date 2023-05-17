####################
# import libraries #
####################
import configparser
from libs.gpt_manager import get_revised_text
from libs.file_manager import get_file_text, save_txt_file, get_output_file_name_with_date
from libs.latex_manager import get_tex_preamble_body_references


##################
# set parameters #
##################
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
TARGET_FOLDER = config_ini['FILE']['TARGET_FOLDER']
INPUT_FILE_NAME = config_ini['FILE']['INPUT_FILE_NAME']
FILE_ENCODE = config_ini['FILE']['FILE_ENCODE']


###################
# Define function #
###################
def main(in_i_start=0):
    this_result = ''
    this_input_file_path = TARGET_FOLDER + '/' + INPUT_FILE_NAME
    print('% >>>>> START REVISION >>>>>', this_input_file_path)
    this_input_text = get_file_text(this_input_file_path, FILE_ENCODE)
    this_preamble_body_references = get_tex_preamble_body_references(this_input_text)
    if in_i_start == 0:
        print('% >>> preamble\n', this_preamble_body_references['preamble'])
        this_result = this_preamble_body_references['preamble']
    is_all_revised, this_revised_text = get_revised_text(this_preamble_body_references['body'], in_i_start)
    if not is_all_revised:
        this_result += '\n' + this_revised_text
    else:
        print('% >>> references\n', this_preamble_body_references['references'])
        this_result += '\n' + this_revised_text + '\n' + this_preamble_body_references['references']
    this_output_file_path = TARGET_FOLDER + '/' + get_output_file_name_with_date(INPUT_FILE_NAME)
    save_txt_file(this_output_file_path, this_result)


################
# Run function #
################

# If necessary, set in_i_start for the main function where you want to restart.

main(in_i_start=0)
