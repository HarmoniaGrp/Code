from random import randint
from pygame import *

 
 
 
#background music
mixer.init()
mixer.music.load('fire.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
 
#we need the following images:
img_back = "galaxy.jpg" #game background
img_hero = "rocket.png" #hero
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_asteroid = "asteroid.png"


font.init()
font1 = font.Font('Arial', 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font('Arial', 36)
 
#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Call for the class (Sprite) constructor:
       super().__init__()
 
 
       #every sprite must store the image property
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
 
       #every sprite must have the rect property – the rectangle it is fitted in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #method drawing the character on the window
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
 
#main player class
class Player(GameSprite):
   #method to control the sprite with arrow keys
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #method to "shoot" (use the player position to create a bullet there)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
 
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()    
 
 
 
goal = 10
score = 0
lost = 0
max_lost = 3
num_fire = 0
global number
 
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1
 
class asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1
 
 
 
 
font.init()
style = font.Font('Arial', 36)
 
text_lose = style.render("Missed: " + str(lost), 1, (255, 255, 255))
 
 
 
 
#create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
 
#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
 
asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
   asteroids.add(asteroid)
 
 
bullets = sprite.Group()
 

 
#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#Main game loop:
run = True #the flag is reset by the window close button
while run:
    #"Close" button press event
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:

                    fire_sound.play()
                    ship.fire()
        
    
    
    if not finish:
        #update the background
        window.blit(background,(0,0))

        text = font2.render('Score:', str(score), 1, (255, 255, 255))
        window.blit(text, (10, 10))

        text_lose = font2.render("Missed:", str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
    
    
        #launch sprite movements
        ship.update()
    
        bullets.update()
        bullets.draw(window)
    
        #update them in a new location in each loop iteration
        ship.reset()
        monsters.update()
        monsters.draw(window)
    
        asteroids.update()
        asteroids.draw(window)
    
        display.update()
    if lost == lost + 3:
        finish = True
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
            #this loop will repeat as many times as the number of monsters hit
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
        finish = True
        window.blit(lose, (200, 200))
    if score >= goal:
        True
        window.blit(win, (200, 200))
    
    #the loop is executed each 0.05 sec
    time.delay(50)