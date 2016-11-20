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



pygame.init()
font = pygame.font.SysFont('Calibri', 15, True, False)
size = (700, 700)
gScreen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.display.set_caption("TBB: To Be Renamed")


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
	#doings is list of operations, operations is a tuple of the operation and the number
	def __init__(self, desc, result, doings):
		self.desc = desc
		self.result = result
		self.doings = doings
	
	def decide(self, player):
		for i in range(len(self.doings)):
			o, n = self.doings[i][0], self.doings[i][1]
			
			if o == "addprog":
				player.progress += n
			if o == "addmoney":
				player.money += n
			if o == "multmoney":
				player.money *= n
			if o == "addfail":
				player.failChance += n
			if o == "multfail":
				player.failChance *= n
			if o == "addsci":
				player.scientists += n
			if o == "addeng":
				player.engineers += n
			if o == "addmat":
				player.maths += n
			if o == "addcam":
				player.campaigners += n
			if o == "addpop":
				for i in range(n):
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

coffee = Prompt("", "Can we install a coffee machine in the rocket?", [Result("Sure, Why not?", "You install a coffee machine.", [["addmoney", -1], ["addprog", 2], ["addfail", 4], ["addeng", 1]]), Result("NO?", "After not installing a coffee machine...", [["addfail", -1]])], 1)			
coffeee = Prompt("", "Can we install a coffeee machine in the rocket?", [Result("NO?", "After not installing a coffee machine...", [["addfail", -1]])], 1)			

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

possiblequestions = [coffee, coffeee]	
questions = [coffee, coffeee]
newday = True	
mouse_down = False
done, running = False, True

while running:
	#Before choosing an answer
	theQuestion = possiblequestions[random.randint(0, len(questions) - 1)]
	
	done = False
	while not done:
	
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				done, running = True, False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_down = True
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_down = False
		mouse_pos = pygame.mouse.get_pos()
		
		
		if mouse_down:
			for i in range(len(theQuestion.results)):
				if hitDetect(mouse_pos, mouse_pos, [50, 450 + i * 50], [650, 525 + i * 50]):
					mouse_down = False
					theQuestion.results[i].decide(player)
					possiblequestions.remove(theQuestion)
					for q in questions:
						q.daysSince +=1
						if q.daysSince >= q.cooldown:
							possiblequestions.append(q)
		
		gScreen.fill(WHITE)
		gScreen.blit(font.render(theQuestion.prompt, True, BLACK), [200, 100])
		
		y = 0
		for i in theQuestion.results:
			pygame.draw.rect(gScreen, GREY, [50, 450 + y * 50, 600, 25])
			gScreen.blit(font.render(i.desc,True,BLACK), [60, 455 + y * 50])
			y+= 1
		
		
		gScreen.blit(font.render(str(player.money),True,BLACK), [155 - 38, 50])
		gScreen.blit(font.render(str(player.progress),True,BLACK), [233 - 38, 50])
		gScreen.blit(font.render(str(player.failChance),True,BLACK), [311 - 38, 50])
		gScreen.blit(font.render(str(player.scientists),True,BLACK), [388 - 38, 50])
		gScreen.blit(font.render(str(player.engineers),True,BLACK), [466 -38, 50])
		gScreen.blit(font.render(str(player.maths),True,BLACK), [544 - 38, 50])
		gScreen.blit(font.render(str(player.campaigners),True,BLACK), [622 - 38, 50])
		
		pygame.display.update()
		clock.tick(60)

	#after choosing an answer

	
	