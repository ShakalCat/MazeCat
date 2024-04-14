from pygame import *
from random import randint

#класс GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self, p_image, x, y, p_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(p_image),(size_x, size_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#картинки
img_background = 'polana.png'
img_hero = 'kotenochek.png'
img_bullet = 'lapa5.png'

#окно
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер онлайн за 50к долларов')
background = transform.scale(image.load('fonlapka.png'), (win_width, win_height))

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

#Текст/шрифт с подсчётом пропущенных врагов и попеждённых врагов
font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 36)
#класс наследник Player для  класса GameSprite
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

#класс наследник Enemy для  класса GameSprite
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдёт до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1 

#класс Bullet
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

#переменная которая останавливает игру
finish = False
lost = 0
score = 0

#создаём спрайт
ship = Player(img_hero, 5, win_height - 100, 50, 80, 50)
bullets = sprite.Group()
#Группа monsters
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('nitki.png', randint(80, win_width - 80), -40, randint(1,5), 80, 50)
    monsters.add(monster)

#текст выйгрыша и пройгрыша
text_win = font1.render('УРААААА ВЫЙГРЫШ!!!!!', True, (78,173,0))
text_lose = font2.render('ехххх пройгрыш(((((', True, (117,0,0))

#оновной цикл игры
game = True #флаг сбрасывается на кнопку
while game:
#событие нажатия кнопки Закрыть
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire() 

    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
        text_schot = font2.render('Счет:'+str(score), 1, (255,255,255))
        window.blit(text_schot, (10, 50))
        text_miss = font2.render('Пропущено:' +str(lost), 1, (255,255,255))
        window.blit(text_miss, (10, 100))

        #проиводим движения спрайтов
        ship.update()
        #Обновляем monsters
        monsters.update()
        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, False)# пули и враги
        for c in collides:
            score += 1
            monster = Enemy('nitki.png', randint(80, win_width - 80), -40, randint(1,5), 80, 50)
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= 10:
            finish = True
            window.blit(text_lose, (200,200))
        if score >= 50:
            finish = True
            window.blit(text_win, (200,200))
        display.update()
    else:
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    finish = False
                    score = 0
                    lost = 0
                    for n in monsters:
                        n.kill()
                    for m in bullets:
                        m.kill()
                    for i in range(6):
                        monster = Enemy('nitki.png', randint(80, win_width - 80), -40, randint(1,5), 80, 50)
                        monsters.add(monster)

    time.delay(50)#цикл срабатывает каждые 0.05 секунд



#окно выйгрыша и пройгрыша
#window_win = display.set_mode((win_width, win_height))
#window_lose = display.set_mode((win_width, win_height))

#появление окон выйгрыша и пройгрыша
    #if text_miss == 3:
     #   window_lose.open()

#keys = key.get_pressed() 
#!class Player(GameSprite):
#!        def update(self):
#?if keys[K_SPACE] and self.rect.x > 5:
#?         self.rect.x -= self.speed
#/////bro cool
