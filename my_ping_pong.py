from pygame import *

# Инициализация
init()
font.init()

# Параметры окна
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Пинг-Понг")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифты
font1 = font.SysFont('Arial', 36)

# Класс спрайта
class GameSprite(sprite.Sprite):
    def __init__(self, source, x, y, width, height, speed, use_image=False):
        super().__init__()
        if use_image:
            self.image = transform.scale(image.load(source), (width, height))
        else:
            self.image = Surface((width, height))
            self.image.fill(source)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока
class Player(GameSprite):
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed

# Игроки и мяч
player1 = Player(WHITE, 30, 200, 20, 100, 7)
player2 = Player(WHITE, 650, 200, 20, 100, 7)
ball = GameSprite("ball.png", 330, 230, 20, 20, 5, use_image=True)


# Направление мяча
ball_speed_x = 4
ball_speed_y = 4

# Очки
score1 = 0
score2 = 0

# Игровой цикл
clock = time.Clock()
game = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill((135, 206, 235))  # Голубой цвет


    # Обновление игроков
    player1.update_left()
    player2.update_right()
    player1.reset()
    player2.reset()

    # Движение мяча
    ball.rect.x += ball_speed_x
    ball.rect.y += ball_speed_y

    # Отскок от верх/низ
    if ball.rect.top <= 0 or ball.rect.bottom >= win_height:
        ball_speed_y *= -1

    # Отскок от ракеток
    if sprite.collide_rect(ball, player1) or sprite.collide_rect(ball, player2):
        ball_speed_x *= -1

    # Го́л
    if ball.rect.left <= 0:
        score2 += 1
        ball.rect.x, ball.rect.y = 330, 230
        ball_speed_x *= -1
    if ball.rect.right >= win_width:
        score1 += 1
        ball.rect.x, ball.rect.y = 330, 230
        ball_speed_x *= -1

    # Отрисовка мяча и счета
    ball.reset()
    text1 = font1.render("Player 1: " + str(score1), True, WHITE)
    text2 = font1.render("Player 2: " + str(score2), True, WHITE)
    window.blit(text1, (50, 20))
    window.blit(text2, (500, 20))

    display.update()
    clock.tick(60)
