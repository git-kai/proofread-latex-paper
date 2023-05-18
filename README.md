# Proofread-LaTeX-Paper

This repository provides a tool for proofreading academic papers in LaTeX format using GPT model.
The entire text is proofread by dividing the text by a certain length and repeatedly requesting to the model.

## Basic

### _Python Environment_
We highly recommend using Python 3.11 for the best performance. It is also advisable to operate within a virtual environment when executing the code.

### _Code Installation_

1. Install Git on your computer if not already installed. 
2. Clone the repository using git clone as follows:
```
git clone https://github.com/git-kai/proofread-latex-paper.git.
```

### _Libraries Installation_
To install all necessary libraries, please execute the following command:
```
pip install -r requirements.txt
```

### _GPT Model Configuration_
1. Make a duplicate of the `config.default.ini` file and rename this duplicate to `config.ini`.
2. Open the `config.ini` file and insert your unique OpenAI API key into the `API_KEY` field. Remember not to enclose the key in quotation marks ("").
3. For the `GPT_MODEL` setting, our recommendation is to use `gpt-4`.

### _Setting up the LaTeX Paper for Proofreading_
1. Specify the path to the directory containing your target file in the `TARGET_FOLDER` field. For instance, if you have a folder named "target_folder" in the same directory as `main.py`, you would set `TARGET_FOLDER` to `./target_folder`.
2. Input the name of your LaTeX file in the `TARGET_FILE_NAME` field.
3. Adjust the `FILE_ENCODE` parameter to match the encoding of your file, if needed.

### _Target Text for Proofreading_
This tool is designed to proofread and revise the text within LaTeX academic papers, with the exception of the following sections:
* Preamble (any parts before the `\begin{document}`)
* Figures
* Tables
* References

### _Running the Tool_
To run the proofreading tool, execute the `main.py` file with Python.

### _Getting Output_
The revised file is saved within the same directory as the original file. The output file's name includes the date Ωfor easy tracking. For example, if the input file is 'document.tex', then the output file will be such as "document_20230516_161112.tex".

## Advanced

### _Customizing the GPT Model Settings_
If you wish to customize the GPT model's settings, such as the Prompt Text, you can do so by modifying the respective values in the `proofread-latex-paper/libs/gpt_manager.py` file.

### _Visualizing the differences_

To check the revised parts, we recommend using a third-party tool such as `latexdiff`[1].

[1] https://www.ctan.org/pkg/latexdiff

## Caution!
Please check the policy of the journal or conference to which you intend to submit your paper.
It is probable that the policies prohibit the use of LLM.
