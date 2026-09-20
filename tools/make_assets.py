import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(BASE, 'assets')
os.makedirs(ASSETS, exist_ok=True)

BG = (23, 26, 33)
BG_SOFT = (36, 39, 51)
GRID = (92, 104, 128)
GRID_SUB = (54, 59, 70)
ACCENT = (74, 160, 245)
X_COLOR = (245, 92, 94)
O_COLOR = (89, 212, 140)
GOLD = (255, 212, 74)


def draw_board(draw, origin, size, cell, filled):
    ax, ay = origin
    for i in range(10):
        strong = i % 3 == 0
        color = GRID if strong else GRID_SUB
        width = max(cell // 6, 1) if strong else max(cell // 16, 1)
        draw.line([(ax + i * cell, ay), (ax + i * cell, ay + size)], fill=color, width=width)
        draw.line([(ax, ay + i * cell), (ax + size, ay + i * cell)], fill=color, width=width)
    for (bi, r, c) in filled:
        bx = ax + (bi % 3) * 3 * cell
        by = ay + (bi // 3) * 3 * cell
        x = bx + c * cell
        y = by + (2 - r) * cell
        draw_mark(draw, 'X', x, y, cell)


def draw_mark(draw, ch, x, y, cell):
    inset = cell * 0.24
    width = max(int(cell // 7), 2)
    i = int(inset)
    cx0 = int(x)
    cy0 = int(y)
    cs = int(cell)
    if ch == 'X':
        draw.line([(cx0 + i, cy0 + i), (cx0 + cs - i, cy0 + cs - i)], fill=X_COLOR, width=width)
        draw.line([(cx0 + cs - i, cy0 + i), (cx0 + i, cy0 + cs - i)], fill=X_COLOR, width=width)
    else:
        d = int(cs / 2 - i)
        cx = int(cx0 + cs / 2)
        cy = int(cy0 + cs / 2)
        draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=O_COLOR, width=width)


def make_icon(path):
    size = 512
    image = Image.new('RGB', (size, size), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=90, fill=BG)
    margin = 96
    board = size - margin * 2
    cell = board / 9.0
    ox = margin
    oy = margin
    draw.rounded_rectangle([ox - 8, oy - 8, ox + board + 8, oy + board + 8], radius=28, fill=BG_SOFT)
    center_bx = ox + 3 * cell
    center_by = oy + 3 * cell
    draw.rounded_rectangle([center_bx, center_by, center_bx + 3 * cell, center_by + 3 * cell],
                           radius=int(cell * 0.5), fill=(44, 74, 112, 255))
    marks = [(4, 0, 0, 'X'), (4, 0, 1, 'O'), (0, 2, 2, 'X'), (8, 0, 0, 'O'), (5, 1, 1, 'X')]
    for bi, r, c, ch in marks:
        bx = ox + cell * 3 * (bi % 3) + c * cell
        by = oy + cell * 3 * (bi // 3) + (2 - r) * cell
        draw_mark(draw, ch, bx, by, cell)
    vx = ox + 3 * cell
    vy = oy
    draw.line([(vx + cell / 2, vy + cell / 2), (vx + 3 * cell - cell / 2, vy + 3 * cell - cell / 2)],
              fill=GOLD, width=max(int(cell / 6), 4))
    image.save(path, 'PNG')
    print('icon ->', path)


def make_presplash(path):
    width, height = 1280, 720
    image = Image.new('RGB', (width, height), BG)
    draw = ImageDraw.Draw(image)
    board = 420
    cell = board / 9.0
    ox = (width - board) / 2
    oy = 120
    draw.rounded_rectangle([ox - 10, oy - 10, ox + board + 10, oy + board + 10], radius=20, fill=BG_SOFT)
    for i in range(4):
        pos = int((i + 1) / 3 * board)
        draw.line([(ox + pos, oy), (ox + pos, oy + board)], fill=GRID, width=3)
        draw.line([(ox, oy + pos), (ox + board, oy + pos)], fill=GRID, width=3)
    marks = [(0, 0, 0, 'X'), (1, 1, 2, 'O'), (3, 2, 0, 'X'), (4, 0, 1, 'O'), (5, 2, 2, 'X'), (8, 1, 0, 'O')]
    for bi, r, c, ch in marks:
        bx = ox + cell * 3 * (bi % 3) + c * cell
        by = oy + cell * 3 * (bi // 3) + (2 - r) * cell
        draw_mark(draw, ch, bx, by, cell)
    draw_text(draw, width / 2, 588, 'TIC TAC TOWER', 92, (235, 240, 250))
    draw_text(draw, width / 2, 665, 'Ultimate Tic-Tac-Toe', 40, ACCENT)
    image.save(path, 'PNG')
    print('presplash ->', path)


def draw_text(draw, cx, y, text, size, color):
    font_path = 'C:/Windows/Fonts/segoeuib.ttf'
    font = ImageFont.truetype(font_path, size)
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text((cx - (bbox[2] - bbox[0]) / 2, y), text, font=font, fill=color)


make_icon(os.path.join(ASSETS, 'icon.png'))
make_presplash(os.path.join(ASSETS, 'presplash.png'))
print('ASSETS LISTO')