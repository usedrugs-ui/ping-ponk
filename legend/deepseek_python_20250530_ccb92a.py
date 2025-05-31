# Импорт необходимых модулей из pygame
from pygame import *
from pygame.locals import *
import random  # Для случайного выбора направления мяча

# Функция отображения экрана с инструкциями
def show_instructions():
    window.fill((230,255,255))
    # Создание текстовых поверхностей
    title = title_font.render("PONG GAME", True, (0,0,0))
    instr1 = text_font.render("Управление:", True, (0,0,0))
    instr2 = text_font.render("Левая ракетка: W / S", True, (0,0,0))
    instr3 = text_font.render("Правая ракетка: UP / DOWN", True, (0,0,0))
    instr4 = text_font.render("Нажмите ПРОБЕЛ чтобы начать", True, (0,0,0))
    instr5 = text_font.render("P - пауза, R - рестарт", True, (0,0,0))
    # Отображение текста на экране с центрированием
    window.blit(title, (win_width//2 - title.get_width()//2,50))
    window.blit(instr1, (win_width//2 - instr1.get_width()//2,150))
    window.blit(instr2, (win_width//2 - instr2.get_width()//2,200))
    window.blit(instr3, (win_width//2 - instr3.get_width()//2,250))
    window.blit(instr4, (win_width//2 - instr4.get_width()//2,300))
    window.blit(instr5, (win_width//2 - instr5.get_width()//2,350))

# Функция сброса мяча в центр
def reset_ball():
    ball.rect.x = win_width // 2 - ball.rect.width // 2  # Центр по X
    ball.rect.y = win_height // 2 - ball.rect.height // 2  # Центр по Y
    global speed_x, speed_y
    speed_x = 3 * random.choice([1, -1])  # Случайное направление по X
    speed_y = 3 * random.choice([1, -1])  # Случайное направление по Y

# Функция полного сброса игры
def reset_game():
    global score1, score2, finish
    score1 = 0  # Обнуление счета 1 игрока
    score2 = 0  # Обнуление счета 2 игрока
    finish = False  # Сброс флага завершения игры
    # Центрирование ракеток
    racket1.rect.y = win_height // 2 - racket1.rect.height // 2
    racket2.rect.y = win_height // 2 - racket2.rect.height // 2
    reset_ball()  # Сброс мяча

# Функция отображения экрана паузы
def draw_pause_screen():
    # Создание полупрозрачной поверхности
    pause_surface = Surface((win_width, win_height), SRCALPHA)
    pause_surface.fill((0, 0, 0, 128))  # Чёрный с прозрачностью
    window.blit(pause_surface, (0, 0))  # Наложение поверхности
    # Текст паузы
    pause_text = title_font.render("ПАУЗА", True, (255, 255, 255))
    continue_text = text_font.render("Нажмите P для продолжения", True, (255, 255, 255))
    # Отображение текста
    window.blit(pause_text, (win_width//2 - pause_text.get_width()//2, win_height//2 - 50))
    window.blit(continue_text, (win_width//2 - continue_text.get_width()//2, win_height//2 + 50))

# Базовый класс игровых спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
       super().__init__()  # Инициализация родительского класса
       self.image = transform.scale(image.load(player_image), (wight, height))  # Загрузка и масштабирование изображения
       self.speed = player_speed  # Скорость объекта
       self.rect = self.image.get_rect()  # Получение прямоугольника для коллизий
       self.rect.x = player_x  # Начальная позиция X
       self.rect.y = player_y  # Начальная позиция Y

    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))  # Отрисовка спрайта

# Класс игрока (ракетки)
class Player(GameSprite):
    def update_r(self):  # Управление правой ракеткой
        keys = key.get_pressed()  # Получение состояния клавиш
        if keys[K_UP] and self.rect.y > 5:  # Движение вверх
            self.rect.y -= self.speed 
        if keys[K_DOWN] and self.rect.y < win_height - 80:  # Движение вниз
            self.rect.y += self.speed
    def update_l(self):  # Управление левой ракеткой
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:  # Движение вверх
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:  # Движение вниз
            self.rect.y += self.speed

# Инициализация pygame
init()

# Настройки игры
background = image.load('back.png')
background = transform.scale(background, (700,500))
win_width = 600  # Ширина окна
win_height = 500  # Высота окна
score1 = 0  # Счёт первого игрока
score2 = 0  # Счёт второго игрока
window = display.set_mode((win_width, win_height))  # Создание окна
display.set_caption("Pong Game")  # Заголовок окна
window.blit(background, (0, 0))

# Шрифты
title_font = font.Font(None, 70)  # Шрифт для заголовка
text_font = font.Font(None, 36)   # Шрифт для обычного текста

# Флаги состояния игры
show_instructions_screen = True  # Показывать инструкции
game = True  # Главный игровой цикл
finish = False  # Игра завершена
paused = False  # Игра на паузе
clock = time.Clock()  # Для контроля FPS
FPS = 60  # Кадров в секунду

# Создание объектов
racket1 = Player('platform.png', 30, 200, 4, 70, 70)  # Левая ракетка
racket2 = Player('platform1.png', 520, 200, 4, 80, 80)  # Правая ракетка
ball = GameSprite('ball.png', 200, 200, 4, 50, 50)  # Мяч

score_font = font.Font(None, 35)  # Шрифт для счёта

# Начальная скорость мяча
speed_x = 3
speed_y = 3

# Главный игровой цикл
while game:
    # Обработка событий
    for e in event.get():
        if e.type == QUIT:  # Закрытие окна
            game = False
        if e.type == KEYDOWN:  # Нажатие клавиши
            if show_instructions_screen and e.key == K_SPACE:  # Старт игры
                show_instructions_screen = False
                reset_ball()
            elif e.key == K_p:  # Пауза
                paused = not paused
            elif e.key == K_r:  # Рестарт
                reset_game()
            elif e.key == K_ESCAPE:  # Выход в меню
                show_instructions_screen = True
                paused = False
    
    # Логика отображения
    if show_instructions_screen:
        show_instructions()  # Показ инструкций
    else:
        if not finish and not paused:  # Основной игровой процесс
            window.blit(background, (0, 0))
            
            # Рисование центральной линии
            for i in range(0, win_height, 30):
                draw.line(window, (150, 150, 150), (win_width//2, i), (win_width//2, i+15), 3)
            
            # Обновление позиций
            racket1.update_l()  # Левая ракетка
            racket2.update_r()  # Правая ракетка
            ball.rect.x += speed_x  # Движение мяча по X
            ball.rect.y += speed_y  # Движение мяча по Y

            # Обработка столкновений с ракетками
            if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
                speed_x *= -1.1  # Изменение направления и увеличение скорости
                speed_y *= 1.1
                # Расчет угла отскока
                if sprite.collide_rect(racket1, ball):
                    relative_intersect = (racket1.rect.centery - ball.rect.centery) / (racket1.rect.height/2)
                else:
                    relative_intersect = (racket2.rect.centery - ball.rect.centery) / (racket2.rect.height/2)
                speed_y = -relative_intersect * 5  # Новый угол
            
            # Отскок от верхней и нижней границы
            if ball.rect.y > win_height-50 or ball.rect.y < 0:
                speed_y *= -1

            # Гол за правую ракетку
            if ball.rect.x < 0:
                score2 += 1
                reset_ball()

            # Гол за левую ракетку
            if ball.rect.x > win_width:
                score1 += 1
                reset_ball()

            # Отрисовка объектов
            racket1.reset()
            racket2.reset()
            ball.reset()

            # Отображение счёта
            score_text = score_font.render(f'{score1}:{score2}', True, (0, 0, 0))
            text_width = score_text.get_width()
            window.blit(score_text, (win_width//2 - text_width//2, 10))

            # Проверка на победу
            if score1 >= 5 or score2 >= 5:
                finish = True
                win_text = score_font.render(f'PLAYER {1 if score1 >= 5 else 2} WINS!', True, (0, 0, 0))
                restart_text = text_font.render("Нажмите R для рестарта", True, (0, 0, 0))
                window.blit(win_text, (win_width//2 - win_text.get_width()//2, win_height//2 - 50))
                window.blit(restart_text, (win_width//2 - restart_text.get_width()//2, win_height//2 + 50))
        
        elif paused:  # Если игра на паузе
            # Отрисовка объектов
            racket1.reset()
            racket2.reset()
            ball.reset()
            draw_pause_screen()  # Отрисовка экрана паузы
    
    display.update()  # Обновление экрана
    clock.tick(FPS)  # Поддержание FPS

quit()  # Выход из pygame
