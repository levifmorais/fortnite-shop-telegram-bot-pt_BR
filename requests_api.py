import os
import requests
from PIL import Image, ImageOps
from io import BytesIO
from datetime import datetime, timezone, timedelta

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
    'legendary': (165, 93, 18),
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

    
    image_date = datetime.fromtimestamp(os.path.getmtime('imgs/loja.jpg')).astimezone(timezone.utc).date()

    now = datetime.now(timezone.utc).date() 

    if image_date != now:
        received_data = get_request_pt_br()
            
        banner = Image.open('imgs/banner.png')

        new_image = Image.new('RGBA',(banner.size))

        url = ''

        section_name = {}


        img_size = 512
        imgs_per_row = 10

        img_size_bundle = 1024
        imgs_per_row_bundle = 4

        width_per_row = img_size * imgs_per_row

        width_per_row_bundle = img_size_bundle * imgs_per_row_bundle
        
        new_image.paste(banner, (0, 0))

        x,y = 0,banner.height

        for section in received_data['data']:
            section_value = received_data['data'].get(section)
            
            if isinstance(section_value, dict):

                for entry in received_data['data'][section]['entries']:
                    if entry['bundle'] == None:
                            item = entry['items'][0]
                            
                            url = item['images']['icon']

                            response_image = requests.get(url)

                            image = Image.open(BytesIO((response_image.content)))
                            image = ImageOps.expand(image, border=15, fill='white')
                            image_bg = Image.new('RGBA', image.size, color = rarity_table[item['rarity']['value']])
                            
                            #TODO 
                            if x >= img_size * imgs_per_row:
                                x = 0
                                y += img_size

                            new_width = x + image.width
                            new_height = y + image.height
                                
                            combined_image = Image.new('RGBA', (width_per_row, new_height))
                            combined_image.paste(new_image, (0, 0))
                            combined_image.paste(image_bg, (x,y))
                            combined_image.paste(image, (x, y), image)
                            

                            x += img_size

                            new_image = combined_image
                
        x = 0
        y = y + img_size

        for section in received_data['data']:
            section_value = received_data['data'].get(section)

            if isinstance(section_value, dict):

                for entry in received_data['data'][section]['entries']:
                    if entry['bundle'] != None:
                        item = entry['items'][0]
                                
                        url = entry['bundle']['image']

                        response_image = requests.get(url)

                        image = Image.open(BytesIO((response_image.content)))

                        image = image.resize((img_size_bundle, img_size_bundle))

                        image = ImageOps.expand(image, border=15, fill='white')
                        image_bg = Image.new('RGBA', image.size, color = rarity_table[item['rarity']['value']])

                        if x >= img_size_bundle * imgs_per_row_bundle:
                            x = 0
                            y += img_size_bundle

                        new_width = x + image.width
                        new_height = y + image.height
                                    
                        combined_image = Image.new('RGBA', (width_per_row_bundle, new_height))
                        combined_image.paste(new_image, (0, 0))
                        combined_image.paste(image_bg, (x,y))
                        combined_image.paste(image, (x, y),image)
                                

                        x += img_size_bundle

                        new_image = combined_image
        

        #new_image = ImageOps.expand(new_image, border=30, fill='white')
        
        new_image = new_image.resize((new_image.width//4, new_image.height//4))

        new_image = new_image.convert('RGB').save('imgs/loja.jpg', 'JPEG')

    return 'imgs/loja.jpg'

get_image()


