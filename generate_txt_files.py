from pathlib import Path
from os import listdir, remove


# use a str block to generate the basis texts

def generate_n_txt(block: 'str'):
    if not 'prompt_type=' in block:
        return []
    else:
        prompt_type_line = block[0:block.find('\n')]
        prompt_types = prompt_type_line.replace('prompt_type=', '').strip().split(' ')
        txts = [block.replace(prompt_type_line, f'prompt_type={prompt_type}') for prompt_type in prompt_types]
        return txts

# empty TEXT_FOLDER

def delete_existing_files(TEXT_FOLDER):   
    files = [Path(TEXT_FOLDER) / file for file in listdir(TEXT_FOLDER)]
    for file in files:
        file.unlink()
    print(f'Files deleted in folder /{TEXT_FOLDER}/.')

# use FILE_TO_PARSE to create the required .txt files in TEXT_FOLDER

def create_files(FILE_TO_PARSE, TEXT_FOLDER):
    # parse FILE_TO_PARSE
    
    with open(FILE_TO_PARSE, 'r', encoding = 'utf-8') as f:
        text = f.read()
    
    if text[0] == '@':
        text = text[1:]
        
    blocks = text.split('@')   
    
    # create .txt files in TEXT_FOLDER
    
    i = 0
    for block in blocks:
        txts = generate_n_txt(block)
        
        for txt in txts:
            filename = Path(TEXT_FOLDER) / f'text_{str(i)}.txt'
            with open(filename, 'w', encoding = 'utf-8') as f:
                f.write(txt)
            i += 1
    
    print(f'{i} files generated in folder /{TEXT_FOLDER}/.')

if __name__ == '__main__':
    delete_existing_files('tmp')
    create_files('base.txt', 'tmp')