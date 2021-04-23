import pygame, sys, random, math

pygame.init()
pygame.font.init()
inGameFont = pygame.font.SysFont('arial', 30, bold=True)
finalScreenFont = pygame.font.SysFont('arial', 100, bold=True)
clock = pygame.time.Clock()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('AIM practice')


class Target():
	def __init__(self, x, y, radius, color, velocity, shrink):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.velocity = velocity
		self.shrink = shrink

	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

	def update(self, screen):
		self.radius -= self.shrink
		self.x += self.velocity['x']
		self.y += self.velocity['y']

		if self.x - self.radius <= 0 or self.x  + self.radius >= SCREEN_WIDTH:
			self.velocity['x'] *= -1

		if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
			self.velocity['y'] *= -1

		self.draw(screen)


def generate_new_target():
	radius = 50
	x = random.randint(radius, SCREEN_WIDTH - radius)
	y = random.randint(radius, SCREEN_HEIGHT - radius)
	velx = random.choice([-3, -2, -1, 1, 2, 3])
	vely = random.choice([-3, -2, -1, 1, 2, 3])
	velocity = {'x': velx, 'y':vely}
	shrink = random.random()/1.3
	color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))

	dots.append(Target(x, y, radius, color, velocity, shrink))

def check_collision(target, click_x, click_y):
	global score
	distance = math.sqrt((target.x - click_x)**2 + (target.y - click_y)**2)
	if distance <= target.radius:
		dots.pop(dots.index(target))
		generate_new_target()
		score += 1


#Variables
game_state = True
dots = []
score = 0
nn = 2
for i in range(nn):
	generate_new_target()

while True:
	screen.fill((25, 25, 25))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			x = pygame.mouse.get_pos()[0]
			y = pygame.mouse.get_pos()[1]

			for dot in dots:
				check_collision(dot, x, y)

		if event.type == pygame.KEYDOWN and not game_state:
			score = 0
			game_state = True
			for i in range(nn):
				generate_new_target()

	if game_state:
		score_font = inGameFont.render(f'score: {score}', False, (255, 255, 255))
		screen.blit(score_font, (10 , 10))
		for dot in dots:
			dot.update(screen)

			if dot.radius <= 5:
				dots.pop(dots.index(dot))

		if len(dots) == 0:
			game_state = False
	else:
		final_screen_score_font = finalScreenFont.render(f'score: {score}', False, (255, 255, 255))
		screen.blit(final_screen_score_font, (100, 250))

	pygame.display.update()
	clock.tick(60)