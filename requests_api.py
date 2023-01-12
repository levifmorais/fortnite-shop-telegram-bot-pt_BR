import os
import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime, timezone, timedelta

# Dicionário que contém os tipos de itens e seus nomes em português
type_table = {
    'outfit': 'Skin',
    'backpack': 'Mochila',
    'pickaxe': 'Picareta',
    'emote': 'Emote',
    'glider': 'Asa-delta',
    'wrap': 'Envelopamento',
    'music': 'Música'
}

# Dicionário que contém as raridades e suas cores em RGB
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

# Retorna um dicionário com os dados da loja atual
def get_request_pt_br() -> str:
    response = requests.get(url='https://fortnite-api.com/v2/shop/br/combined', params={'language': 'pt-BR'})

    return response.json()

def write(image, text, x, y, font_size, align_pos):
    image_with_write = ImageDraw.Draw(image)
    font = ImageFont.truetype('LUCKIESTGUY-REGULAR.TTF',font_size)
    image_with_write.text((x, y), text, font=font, fill='white', align=align_pos)

# Função que pega a loja atual do fortnite em texto, é esperado retornar uma string
def get_shop_txt() -> str:
    
    received_data = get_request_pt_br()
        
    text = ''


    # O código visualiza as seções da loja que possuem itens dentro para formar a imagem,
    # se o item for parte de um pacote, é apenas adquirido o nome do pacote.
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

    # Formatação do texto
    for key, value in section_name.items():
        text += f"\n\n{key.capitalize()}\n\n"
        for item in value:
            text += item

    return text


# Função que pega a loja atual do fortnite em imagem.
def get_shop():

    # Verifica se a imagem da loja do dia já foi criada, se a imagem for anterior ao dia atual (UTC),
    # uma nova imagem é criada. Se a imagem não existir, a função é iniciada para gerar uma.
    try:
        image_date = datetime.fromtimestamp(os.path.getmtime('src/imgs/loja.jpg')).astimezone(timezone.utc).date()
    except:
        image_date = None

    now = datetime.now(timezone.utc).date() 

    if image_date != now or not image_date:
        
        received_data = get_request_pt_br()
        
        # Banner do projeto, a imagem final se adequa ao tamanho do banner.
        banner = Image.open('src/imgs/banner.png')
        
        # Texto do dia da loja
        write(banner, f'{now.day}/{now.month}/{now.year}', banner.width/2 - (120 * 2), banner.height - (120 * 2), 120, 'left')

        new_image = Image.new('RGBA',(banner.size))

        new_image.paste(banner, (0, 0))

        url = ''

        # Tamanho de cada imagem individual adquirida pela API e a quantidade de imagens por linha,
        # a largura se adequa se a seção for de pacotes ou não.
        img_size = 512
        imgs_per_row = 8

        img_size_bundle = 1024
        imgs_per_row_bundle = 4

        width_per_row = img_size * imgs_per_row

        width_per_row_bundle = img_size_bundle * imgs_per_row_bundle
        

        x,y = 0,banner.height

        vbuck_icon = requests.get(received_data['data']['vbuckIcon'])
        vbuck_icon = Image.open(BytesIO((vbuck_icon.content)))
        vbuck_icon = vbuck_icon.resize((90,90))


        # Adiciona primeiro a imagem os itens individuais, depois de adicionar todas as imagens individuais,
        # um novo loop é iniciado para adicionar apenas os pacotes.
        for section in received_data['data']:
            section_value = received_data['data'].get(section)
            
            if isinstance(section_value, dict):

                for entry in received_data['data'][section]['entries']:
                    if entry['bundle'] == None:
                            item = entry['items'][0]
                            
                            url = item['images']['icon']

                            response_image = requests.get(url)

                            # Cria uma borda para a imagem e um background com a cor da respectiva raridade do item
                            image = Image.open(BytesIO((response_image.content)))
                            image = ImageOps.expand(image, border=15, fill='white')

                            mask_image = image.copy()
                            shadow_bar = ImageDraw.Draw(mask_image)
                            shadow_bar.rectangle([0, image.height, image.width, image.height - 120], fill='black')
                            image = Image.blend(image, mask_image, 0.4)
                            
                            image.paste(vbuck_icon, (20, image.height - 120), vbuck_icon)
                            write(image,str(entry['finalPrice']), vbuck_icon.width + 30, image.height - 110, 100, 'right')

                            image_bg = Image.new('RGBA', image.size, color = rarity_table[item['rarity']['value']])
                            
                            if x >= img_size * imgs_per_row:
                                x = 0
                                y += img_size
                            
                            # Como a largura ja está definida, apenas a altura é modificada a cada item adicionado
                            new_height = y + image.height
                            
                            # Uma nova imagem é criada com a nova altura
                            combined_image = Image.new('RGBA', (width_per_row, new_height))
                            combined_image.paste(new_image, (0, 0))
                            combined_image.paste(image_bg, (x,y))
                            combined_image.paste(image, (x, y), image)
                            
                            # Atualiza a posicao x para a proxima imagem
                            x += img_size

                            new_image = combined_image
        
        # Reseta as variaveis para a secao de pacotes
        x = 0
        y = y + img_size

        # Mesmo codigo da situacao anterior apenas para os pacotes
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

                        mask_image = image.copy()
                        shadow_bar = ImageDraw.Draw(mask_image)
                        shadow_bar.rectangle([0, image.height, image.width, image.height - 120], fill='black')
                        image = Image.blend(image, mask_image, 0.4)
                        
                        image.paste(vbuck_icon, (20, image.height - 120), vbuck_icon)
                        write(image,str(entry['finalPrice']), vbuck_icon.width + 30, image.height - 110, 100, 'right')


                        image_bg = Image.new('RGBA', image.size, color = rarity_table[item['rarity']['value']])

                        if x >= img_size_bundle * imgs_per_row_bundle:
                            x = 0
                            y += img_size_bundle

                        new_height = y + image.height
                                    
                        combined_image = Image.new('RGBA', (width_per_row_bundle, new_height))
                        combined_image.paste(new_image, (0, 0))
                        combined_image.paste(image_bg, (x,y))
                        combined_image.paste(image, (x, y),image)
                                

                        x += img_size_bundle

                        new_image = combined_image
        

        #new_image = ImageOps.expand(new_image, border=30, fill='white')
        
        new_image = new_image.resize((new_image.width//4, new_image.height//4))

        new_image_bg = Image.new('RGBA', new_image.size, color = 'white')

        new_image_bg.paste(new_image, (0,0), new_image)

        new_image = new_image_bg
        

        new_image = new_image.convert('RGB').save('src/imgs/loja.jpg', 'JPEG')

    return 'src/imgs/loja.jpg'

# TODO
get_shop()