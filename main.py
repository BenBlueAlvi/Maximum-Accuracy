import random

import pygame

clock = pygame.time.Clock()

pygame.mixer.pre_init(22050, -16, 3, 8)
pygame.mixer.init()



# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREY = (150,150,150)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)


done = False


pygame.init()
font = pygame.font.SysFont('Calibri', 15, True, False)
size = (700, 700)
gScreen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.display.set_caption("TBB: To Be Renamed")
sciencepic = pygame.image.load("Assets/science.png")
progresspic = pygame.image.load("Assets/progress.png")
failurepic = pygame.image.load("Assets/failure.png")
mathspic = pygame.image.load("Assets/maths.png")
engiespic = pygame.image.load("Assets/engies.png")
campainerspic = pygame.image.load("Assets/campainers.png")
moneypic = pygame.image.load("Assets/money.png")

def bubble_sort(items):
	""" Implementation of bubble sort """
	for i in range(len(items)):
		for j in range(len(items)-1-i):
			if items[j] > items[j+1]:
				items[j], items[j+1] = items[j+1], items[j] 
	return items
	
def hitDetect(p1, p2, p3, p4):
	if p2[0] > p3[0] and p1[0] < p4[0] and p2[1] > p3[1] and p1[1] < p4[1]:
		return True
		
class Result(object):
	def __init__(self, desc, id, mon, prog, fail, sci, eng, mat, cam, pop):
		self.desc = desc
		self.id = id
		self.money = mon
		self.progress = prog
		self.failChance = fail
		self.scientists = sci
		self.engineers = eng
		self.maths = mat
		self.campaigners = cam
		self.people = pop
	
	def decide(self, player):
		if id == "":
			player.progress += self.progress
			player.failChance += self.failChance
			player.scientists += self.scientists
			player.engineers += self.engineers
			player.maths += self.maths
			player.campaigners += self.campaigners
		if "addprog" in id:
			player.progress += self.progress
		if "addmoney" in id:
			player.money += self.money
		if "multmoney" in id:
			player.money *= self.money
		if "addfail" in id:
			player.failChance += self.failChance
		if "multfail" in id:
			player.failChance *= self.failChance
		if "addsci" in id:
			player.scientists += self.scientists
		if "addeng" in id:
			player.engineers += self.engineers
		if "addmat" in id:
			player.maths += self.maths
		if "addcam" in id:
			player.campaigners += self.campaigners
		if "addpop" in id:
			for i in range(self.pop):
				rand = random.randint(1, 4)
				if rand == 1:
					player.scientists += 1
				if rand == 2:
					player.engineers += 1
				if rand == 3:
					player.maths += 1
				if rand == 4:
					player.campaigners += 1

class Prompt(object):
	def __init__(self, name, prompt, results, cooldown):
		self.name = name
		self.prompt = prompt
		self.results = results
		self.cooldown = cooldown
		self.daysSince = 0
	def result(self, response):
		#varbile changing here:
		if response == "yes":
			pass

coffee = Prompt("", "Can we install a coffee machine in the rocket?", [Result("Sure, Why not?", ["addmoney", "addfail", "addeng", "addprog"], -1, 2, 4, 0, 1, 0, 0, 0)], 1)			
coffeee = Prompt("", "Can we install a coffeee machine in the rocket?", [Result("NO?", ["addmoney", "addfail", "addeng", "addprog"], -1, 2, 4, 0, 1, 0, 0, 0)], 1)			

class Player(object):
	def __init__(self, mon, prog, fail, sci, eng, mat, cam):
		self.money = mon
		self.progress = prog
		self.failChance = fail
		self.fails = 0
		self.scientists = sci
		self.engineers = eng
		self.maths = mat
		self.campaigners = cam
		
		
player = Player(100, 0, 100, 1, 2, 1, 1)

class button(object):
	def __init__(self, image, hoverimg):
		self.image = image
		self.hoverimg = hoverimg
	def buildNew(self):
		newButton = button(pygame.image.load(self.image), pygame.image.load(self.hoverimg))
		return newButton
responseButton = button("Assets/button.png", "Assets/button_hover.png").buildNew()
		

possiblequestions = [coffee, coffeee]	
questions = [coffee, coffeee]
newday = True	
mouse_down = False

while not done:

	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			done = True 
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_down = True
				
		elif event.type == pygame.MOUSEBUTTONUP:
			mouse_down = False
	mouse_pos = pygame.mouse.get_pos()
	
	if newday:
		#new 
		newday = False
		theQuestion = possiblequestions[random.randint(0, len(questions) - 1)]
		
		
	y = 0
	for i in theQuestion.results:
		
	
		if hitDetect(mouse_pos, mouse_pos, [50, 450 + y * 50], [650, 525 + y * 50]):
			if mouse_down:
				newday = True
				mouse_down = False
				possiblequestions.remove(theQuestion)
				
				for q in questions:
					q.daysSince +=1
					if q.daysSince >= q.cooldown:
						possiblequestions.append(q)
	
		y += 1
	
	
	
	gScreen.fill(WHITE)
	gScreen.blit(font.render(theQuestion.prompt, True, BLACK), [200, 100])
	
	y = 0
	for i in theQuestion.results:
		
		gScreen.blit(responseButton.image, [50, 450 + y * 50])
		
		gScreen.blit(font.render(i.desc,True,BLACK), [60, 455 + y * 50])
		
		y+= 1
	
	
	gScreen.blit(font.render(str(player.money),True,BLACK), [155 - 38, 60])
	pygame.draw.rect(gScreen, YELLOW, [155 - 38, 60, 50, (player.money * -1) / 20])
	gScreen.blit(moneypic, [155 - 38, 10])
	
	pygame.draw.rect(gScreen, GREEN, [233 - 38, 60, 50, (player.progress * -1) / 2])
	gScreen.blit(progresspic, [233 - 38, 10])
	
	pygame.draw.rect(gScreen, RED, [311 - 38, 60, 50, (player.failChance * -1) / 2])
	gScreen.blit(failurepic, [311 - 38, 10])
	
	pygame.draw.rect(gScreen, BLUE, [388 - 38, 60, 50, (player.scientists * -1)])
	gScreen.blit(sciencepic, [388 - 38, 10])
	
	pygame.draw.rect(gScreen, GREY, [466 -38, 60, 50, (player.engineers * -1)])
	gScreen.blit(engiespic, [466 -38, 10])
	
	pygame.draw.rect(gScreen, PURPLE, [544 - 38, 60, 50, (player.maths * -1)])
	gScreen.blit(mathspic, [544 - 38, 10])
	
	pygame.draw.rect(gScreen, WHITE, [622 - 38, 60, 50, (player.campaigners * -1)])
	gScreen.blit(campainerspic, [622 - 38, 10])
	
	
	
	gScreen.blit(font.render(str(player.progress),True,BLACK), [233 - 38, 60])
	gScreen.blit(font.render(str(player.failChance),True,BLACK), [311 - 38, 60])
	gScreen.blit(font.render(str(player.scientists),True,BLACK), [388 - 38, 60])
	gScreen.blit(font.render(str(player.engineers),True,BLACK), [466 -38, 60])
	gScreen.blit(font.render(str(player.maths),True,BLACK), [544 - 38, 60])
	gScreen.blit(font.render(str(player.campaigners),True,BLACK), [622 - 38, 60])
	
	pygame.display.update()
	clock.tick(60)



	
	