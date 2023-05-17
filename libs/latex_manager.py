# Define functions

# define constants to replace some words in the GPT model's output
LATEX_FORMAT_REPLACEMENTS = [
    (' "', ' ``'),
    ('"', "'' "),
    ('."', ".''"),
    (',"', ",''"),
    ('".', ".''"),
    (',"', ",''"),
    ('",', ",''"),
    (" '", " `"),
    ('"', '``'),
    ('—', '--')
]

# define constants to remove commands that GPT model add without permission
DO_NOT_ADD_COMMAND = [
    '\\end{document}'
]

# define constants to detect empty lines
EMPTY_LINE = ''
VARIOUS_EMPTY_LINE_LIST = ['', ' ', '%', '% ', '\n', '\t', '\r\n']


# get the preamble and body and references separately from the text
def get_tex_preamble_body_references(in_text):
    this_preamble = ''
    this_body = ''
    this_references = ''
    all_lines = in_text.splitlines()
    is_preamble = True
    is_references = False
    for this_line in all_lines:
        # Check where the line belongs to
        if this_line.startswith('\\begin{document}'):
            is_preamble = False
        elif this_line.startswith('\\bibliographystyle') or this_line.startswith('\\begin{thebibliography}'):
            is_references = True
        # Add the line to the appropriate section
        if is_preamble:
            this_preamble += this_line + '\n'
        elif is_references:
            this_references += this_line + '\n'
        else:
            this_body += this_line + '\n'
    return {'preamble': this_preamble, 'body': this_body, 'references': this_references}


# get groups of input texts in the json from
def get_input_text_groups(in_text, in_max_letters):
    results_groups = []
    this_group = []
    n_letters = 0
    is_figure_or_table = False
    # Split the text into lines
    for line in in_text.split('\n'):
        # Check if the line contains a figure or table tag
        if '\\begin{figure}' in line or '\\begin{table}' in line:
            # End the current group if there was one
            results_groups = _get_all_groups_appended_new_group(results_groups, this_group, True)
            this_group = [line]
            is_figure_or_table = True
        # Check if the line contains an end figure or table tag
        elif '\\end{figure}' in line or '\\end{table}' in line:
            # End the current group
            this_group.append(line)
            results_groups = _get_all_groups_appended_new_group(results_groups, this_group, False)
            this_group = []
            is_figure_or_table = False
        # Add the line to the current group if we are in a figure or table
        elif is_figure_or_table:
            this_group.append(line)
        # Otherwise, we are in regular text
        else:
            # Count the number of letters in the line
            n_letters += len(line)
            # If the line exceeds the maximum number of letters and the end of the paragraph, end the current group
            if n_letters > in_max_letters and line == EMPTY_LINE:
                # End the current group if there was one
                results_groups = _get_all_groups_appended_new_group(results_groups, this_group, True)
                this_group = []
                n_letters = 0
            # Add the line to the current group except for the empty line
            this_group.append(line)
    # If there is still a current group, add it to the list of results_groups
    results_groups = _get_all_groups_appended_new_group(results_groups, this_group, True)
    return results_groups


# append a new group to the list of all groups
def _get_all_groups_appended_new_group(in_all_groups, in_new_group, is_target=True):
    if _is_meaningful_group(in_new_group):
        in_all_groups.append({'data': "\n".join(in_new_group), 'is_target': is_target})
    return in_all_groups


# check if the group is meaningful
def _is_meaningful_group(in_group):
    for line in in_group:
        if line not in VARIOUS_EMPTY_LINE_LIST:
            return True
    return False


# get the text formatted by the LATEX_FORMAT_REPLACEMENTS
def get_formatted_text(in_text):
    for old, new in LATEX_FORMAT_REPLACEMENTS:
        in_text = in_text.replace(old, new)
    return in_text


# get the text without the commands that GPT model add without permission defined in DO_NOT_ADD_COMMAND
def get_do_not_add_command_removed_text(in_original_text, in_revised_text):
    for this_command in DO_NOT_ADD_COMMAND:
        if in_original_text.find(this_command) == -1:
            return in_revised_text.replace(this_command, '')
    return in_revised_text
