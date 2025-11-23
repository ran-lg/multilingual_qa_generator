from sys import argv
from datetime import datetime

from os import listdir, mkdir
from os.path import exists, isdir
from pathlib import Path

from openai import OpenAI

from generate_txt_files import delete_existing_files, \
                               create_files
                               
from instruction_generator import generate_prompt_answer, \
                                  generate_prompt_input, \
                                  generate_system_prompt

import yaml

TEXT_FOLDER = 'tmp'
FILE_TO_PARSE = 'base.txt'
TXT_TARGET_FILENAME = 'output.txt'
TEMPERATURE = 0.7


with open('.deepseek-config.yml', 'r') as file:
    login_data_ds = yaml.safe_load(file)

def instantiate_llm(temperature):
    return OpenAI(api_key = login_data_ds['api_key'], base_url = login_data_ds['openai_api_base'])

def prompt_llm(client, user_prompt, system_prompt = None):
    if system_prompt is None:
        response = client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "user", "content": user_prompt},
            ],
            stream = False
        )
    else:
        response = client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream = False
        )
    return response.choices[0].message.content
    
def main(lang = 'en'):
    if not isdir(TEXT_FOLDER):
        mkdir(TEXT_FOLDER)

    client = instantiate_llm(TEMPERATURE)   

    delete_existing_files(TEXT_FOLDER)
    create_files(FILE_TO_PARSE, TEXT_FOLDER)
    
    txt_files = [Path(TEXT_FOLDER) / file for file in listdir(TEXT_FOLDER)]
    
    data = []
    prompt_types = set()
    
    for i, txt_file in enumerate(txt_files, 1):
       
        with open(txt_file, 'r', encoding = 'utf-8') as f:
            txt = f.read()
       
        system_prompt = generate_system_prompt(lang = lang)
                
        prompt_input, prompt_type, source_url = generate_prompt_input(txt, lang = lang)
        q = prompt_llm(client, prompt_input, system_prompt = system_prompt)
        
        prompt_answer = generate_prompt_answer(txt, q, lang = lang)
        a = prompt_llm(client, prompt_answer, system_prompt = system_prompt)
                     
        data.append({'prompt_type': prompt_type, 'q': q, 'a': a})
        prompt_types.add(prompt_type)
        
        print('\nPROMPT INPUT\n')
        print(prompt_input + '\n')
        print('\nSYSTEM PROMPT\n')
        print(system_prompt + '\n')
        print('\nPROMPT ANSWER\n')
        print(prompt_answer + '\n')
        print('\n=================\n')
        print(q + '\n')
        print(a)
        print('\n=================\n')
                
    all_q = ['Q', '\n']
    all_a = ['A', '\n']
    
    for i, element in enumerate(data, 1):
            all_q.append(f"{i}) {element['q']}\n")
            all_a.append(f"{i}) {element['a']}\n")
        
    with open(TXT_TARGET_FILENAME, 'w', encoding = 'utf-8') as f:
        f.writelines(all_q + ['\n', '\n'] + all_a)
    
    
    
if __name__ == "__main__":
    try:
        lang = str(argv[1])
    except (IndexError, ValueError):
        lang = 'en'

    main(lang)