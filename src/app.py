from random import *
import pygame
import psycopg2 as p
con = p.connect("dbname='python_game_data' user='postgres' host='192.168.99.100' password='postgres'")
cur = con.cursor()
cur.execute("select * from game_text")
rows=cur.fetchall()

cur.execute("select score from scores ORDER BY score DESC")
score=cur.fetchall()

#Game part
pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("First Game in Python")

#load imgs
walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]
bg = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')
sananes_L = pygame.image.load('images/sananes_L.png')
sananes_R = pygame.image.load('images/sananes_R.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('sounds/bullet.wav')
hitSound = pygame.mixer.Sound('sounds/hit.wav')
screamSound = pygame.mixer.Sound('sounds/scream.wav')
deathSound = pygame.mixer.Sound('sounds/goblin_death_2.wav')
winSound = pygame.mixer.Sound('sounds/win.wav')
looseSound = pygame.mixer.Sound("sounds/loose_zelda.wav")

music = pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

class player(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 5
		self.isJump = False
		self.jumpCount = 10
		self.left = True
		self.right = False
		self.walkCount = 0
		self.standing = True
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		self.lives = 5
		self.score = 0

	def draw(self, win):
		if self.walkCount + 1 >= 27:
			self.walkCount = 0

		if not(self.standing):
			if self.left:
				win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
			elif self.right:
				win.blit(walkRight[self.walkCount//3], (self.x,self.y))
				self.walkCount += 1
		else:
			if self.right:
				win.blit(walkRight[0], (self.x,self.y))
			else:
				win.blit(walkLeft[0], (self.x,self.y))
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		#pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
	def hit(self):
		self.isJump = False
		self.jumpCount = 10
		self.x = 60
		self.y = 410
		self.walkCount = 0
		self.lives -= 1
		self.score -= 5
		if self.lives <= 0:
			font1 = pygame.font.SysFont('comicsans', 28, True)
			text = font1.render(rows[1][2], 1, (255,0,0))
			win.blit(text, (250 - (text.get_width()/2), 200))
			pygame.display.update()
			pygame.mixer.music.stop()
			pygame.mixer.music.set_volume(0.8)
			looseSound.play()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						i = 301
						cur.execute("INSERT INTO scores (score) VALUES (%s);", (self.score, ))
						con.commit()
						pygame.quit()


		font1 = pygame.font.SysFont('comicsans', 100)
		text = font.render('-5', 1, (255,0,0))
		win.blit(text, (250 - (text.get_width()/2), 200))
		pygame.display.update()
		i = 0
		while i < 200:
			pygame.time.delay(10)
			i += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					i = 301
					pygame.quit()

class projectile(object):
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y - 12
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * facing

	def draw(self, win):
		if self.facing == -1:
			win.blit(sananes_L, (self.x, self.y))
		else:
			win.blit(sananes_R, (self.x, self.y))

	

class enemy(object):
	walkRight = [pygame.image.load('images/R1E.png'), pygame.image.load('images/R2E.png'), pygame.image.load('images/R3E.png'), pygame.image.load('images/R4E.png'), pygame.image.load('images/R5E.png'), pygame.image.load('images/R6E.png'), pygame.image.load('images/R7E.png'), pygame.image.load('images/R8E.png'), pygame.image.load('images/R9E.png'), pygame.image.load('images/R10E.png'), pygame.image.load('images/R11E.png')]
	walkLeft = [pygame.image.load('images/L1E.png'), pygame.image.load('images/L2E.png'), pygame.image.load('images/L3E.png'), pygame.image.load('images/L4E.png'), pygame.image.load('images/L5E.png'), pygame.image.load('images/L6E.png'), pygame.image.load('images/L7E.png'), pygame.image.load('images/L8E.png'), pygame.image.load('images/L9E.png'), pygame.image.load('images/L10E.png'), pygame.image.load('images/L11E.png')]

	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.path = [50, self.end]
		self.walkCount = 0
		self.vel = 3
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)
		self.health = 10
		self.visible = True

	def draw(self, win):
		self.move()
		if self.visible:
			if self.walkCount + 1 >= 33:
				self.walkCount = 0

			if self.vel > 0:
				win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			else:
				win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			

			pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
			pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
			self.hitbox = (self.x + 17, self.y + 2, 31, 57)
			#pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

	def move(self):
		if self.vel > 0:
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
				self.walkCount = 0
		else:
			if self.x - self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
				self.walkCount = 0

	def hit(self):
		if self.health > 1:
			self.health -= 1
		else:
			self.visible = False
		#print('hit')

def redrawGameWindow():
	global walkCount
	win.blit(bg, (0,0))

	textB = fontB.render(rows[0][2], 1, (0,0,128))
	textC = font.render('Lives ' + str(man.lives), 1, (200,0,0))

	if man.score > score[0][0]:
		text = font.render('Score: ' + str(man.score), 1, (255, 128, 0))
		textD = font.render('Record: ' + str(man.score), 1, (255, 128, 0))
	else:
		text = font.render('Score: ' + str(man.score), 1, (0, 0, 0))
		textD = font.render('Record: ' + str(score[0][0]), 1, (255, 128, 0))


	win.blit(text, (360, 10))
	win.blit(textB, (10, 50))
	win.blit(textC, (10, 10))
	win.blit(textD, (360, 32))

	man.draw(win)
	goblin.draw(win)
	for bullet in bullets:
		bullet.draw(win)
	pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
fontB = pygame.font.SysFont('comicsans', 18, False, True)
man = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
wait_for_enemy = False

while run:
	clock.tick(27)

	#win condition
	if man.score >= 2000:
		font1 = pygame.font.SysFont('comicsans', 23, True)
		text = font1.render(rows[2][2], 1, (0, 128, 0))
		win.blit(text, (250 - (text.get_width()/2), 230))
		pygame.display.update()
		pygame.mixer.music.stop()
		pygame.mixer.music.set_volume(0.8)
		winSound.play()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					cur.execute("INSERT INTO scores (score) VALUES (%s);", (man.score, ))
					con.commit()
					pygame.quit()
					break


	if goblin.visible == True:
		if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
			if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
				screamSound.play()
				man.hit()
				#man.isJump = False
				#man.jumpCount = 10
				man.score -= 5
	elif wait_for_enemy == 0:
		pygame.mixer.stop()
		deathSound.play()
		wait_for_enemy = 50
		#del goblin
		#goblin = enemy(randint(90,400), 410, 64, 64, 450)

	if shootLoop > 0:
		shootLoop += 1
	if shootLoop > 3:
		shootLoop = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	for bullet in bullets:
		if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
			if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
				hitSound.play()
				goblin.hit()
				man.score += 1
				bullets.pop(bullets.index(bullet))

		if bullet.x < 500 and bullet.x > 0:
			bullet.x += bullet.vel
		else:
			bullets.pop(bullets.index(bullet))	
	
	keys = pygame.key.get_pressed()

	if keys[pygame.K_SPACE] and shootLoop == 0 and goblin.visible == True:
		bulletSound.play()
		if man.left:
			facing = -1
		else:
			facing = 1
		if len(bullets) < 5:
			bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6, (0,0,0), facing))

		shootLoop = 1

	if keys[pygame.K_LEFT] and man.x > man.vel:
		man.x -= man.vel
		man.left = True
		man.right = False
		man.standing = False
	elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
		man.x += man.vel
		man.right = True
		man.left = False
		man.standing = False
	else:
		man.standing = True
		man.walkCount = 0
	if not(man.isJump):
		if keys[pygame.K_UP]:
			man.isJump = True
			man.right = False
			man.left = False
			man.walkCount = 0
	else:
		if man.jumpCount >= - 10:
			neg = 1
			if man.jumpCount < 0:
				neg = -1
			man.y -= (man.jumpCount ** 2) * 0.5 * neg
			man.jumpCount -= 1
		else:
			man.isJump = False
			man.jumpCount = 10

	if wait_for_enemy > 0:
		wait_for_enemy -= 1
		if wait_for_enemy == 0:
			del goblin
			goblin = enemy(randint(90,400), 410, 64, 64, 450)
	redrawGameWindow()

pygame.quit()
