import requests
from PIL import Image
from io import BytesIO
#from datetime import datetime

type_table = {
    'outfit': 'Skin',
    'backpack': 'Mochila',
    'pickaxe': 'Picareta',
    'emote': 'Emote',
    'glider': 'Asa-delta',
    'wrap': 'Envelopamento',
    'music': 'Música'
}

rarity_table = {
    'common': (85, 89, 88),
    'uncommon': (110, 170, 42),
    'rare': (22, 133, 181),
    'epic': (99, 16, 148),
    'legendary': (185, 19, 162),
    'marvel': (144, 46, 42),
    'dc': (55, 76, 131),
    'icon': (66, 156, 151),
    'frozen': (26, 108, 141),
    'lava': (145, 68, 39),
    'starwars': (24, 41, 77),
    'shadow': (32, 34, 34),
    'slurp': (40, 191, 145),
    'gaminglegends': (54, 43, 143)
}



def get_request_pt_br() -> str:
    response = requests.get(url='https://fortnite-api.com/v2/shop/br/combined', params={'language': 'pt-BR'})

    return response.json()

# Função que pega a loja atual do fortnite, é esperado retornar uma string
def get_shop() -> str:
    
    received_data = get_request_pt_br()
        
    text = ''

    section_name = {}

    for section in received_data['data']:
        section_value = received_data['data'].get(section)
        

        if isinstance(section_value, dict):

            for entry in received_data['data'][section]['entries']:
                
                entry_section = entry['section']['name']

                if entry_section not in section_name:
                    section_name[entry_section] = []

                if entry['bundle'] == None:
                    item = entry['items'][0]
                    name = item['name']
                    price = entry['finalPrice']
                    item_type = item['type']['value']

                    section_name[entry_section].append(f"\n{name} - {price} Vbucks - {type_table[item_type]}\n")

                else:
                    section_name[entry_section].append(f"\n{entry['bundle']['name']} - {entry['finalPrice']} Vbucks\n")

    for key, value in section_name.items():
        text += f"\n\n{key.capitalize()}\n\n"
        for item in value:
            text += item

    return text

def get_image():

        
    received_data = get_request_pt_br()
        
    new_image = Image.new('RGBA',(0,0))

    url = ''

    section_name = {}

    for section in received_data['data']:
        section_value = received_data['data'].get(section)

        if isinstance(section_value, dict):

            for entry in received_data['data'][section]['entries']:
                if entry['bundle'] == None:
                        item = entry['items'][0]
                        
                        url = item['images']['icon']

                        white = (255, 255, 255)

                        response_image = requests.get(url)

                        image = Image.open(BytesIO((response_image.content)))
                        image_bg = Image.new('RGBA', image.size, color = rarity_table[item['rarity']['value']])

                        width, height = new_image.size
                        
                        new_width = width + image.width
                        new_height = max(height,image.height)

                        combined_image = Image.new('RGBA', (new_width, new_height))
                        combined_image.paste(new_image, (0, 0))
                        combined_image.paste(image_bg, (width, 0))
                        combined_image.paste(image, (width, 0), image)

                        new_image = combined_image

    new_image.save('imgs/teste.png')

    return 'imgs/teste.png'

get_image()