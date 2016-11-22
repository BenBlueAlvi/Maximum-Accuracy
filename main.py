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

#This is your money. You run out, you get fired.
#Rocket progress. Higher progress means better launch.
#Fail chance increases the chance of explosions.
#Mathematitians decrease the chance of failiure of launch.
#Scientists increase the efficiency of your engineers.
#Engineers spend money to buy resources and work on the rocket.
#Campaigners spend their time advertising and gaining more money.

pygame.init()
font = pygame.font.SysFont('Calibri', 15, True, False)
size = (700, 700)
gScreen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

pygame.display.set_caption("Maximum Accuracy")
sciencepic = pygame.image.load("Assets/science.png")
progresspic = pygame.image.load("Assets/progress.png")
failurepic = pygame.image.load("Assets/failure.png")
mathspic = pygame.image.load("Assets/maths.png")
engiespic = pygame.image.load("Assets/engies.png")
campainerspic = pygame.image.load("Assets/campainers.png")
moneypic = pygame.image.load("Assets/money.png")
end_of_day_pic = pygame.image.load("Assets/end_of_day.png")

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
		self.feedback = [result]
	
	def decide(self, player):
		self.feedback = [self.result]
		for i in range(len(self.doings)):
			o, n = self.doings[i][0], self.doings[i][1]
			
			if o == "addprog":
				if n < 0:
					self.feedback.append("The rocket loses progresses by "+str(n) + "%")
				else:
					self.feedback.append("The rocket progresses by "+str(n) + "%")
				player.progress += n
			if o == "addmoney":
				if n < 0:
					if player.money + n < 0:
						self.feedback.append("You realize you don't have enough funds.")
						break
					else:
						player.money += n
						self.feedback.append("You spend $"+str(-n)+"K")
				else:
					player.money += n
					self.feedback.append("You gain $"+str(n)+"K")
			if o == "addfail":
				if n < 0:
					self.feedback.append("Estamates show that the chance of faliure has decreased by "+str(-n)+"%")
				else:
					self.feedback.append("Estamates show that the chance for faliure has increased by "+str(n)+"%")
				player.failChance += n
			if o == "addsci":
				if n < 0:
					self.feedback.append(str(-n)+" scientists have quit.")
				else:
					self.feedback.append("You hire "+str(n)+" scientists")
				player.scientists += n
			if o == "addeng":
				if n < 0:
					self.feedback.append(str(-n)+" engineers have quit.")
				else:
					self.feedback.append("You hire "+str(n)+" engineers")
				player.engineers += n
			if o == "addmat":
				if n < 0:
					self.feedback.append(str(-n)+" mathematitions have quit.")
				else:
					self.feedback.append("You hire "+str(n)+" mathematitions")
				player.maths += n
			if o == "addcam":
				if n < 0:
					self.feedback.append(str(-n)+" campaigners have quit.")
				else:
					self.feedback.append("You hire "+str(n)+" campaigners")
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
			if o == "overtime":
				rand = n * ((2*player.campaigners) - (player.engineers + player.scientists))
				rand2 = n * ((.2*player.scientists)+1)*player.engineers*0.4
				if rand < 0:
					if player.money - rand < 0:
						self.feedback.append("You realize you don't have enough funds.")
						break
					else:
						self.feedback.append("You spend $"+str(-rand)+"K.")
						player.money += rand
				else:
					self.feedback.append("You gain $"+str(rand)+"K.")
					player.money += rand
				
				self.feedback.append("The rocket loses progresses by "+str(rand2)+"%")
				player.progress += rand2

		return self.feedback

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

coffee = Prompt("", ["A few engineers approch you and ask:", "Can we install a coffee machine in the rocket?"], [Result("Sure, Why not?", "After installing a coffee machine on the rocket,", [["addmoney", -1], ["addprog", 2], ["addfail", 4], ["addeng", 1]]), Result("NO?", "After not installing a coffee machine...", [["addfail", -1]])], 1)			
coffeee = Prompt("", ["A few engineers approch you and ask:", "Can we install a coffeee machine in the rocket?"], [Result("NO?", "After not installing a coffee machine on the rocket,", [["addfail", -1]])], 1)			
hire1 = Prompt("", ["Your advisor from the government approches you:", "I would like to suggest we hire new staff."], [Result("Sure, I'll leave it up to you.", "You manage to hire 2 new people.", [["addmoney", -4], ["addpop", 2]]), Result("Let's hire some Campaigners.", "You attempt to hire campaigners.", [["addmoney", -2], ["addcam", 1]]), Result("Let's just focus on working today.", "after convincing your staff to work overtime..", [["overtime", 0.4]])], 2)
#hire2 = engineers, scientists
#hire3 = maths, campaigners
#bakesale
#adcampaign
#toaster
#hotel = build hotel on moon
hotel = Prompt("", ["The CEO of a large hotel group has approched you", "and wishes install one of his hotels on the moon.", "He bribes you with quite a bit of money."], [Result("I guess so.", "The engineers begin to load materials to build the hotel on the moon.", [["addfail", -20], ["addmoney", 30]]), Result("No.", "After focusing on building the rocket and not business deals:", [["addprog", 5], ["addpop", 1]])], 1)
#mtndew
#sodamachine

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

player = Player(18, 0, 100, 1, 2, 1, 0)

class button(object):
	def __init__(self, image, hoverimg):
		self.image = image
		self.hoverimg = hoverimg
	def buildNew(self):
		newButton = button(pygame.image.load(self.image), pygame.image.load(self.hoverimg))
		return newButton
responseButton = button("Assets/button.png", "Assets/button_hover.png").buildNew()


possiblequestions = [coffee, coffeee, hire1]	
questions = [coffee, coffeee, hire1, hotel]
funded = True	
mouse_down = False

done, running = False, True

while running:
	#Before choosing an answer
	if player.money < 4 and not hotel in possiblequestions:
		possiblequestions.append(hotel)
		
	theQuestion = possiblequestions[random.randint(0, len(possiblequestions) - 1)]
	done, mouse_down = False, False
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
				gScreen.blit(responseButton.image, [50, 450 + i * 50])
				if hitDetect(mouse_pos, mouse_pos, [50, 450 + i * 50], [650, 475 + i * 50]):
					mouse_down = False
					feedback = theQuestion.results[i].decide(player)
					possiblequestions.remove(theQuestion)
					for q in questions:
						q.daysSince +=1
						if q.daysSince >= q.cooldown:
							possiblequestions.append(q)
					done = True
		
		gScreen.fill(WHITE)
		for i in range(len(theQuestion.prompt)):
		
			gScreen.blit(font.render(theQuestion.prompt[i], True, BLACK), [200, 100 + i * 20])
			
		y = 0
		for i in theQuestion.results:
			gScreen.blit(responseButton.image, [50, 450 + y * 50])
		
			gScreen.blit(font.render(i.desc,True,BLACK), [60, 455 + y * 50])
		
			y+= 1

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

		gScreen.blit(font.render(str(player.money)+"K",True,BLACK), [155 - 38, 60])
		gScreen.blit(font.render(str(player.progress)+"%",True,BLACK), [233 - 38, 60])
		gScreen.blit(font.render(str(player.failChance)+"%",True,BLACK), [311 - 38, 60])
		gScreen.blit(font.render(str(player.scientists),True,BLACK), [388 - 38, 60])
		gScreen.blit(font.render(str(player.engineers),True,BLACK), [466 -38, 60])
		gScreen.blit(font.render(str(player.maths),True,BLACK), [544 - 38, 60])
		gScreen.blit(font.render(str(player.campaigners),True,BLACK), [622 - 38, 60])
		
		pygame.display.update()
		clock.tick(60)

	#after choosing an answer
	feedback1 = []
	feedback1.append("After a full day of work...")
	if player.campaigners > 0:
		player.money += 2*player.campaigners
		feedback1.append("Your campaigners raise "+str(2*player.campaigners)+"K")
	if funded:
		#6 is default reduced per turn with 1 sci & math, and 2 eng
		player.money += 8
		feedback1.append("You gain 8K in government funding.")
	player.money += ((2 * player.campaigners) - (2*player.engineers + player.maths + player.scientists))
	feedback1.append("You pay your employees "+str(player.maths+player.scientists+player.engineers)+"K")
	feedback1.append("Your engineers spend "+str(player.engineers)+"K")
	feedback1.append("Your mathematitions reduce chance of failiure by "+str(2*player.maths)+"%")
	
	player.failChance -= 2*player.maths
	if player.failChance < 0:
		player.failChance = 0
	player.progress += ((.2*player.scientists)+1)*player.engineers*0.4
	
	feedback1.append("")
	feedback1 += feedback
	feedback1.append("")
	feedback1.append("You gain "+str(((.2*player.scientists)+1)*player.engineers*0.4)+"% progress on the ship.")
	feedback1.append("Current progress: "+str(player.progress)+"%")
	if player.money <= 0:
		feedback1.append("You have run out of money. You might want to launch...")

	feedback = feedback1

	done, mouse_down = False, False
	while not done and running:
		gScreen.fill(WHITE)
		gScreen.blit(end_of_day_pic, [190, 90])
		for i in range(len(feedback)):
			gScreen.blit(font.render(feedback[i], True, BLACK), [200, 100+(i*20)])
		
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				done, running = True, False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_down = True
				done = True
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_down = False
		mouse_pos = pygame.mouse.get_pos()
		#launch button, and continue button.
		pygame.display.update()
		clock.tick(60)

