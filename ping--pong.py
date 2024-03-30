from pygame import *

init()

win_width = 700
win_height = 500
FPS = 60
clock = time.Clock()
exit = False

bg = image.load("background.png")
bg = transform.scale(bg, (win_width, win_height))

window = display.set_mode((win_width, win_height))

display.set_caption("Ping_pong")


class GameSpite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSpite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__(player_image, player_x, player_y, width, height)
        self.speed = player_speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


class Ball(GameSpite):
    def __init__(self, player_image, player_x, player_y, width, height, speed_x, speed_y):
        super().__init__(player_image, player_x, player_y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


player_l = Player('player_l.png', 0, 100, 80, 80, 10)
player_r = Player('player_r.png', win_width - 80, 100, 80, 80, 10)
ball = Ball("bullet.png", 100, 100, 50, 50, 5, 5)

finish = False
pause = True

font = font.Font(None, 35)
lose = 1

def ball_collide():
    if sprite.collide_rect(player_l, ball):
        ball.speed_x *= -1
        ball.speed_y += (ball.rect.centery - player_l.rect.centery) / 12
    if sprite.collide_rect(player_r, ball):
        ball.speed_x *= -1
        ball.speed_y += (ball.rect.centery - player_r.rect.centery) / 12
    if ball.rect.y > win_height - 50 or ball.rect.y < 0:
        ball.speed_y *= -1

while exit != True:
    for e in event.get():
        if e.type == QUIT:
            exit = True
    keys = key.get_pressed()
    window.blit(bg, (0, 0))
    if finish != True:
        if pause == False:
            ball_collide()
            if ball.rect.x < -50:
                lose = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
                finish = True
            if ball.rect.x > win_width:
                lose = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))
                finish = True
            ball.update()
            player_l.update_l()
            player_r.update_r()
        else:
            window.blit(font.render('Press SPACE to start.', True, (255, 255, 255)), (250, 250))
            if keys[K_SPACE]:
                pause = False
    else:
        window.blit(lose, (250, 250))
        if keys[K_r]:
            ball.rect.x = 250
            ball.rect.y = 100
            ball.speed_x = 3
            ball.speed_y = 3
            finish = False
            pause = True
    player_r.reset()
    player_l.reset()
    ball.reset()
    display.update()
    clock.tick(FPS)