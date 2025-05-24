from pygame import *

def show_instructions():
    window.fill(background)
    title = title_font.render("PONG GAME", True, (0,0,0))
    instr1 = text_font.render("Управление:", True, (0,0,0))
    instr2 = text_font.render("Левая ракетка: W / S", True, (0,0,0))
    instr3 = text_font.render("Правая ракетка: UP / DOWN", True, (0,0,0))
    instr4 = text_font.render("Нажмите ПРОБЕЛ чтобы начать", True, (0,0,0))
    window.blit(title, (win_width//2 - title.get_width()//2,50))
    window.blit(instr1, (win_width//2 - instr1.get_width()//2,150))
    window.blit(instr2, (win_width//2 - instr2.get_width()//2,200))
    window.blit(instr3, (win_width//2 - instr3.get_width()//2,250))
    window.blit(instr4, (win_width//2 - instr4.get_width()//2,300))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (wight, height)) 
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


background = (200, 255, 255)
win_width = 600
win_height = 500
score1 = 0
score2 = 0
window = display.set_mode((win_width, win_height))
window.fill(background)

show_instructions_screen = True
game = True
finish = False
clock = time.Clock()
FPS = 60

racket1 = Player('platform.png', 30, 200, 4, 50, 200)
racket2 = Player('platform1.png', 520, 200, 4, 50, 200)
ball = GameSprite('ball.png', 200, 200, 4, 50, 50)


font.init()
font = font.Font(None, 35)


speed_x = 3
speed_y = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if show_instructions_screen:
            if e.type == KEYDOWN and e.key == K_SPACE:
                show_instructions_screen = False
            if show_instructions_screen:
                show_instructions()
            else:
                if not finish:
                    window.fill(background)
                    racket1.update_l()
                    racket2.update_r()
                    ball.rect.x += speed_x
                    ball.rect.y += speed_y

                    if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
                    speed_x *= -1
                    speed_y *= 1
                
                    if ball.rect.y > win_height-50 or ball.rect.y < 0:
                    speed_y *= -1

                    if ball.rect.x < 0:
                    score2 += 1
                    ball.rect.x = 200
                    ball.rect.y = 200
                    speed_x = 3

                    if ball.rect.x > win_width:
                    score1 += 1
                    ball.rect.x = 200
                    ball.rect.y = 200
                    speed_x = -3

                    racket1.reset()
                    racket2.reset()
                    ball.reset()

                    score_text = font.render(f'{score1}:{score2}', True, (0, 0, 0))
                    text_width = score_text.get_width()
                    window.blit(score_text,(win_width//2 - text_width//2, 10))

                    if score1 >=5 or score2 >= 5:
                        finish = True
                        win_text = font.render(f'PLAYER{1 if score1 >= 5 else 2}WINS', True, (0, 0, 0))
                        windows.blit(win_text,(200,200))

                display.update()
                clock.tick(FPS)
