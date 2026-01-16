import yaml
from pathlib import Path
from prompts.system_prompts import system_prompt_fr, \
                                   system_prompt_en, \
                                   system_prompt_de, \
                                   system_prompt_pl, \
                                   system_prompt_vn

from prompts.input_prompts import input_prompt1_fr, \
                                  input_prompt1_en, \
                                  input_prompt1_de, \
                                  input_prompt1_pl, \
                                  input_prompt1_vn, \
                                  input_prompt2_fr, \
                                  input_prompt2_en, \
                                  input_prompt2_de, \
                                  input_prompt2_pl, \
                                  input_prompt2_vn

from prompts.answer_prompts import answer_prompt1_fr, \
                                   answer_prompt1_en, \
                                   answer_prompt1_de, \
                                   answer_prompt1_pl, \
                                   answer_prompt1_vn, \
                                   answer_prompt2_fr, \
                                   answer_prompt2_en, \
                                   answer_prompt2_de, \
                                   answer_prompt2_pl, \
                                   answer_prompt2_vn, \
                                   answer_prompt3_fr, \
                                   answer_prompt3_en, \
                                   answer_prompt3_de, \
                                   answer_prompt3_pl, \
                                   answer_prompt3_vn

from prompts.system_prompts import system_prompt_fr, \
                                   system_prompt_en, \
                                   system_prompt_de, \
                                   system_prompt_pl, \
                                   system_prompt_vn

with open(Path('prompts') / f'category_prompts.yml', 'r', encoding = 'utf-8') as file:
    category_prompts = yaml.safe_load(file)
    
# 'prompt_type=definition1' => 'definition1'

def extract_prompt_type(txt):
    # print(txt)
    # print(txt[:txt.find('\n')].replace('prompt_type=', '').strip())
    # print(len((txt[:txt.find('\n')].replace('prompt_type=', '').strip())))
    # input('== ENTER ==')
    return txt[:txt.find('\n')].replace('prompt_type=', '').strip()

def extract_core_text(txt):
    position_url = txt.find('source_url=')
    return txt[txt.find('\n', position_url + 1) + 1:].strip()
    
def extract_url(txt):
    if 'source_url=' in txt:
        start = txt.find('source_url=') + 11
        return txt[start:txt.find('\n', start)].strip()
    else:
        return ''
    
def generate_prompt_input(txt, lang = 'en'):
    prompt_type = extract_prompt_type(txt)
    core_text = extract_core_text(txt)
    source_url = extract_url(txt)
    
    match lang:
        case 'en':
            input_prompt1 = input_prompt1_en
            input_prompt2 = input_prompt2_en
        case 'de':
            input_prompt1 = input_prompt1_de
            input_prompt2 = input_prompt2_de
        case 'pl':
            input_prompt1 = input_prompt1_pl
            input_prompt2 = input_prompt2_pl
        case 'vn':
            input_prompt1 = input_prompt1_vn
            input_prompt2 = input_prompt2_vn
            
    prompt_input = f'''{input_prompt1} {category_prompts[f'{prompt_type}_{lang}']} {input_prompt2} {core_text}'''
    
    return (prompt_input, prompt_type, source_url)


def generate_prompt_answer(txt, my_input, lang = 'en'):
    prompt_type = extract_prompt_type(txt)
    core_text = extract_core_text(txt)
    
    match lang:
        case 'en':
            answer_prompt1 = answer_prompt1_en
            answer_prompt2 = answer_prompt2_en
            answer_prompt3 = answer_prompt3_en
        case 'de':
            answer_prompt1 = answer_prompt1_de
            answer_prompt2 = answer_prompt2_de
            answer_prompt3 = answer_prompt3_de
        case 'pl':
            answer_prompt1 = answer_prompt1_pl
            answer_prompt2 = answer_prompt2_pl
            answer_prompt3 = answer_prompt3_pl
        case 'vn':
            answer_prompt1 = answer_prompt1_vn
            answer_prompt2 = answer_prompt2_vn
            answer_prompt3 = answer_prompt3_vn

            
    return f'''{answer_prompt1}{core_text}

{answer_prompt2} {my_input}
{answer_prompt3}'''


def generate_system_prompt(lang = 'en'):
    match lang:
        case 'en':
            system_prompt = system_prompt_en
        case 'de':
            system_prompt = system_prompt_de
        case 'pl':
            system_prompt = system_prompt_pl
        case 'vn':
            system_prompt = system_prompt_vn
    return system_prompt