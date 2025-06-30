import random
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import json
import os

# Configuração fixa para dimensão universal (compatível com a maioria das redes)
UNIFIED_DIMENSION = (1200, 1200)  # Tamanho quadrado padronizado

TITLE_COLOR = (0, 0, 0)
TEXT_COLOR = (30, 30, 30)

# Carrega dados do JSON
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Converte cor hex string para tupla RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Aplica máscara circular na foto
def circular_mask(image, size):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(image, size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

# Ajusta dinamicamente o tamanho da fonte do título e quebra linhas

def wrap_text(text, font, max_width, draw):
    lines = []
    for paragraph in text.split('\n'):
        line = []
        words = paragraph.split()
        while words:
            line.append(words.pop(0))
            w = draw.textlength(' '.join(line + words[:1]), font=font)
            if w > max_width:
                break
        lines.append(' '.join(line))
        if words:
            lines.extend(textwrap.wrap(' '.join(words), width=40))
    return lines

# Geração da arte com layout fixo
def generate_art(data, output_path=".", upload_path="."):
    WIDTH, HEIGHT = UNIFIED_DIMENSION

    FONT_PATH_BOLD = "./fonts/Montserrat-Bold.ttf"
    FONT_PATH_REGULAR = "./fonts/Montserrat-Regular.ttf"
    FONT_PATH_ICON = "./fonts/fontawesome-webfont.ttf"

    FONT_NORMAL = ImageFont.truetype(FONT_PATH_REGULAR, 36)
    FONT_SMALL = ImageFont.truetype(FONT_PATH_REGULAR, 28)
    FONT_ICON = ImageFont.truetype(FONT_PATH_ICON, 30)
    FONT_TITLE = ImageFont.truetype(FONT_PATH_BOLD, 52)
    
    backgrounds_dir = "./backgrounds"
    available_backgrounds = [
        f for f in os.listdir(backgrounds_dir)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    chosen_bg = random.choice(available_backgrounds)

    background = Image.open(os.path.join(backgrounds_dir, chosen_bg)).convert("RGBA")
    background = background.resize((WIDTH, HEIGHT))
    draw = ImageDraw.Draw(background, 'RGBA')

    margin_x = 60
    margin_top = 60

    # Texto fixo superior
    draw.text((225, margin_top), "Série de Seminários do INF", font=ImageFont.truetype(FONT_PATH_BOLD, 52), fill=TITLE_COLOR)

    # Título principal com highlight e quebra de linha
    y_title = 300
    max_title_width = WIDTH - 2 * margin_x
    title_lines = wrap_text(data['title'], FONT_TITLE, max_title_width, draw)
    line_height = FONT_TITLE.getsize('A')[1] + 10
    highlight_margin = 10
    highlight_color = hex_to_rgb(data.get('highlight_color', "#000000"))

    for i, line in enumerate(title_lines):
        line_width = draw.textlength(line, font=FONT_TITLE)
        x = margin_x
        y = y_title + i * line_height
        #draw.rectangle([x - highlight_margin, y - 5, x + line_width + highlight_margin, y + line_height], fill=highlight_color)
        draw.text((x, y), line, font=FONT_TITLE, fill=(0, 0, 0))

    # Palestrante
    #y_palestrante = y_title + len(title_lines) * line_height + 40
    y_palestrante = 500
    draw.text((margin_x, y_palestrante), f"Palestrante: {data['speaker']}", font=FONT_NORMAL, fill=TITLE_COLOR)

    # Informações com ícones
    infos = [
        ("\uf073", data['date'] ),
        ("\uf017", f"{data['time']} - duração {data['duration']}"),
        ("\uf144", "Transmissão online"),
        ("\uf0ac", data['stream_link']),
        ("\uf276", data.get('location', 'Local não informado')),
    ]

    y_info = 575
    max_info_width = 750  # ou ajuste conforme seu layout

    for icon, text_info in infos:
        # Se for o campo de localização (map-pin ou map-marker-alt), ajustar tamanho da fonte
        if icon == "\uf276":
            font_size = 30
            font = ImageFont.truetype(FONT_PATH_REGULAR, font_size)
            while draw.textlength(text_info, font=font) > max_info_width and font_size > 14:
                font_size -= 1
                font = ImageFont.truetype(FONT_PATH_REGULAR, font_size)
            draw.text((margin_x+5, y_info), icon, font=FONT_ICON, fill=TEXT_COLOR)
            draw.text((margin_x + 50, y_info), text_info, font=font, fill=TEXT_COLOR)
        else:
            draw.text((margin_x, y_info), icon, font=FONT_ICON, fill=TEXT_COLOR)
            draw.text((margin_x + 50, y_info), text_info, font=FONT_SMALL, fill=TEXT_COLOR)

        y_info += 45


    # Observação adicional
    if obs := data.get('observation'):
        draw.text((margin_x, y_info + 20), f"* {obs}", font=FONT_SMALL, fill=TEXT_COLOR)

    # Foto da palestrante com máscara circular
    photo_path = os.path.join(upload_path, data['photo'])
    photo = Image.open(photo_path).convert("RGBA")
    circle_photo = circular_mask(photo, (300, 300))
    shadow_posx=820
    shadow_posy=750
    background.paste(circle_photo, (860, 500), circle_photo)

    background.convert("RGB").save(os.path.join(output_path, "seminar_art.png"))

if __name__ == '__main__':
    data = load_data("input.json")
    generate_art(data)
