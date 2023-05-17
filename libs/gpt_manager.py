# Import libraries
import openai, tiktoken, configparser, datetime, backoff
from latex_manager import get_input_text_groups, get_formatted_text, get_do_not_add_command_removed_text

# Define parameters
MAX_ALL_TOKENS = 8192
MAX_INPUT_TOKENS = 1000
OUTPUT_TOKENS = MAX_ALL_TOKENS - MAX_INPUT_TOKENS
SAFETY_FACTOR = 1.5

# Define parameters for backoff TODO: fix the behaviour of backoff
WAIT_MULTIPLIER = 2.0
MIN_WAIT_RANDOM_EXPONENTIAL = 180
MAX_WAIT_RANDOM_EXPONENTIAL = 5760

EMPTY_TEXT = ''

# Load the API key and the GPT model name
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
openai.api_key = config_ini['GPT']['API_KEY']
GPT_MODEL = config_ini['GPT']['GPT_MODEL']

# Set parameters for GPT
TEMPERATURE = 0
FREQUENCY_PENALTY = 0.7
PRESENCE_PENALTY = 0.0


# Set prompts for GPT

PROMPT_TEXT = '''
As an AI model, act like an expert in academic writing with proficiency in English.
Your task is to improve an academic paper given to you.
The improvement should focus on clarifying, simplifying, and strengthening the logical structure of the paper.
Feel free to rearrange and interweave sentences as needed to accomplish this task.

The paper is in LaTeX format.
You MUST adhere the seven rules below:

1) Include the whole revised text in your output.
2) Preserve the functionality of all LaTeX commands in the modified version.
3) Maintain the original form of quoted or cited texts. Do not make changes to them.
4) Keep lines starting with '%' in your output, ensuring they are at their original position.
5) Organize the sentences so that each one is on a separate line ending with a period '.'.
6) Do NOT write any new ideas and irrelevant sample text that does not correspond to the input text.
7) If unable to revise a particular text, return it in its original form.

The text you need to revise is given below:

'''


# get all the revised texts
def get_revised_text(in_text, in_i_start=0):
    n_times = _get_n_calculation_times(in_text)
    n_text_length = _get_n_text_length(in_text)
    n_letters = int(n_text_length / n_times) + 1
    this_input_text_groups = get_input_text_groups(in_text, n_letters)
    this_result_text = ''
    n_groups = len(this_input_text_groups)
    for i, this_input_text in enumerate(this_input_text_groups):
        if i >= in_i_start:
            print('% >>> processing index i =', i, '( of total:', n_groups-1, ') for revision')
            if this_input_text['is_target']:
                _print_input_text(this_input_text['data'])
                try:
                    this_tmp_text = _get_one_revised_text(this_input_text['data'])
                    this_tmp_text = get_do_not_add_command_removed_text(this_input_text['data'], this_tmp_text)
                    this_tmp_text = get_formatted_text(this_tmp_text)
                except Exception as e:
                    print('% Error:', e)
                    print('% If necessary, please change related parameter(s) and set in_i_start =', i, 'in the main() function and restart.')
                    return False, this_result_text
            else:
                this_tmp_text = this_input_text['data']
            this_tmp_text += '\n'
            print(this_tmp_text)
            this_result_text += this_tmp_text
    return True, this_result_text


# get one revised text
def _print_input_text(in_text):
    print('% > The next input text is:')
    for this_line in in_text.split('\n'):
        print('%%', this_line)


# get the number of calculation times
def _get_n_text_length(in_text):
    return len(in_text)


def _get_n_calculation_times(in_text):
    if in_text == EMPTY_TEXT:
        return 0
    else:
        this_sample_token_length = _get_token_length(in_text)
        return int((this_sample_token_length * SAFETY_FACTOR) / (MAX_INPUT_TOKENS - _get_token_length(PROMPT_TEXT))) + 1


def _get_token_length(in_text):
    enc = tiktoken.encoding_for_model(GPT_MODEL)
    tokens = enc.encode(in_text)
    return len(tokens)


# Define functions for exponential backoff
@backoff.on_exception(backoff.expo, openai.error.RateLimitError, factor=4, max_tries=8)
def completion_with_backoff(**kwargs):
    print('% > queried:', datetime.datetime.now())
    return openai.ChatCompletion.create(**kwargs)


# Define functions for the GPT model
def _get_one_revised_text(in_text):
    response = completion_with_backoff(
        model=GPT_MODEL,
        messages=[{'role': 'user', 'content': PROMPT_TEXT + in_text}],
        temperature=TEMPERATURE,
        max_tokens=OUTPUT_TOKENS,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY
    )
    return response['choices'][0]['message']['content']
