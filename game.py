import pygame
import sys
import os

# ПЕРЕКЛЮЧАТЕЛЬ РЕЖИМА: True = с багами (для сдачи), False = идеальная (для себя)
BUGGY_MODE = True

# Инициализация Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Подземелье Забытых Багов 2D")
clock = pygame.time.Clock()

# Шрифты
font_small = pygame.font.SysFont("arial", 20)

# Цвета
COLOR_UI_BG = (20, 20, 30)
COLOR_UI_BORDER = (100, 100, 120)
COLOR_TEXT = (255, 255, 255)
COLOR_BTN = (60, 60, 80)
COLOR_BTN_HOVER = (80, 80, 110)
COLOR_GOLD = (255, 215, 0)

# Загрузка изображений
def load_image(name):
    if not os.path.exists(name):
        print(f"ОШИБКА: Файл {name} не найден! Скачай картинки и положи их в папку с кодом.")
        pygame.quit()
        sys.exit()
    return pygame.image.load(name).convert_alpha()

# Загрузка всех фонов
bg_entrance = pygame.transform.scale(load_image("bg_cave.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_fork = pygame.transform.scale(load_image("bg_fork.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_skeleton_room = pygame.transform.scale(load_image("bg_skeleton.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_merchant_room = pygame.transform.scale(load_image("bg_merchant.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_boss_lair = pygame.transform.scale(load_image("bg_boss_lair.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_treasure = pygame.transform.scale(load_image("bg_treasure.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка персонажей
img_skeleton = pygame.transform.scale(load_image("char_skeleton.png"), (300, 500))
img_merchant = pygame.transform.scale(load_image("char_merchant.png"), (700, 600))

# Игровые переменные
hp = 50 if BUGGY_MODE else 100
max_hp = 100
gold = 0
has_sword = False
searched_entrance = False
skeleton_defeated = False
dragon_defeated = False
location = "entrance"
current_text = "Ты стоишь у входа в темную пещеру. Что будем делать?"
current_image = None
buttons = []

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def get_current_background():
    if location == "fork":
        return bg_fork
    elif location in ["boss", "win", "die_boss", "run_boss"]:
        return bg_treasure if dragon_defeated else bg_boss_lair
    elif location in ["monster", "fight"]:
        return bg_skeleton_room
    elif location in ["merchant", "buy_sword", "buy_potion"]:
        return bg_merchant_room
    else:
        return bg_entrance

def update_ui():
    global buttons
    
    current_bg = get_current_background()
    screen.blit(current_bg, (0, 0))
    
    if current_image:
        img_x = (SCREEN_WIDTH - current_image.get_width()) // 2
        img_y = SCREEN_HEIGHT - current_image.get_height() - 180
        screen.blit(current_image, (img_x, img_y))

    ui_rect = pygame.Rect(0, SCREEN_HEIGHT - 180, SCREEN_WIDTH, 180)
    pygame.draw.rect(screen, COLOR_UI_BG, ui_rect)
    pygame.draw.line(screen, COLOR_UI_BORDER, (0, ui_rect.top), (SCREEN_WIDTH, ui_rect.top), 3)

    stats_text = f"HP: {hp}/{max_hp}  |  Золото: {gold}  |  Меч: {'Да' if has_sword else 'Нет'}"
    screen.blit(font_small.render(stats_text, True, COLOR_GOLD), (20, ui_rect.top + 10))

    lines = wrap_text(current_text, font_small, SCREEN_WIDTH - 40)
    for i, line in enumerate(lines):
        screen.blit(font_small.render(line, True, COLOR_TEXT), (20, ui_rect.top + 40 + i * 25))

    btn_y = ui_rect.top + 110
    btn_width = (SCREEN_WIDTH - 60) // len(buttons) if buttons else 0
    for i, (btn_text, btn_action) in enumerate(buttons):
        btn_rect = pygame.Rect(20 + i * (btn_width + 10), btn_y, btn_width, 50)
        mouse_pos = pygame.mouse.get_pos()
        color = COLOR_BTN_HOVER if btn_rect.collidepoint(mouse_pos) else COLOR_BTN
        pygame.draw.rect(screen, color, btn_rect, border_radius=8)
        text_surf = font_small.render(btn_text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=btn_rect.center)
        screen.blit(text_surf, text_rect)

def set_location(loc):
    global hp, max_hp, gold, has_sword, searched_entrance, skeleton_defeated
    global dragon_defeated, location, current_text, current_image, buttons
    
    location = loc
    buttons = []
    
    txt_search = "Обыскать ваход" if BUGGY_MODE else "Обыскать вход"
    txt_back = "Вурнуться" if BUGGY_MODE else "Вернуться"
    txt_attack = "Атакавать!" if BUGGY_MODE else "Атаковать!"
    txt_merchant_intro = "Ты встречаешь Старого Тарговца. Он довольно потирает руки." if BUGGY_MODE else "Ты встречаешь Старого Торговца. Он довольно потирает руки."

    if loc == "entrance":
        current_text = "Ты стоишь у входа в темную пещеру. Пахнет сыростью и приключениями."
        current_image = None
        buttons = [("Войти в пещеру", "fork"), (txt_search, "search"), ("Уйти домой", "quit")]
        
    elif loc == "search":
        if not searched_entrance or BUGGY_MODE:
            gold += 30
            if not BUGGY_MODE:
                searched_entrance = True
            current_text = "Ты порылся в кустах и нашел 30 золотых монет! Неплохое начало."
        else:
            current_text = "Ты уже всё тут обыскал. Больше ничего нет, кроме паутины."
        current_image = None
        buttons = [("Назад", "entrance")]

    elif loc == "fork":
        current_text = "Ты на развилке. Слева темный туннель (слышны звуки), справа светлый проход."
        current_image = None
        buttons = [("Налево (темно)", "monster"), ("Направо (светло)", "merchant"), (txt_back, "entrance")]

    elif loc == "monster":
        if skeleton_defeated:
            current_text = "Ты снова в комнате скелета. Тут пусто, только кости хрустят под ногами."
            current_image = None
            buttons = [("Идти к дракону", "boss"), ("На развилку", "fork")]
        else:
            current_text = "На тебя выпрыгивает Скелет-Воин с ржавым мечом! Он выглядит злой."
            current_image = img_skeleton
            buttons = [(txt_attack, "fight"), ("Проскочить мимо", "dodge")]

    elif loc == "fight":
        hp -= 30
        current_text = "Ты вступил в бой! Скелет царапнул тебя (-30 HP)."
        if hp > 0:
            gold += 50
            skeleton_defeated = True
            current_text += " Ты победил и нашел сундук с 50 золотыми!"
            current_image = None
            buttons = [("Идти к дракону", "boss")]
        else:
            current_text = "Скелет оказался сильнее... Ты погиб."
            current_image = None
            buttons = [("Начать заново", "restart")]

    elif loc == "dodge":
        hp -= 10
        current_text = "Ты ловко уклонился, но он всё же задел тебя (-10 HP)."
        current_image = None
        buttons = [("Идти к дракону", "boss")]

    elif loc == "merchant":
        current_text = txt_merchant_intro
        current_image = img_merchant
        buttons = [("Купить Меч (40g)", "buy_sword"), ("Купить Зелье (20g)", "buy_potion"), ("Идти дальше", "boss")]

    elif loc == "buy_sword":
        if has_sword:
            current_text = "Торговец усмехается: 'Зачем тебе второй меч, дружище?'"
        elif gold >= 40:
            if not BUGGY_MODE:
                gold -= 40
            has_sword = True
            current_text = "Ты купил отличный меч! Теперь ты опасен."
        else:
            current_text = "Торговец качает головой: 'Не хватает золота, дружище'."
        buttons = [("Назад к торговцу", "merchant")]

    elif loc == "buy_potion":
        if gold >= 20:
            if not BUGGY_MODE:
                gold -= 20
            heal = 40
            if not BUGGY_MODE:
                hp = min(hp + heal, max_hp)
            else:
                hp += heal
            current_text = f"Ты выпил зелье. Твое здоровье: {hp}/{max_hp}."
        else:
            current_text = "У тебя нет 20 золотых."
        buttons = [("Назад к торговцу", "merchant")]

    elif loc == "boss":
        current_text = "Ты вошел в логово ДРАКОНА! Он охраняет свои сокровища."
        current_image = None
        if has_sword:
            buttons = [("Атаковать мечом!", "win"), ("Убежать", "run_boss")]
        else:
            buttons = [("Атаковать голыми руками", "die_boss"), ("Убежать", "run_boss")]

    elif loc == "win":
        global dragon_defeated
        dragon_defeated = True
        current_text = "Ты наносишь смертельный удар! Дракон повержен! ТЫ ПОБЕДИЛ!"
        current_image = None
        buttons = [("Начать заново", "restart")]

    elif loc == "die_boss":
        hp -= 80
        current_text = "Дракон обжигает тебя огнем! (-80 HP)"
        if BUGGY_MODE:
            if hp == 0:
                current_text += " Ты сгорел заживо."
                buttons = [("Начать заново", "restart")]
            else:
                current_text += " Ты чудом выжил и убежал."
                buttons = [("На развилку", "fork")]
        else:
            if hp <= 0:
                current_text += " Ты сгорел заживо."
                buttons = [("Начать заново", "restart")]
            else:
                current_text += " Ты чудом выжил и убежал."
                buttons = [("На развилку", "fork")]

    elif loc == "run_boss":
        hp -= 20
        current_text = "Ты убегаешь, но дракон бьет тебя хвостом (-20 HP)."
        if BUGGY_MODE:
            if hp == 0:
                current_text += " Ты не успел убежать..."
                buttons = [("Начать заново", "restart")]
            else:
                buttons = [("На развилку", "fork")]
        else:
            if hp <= 0:
                current_text += " Ты не успел убежать..."
                buttons = [("Начать заново", "restart")]
            else:
                buttons = [("На развилку", "fork")]

    elif loc == "restart":
        hp = 50 if BUGGY_MODE else 100
        gold = 0
        has_sword = False
        searched_entrance = False
        skeleton_defeated = False
        dragon_defeated = False
        set_location("entrance")
        return

    elif loc == "quit":
        pygame.quit()
        sys.exit()

# Главный цикл
running = True
set_location("entrance")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, (btn_text, btn_action) in enumerate(buttons):
                btn_width = (SCREEN_WIDTH - 60) // len(buttons) if buttons else 0
                btn_y = SCREEN_HEIGHT - 180 + 110
                btn_rect = pygame.Rect(20 + i * (btn_width + 10), btn_y, btn_width, 50)
                if btn_rect.collidepoint(event.pos):
                    
                    if BUGGY_MODE and btn_action == "entrance" and location == "fork":
                        continue 
                    
                    set_location(btn_action)

    update_ui()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()