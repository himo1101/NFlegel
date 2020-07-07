import json

def load_json(filename:str):
    try:
        with open(f'config/{filename}.json', encoding='utf-8') as f:
            return json.load(f)
             
    except OSError:
        mes = {}
        save(mes, filename)


def save(contents, filename:str):
        
    with open(f'config/{filename}.json', 'w', encoding='utf-8') as f:
        return json.dump(contents, f, ensure_ascii=False, indent=4)


def nsfw_load_json(filename:str):
    try:
        with open(f'config/nsfw/{filename}.json', encoding='utf-8') as f:
            return json.load(f)
    
    except OSError:
        mes = {}
        nsfw_save(mes, filename)

    
def nsfw_save(contents, filename:str):
    with open(f'config/nsfw/{filename}.json', 'w', encoding='utf-8') as f:
        return json.dump(contents, f, ensure_ascii=False, indent=4)