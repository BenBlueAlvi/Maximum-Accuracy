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


pygame.init()
font = pygame.font.SysFont('Calibri', 15, True, False)
size = (700, 700)
gScreen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Maximum Accuracy")

def getImg(name):
	full = "Assets/"+name+".png"
	print "Loading: "+full
	return pygame.image.load(full)
	
sciencepic = getImg("science")
progresspic = getImg("progress")
failurepic = getImg("failure")
mathspic = getImg("maths")
engiespic = getImg("engies")
campainerspic = getImg("campainers")
moneypic = getImg("money")
end_of_day_pic = getImg("backgrounds/end_of_day")
continuepic = getImg("buttons/continue")
launchpic = getImg("buttons/launch")
tippic = getImg("tip")
capstrip1 = getImg("capstrip1")
vertstrip = getImg("vertstrip")
capstrip2 = getImg("capstrip2")

class button(object):
	def __init__(self, image, hoverimg):
		self.image = image
		self.hoverimg = hoverimg
	def buildNew(self):
		newButton = button(getImg("buttons/"+self.image), getImg("buttons/"+self.hoverimg))
		return newButton
		
responseButton = button("button", "button_hover").buildNew()

def bubble_sort(items):
	""" Implementation of bubble sort """
	for i in range(len(items)):
		for j in range(len(items)-1-i):
			if items[j] > items[j+1]:
				items[j], items[j+1] = items[j+1], items[j] 
	return items
	
def wraptext(text, fullline):
	Denting = True
	count = fullline
	size = pygame.font.size(text)
	outtext = []
	while Denting:
		if pygame.font.size(text)[0] > fullline:
			#Search for ammount of charachters that can fit in set fullline size
			thistext = ""
			for i in range(900):
				if pygame.font.size(thistext + text[i])[0] > fullline:
					count = len(thistext)
				else:
					thistext += text[i]
			thistext = text[:count]
			#is it indentable
			if " " in thistext:
				for i in range(len(thistext)):
					#find first space
					if thistext[len(thistext)-(i+1)] == " ":
						if i > (fullline/4):
							count += fullline #to prevent largly empty lines. USE SKIPS TO COUNTER
						#split text, add indent, update count
						else:
							outtext.append(thistext[:len(thistext)-(i+1)])
							text = text[len(thistext)-(i):]
							count = fullline
							break
			#unindentable, skip to next
			else:
				count += fullline
		else:
			#exit denting, add remaining to outtext, return
			Denting = False
			outtext = outtext+text+"\n"
		#time.sleep(1)
	return outtext
	

	
	
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
			
			if o == "addflav":
				self.feedback.append(n)
			if o == "addprog":
				if n < 0:
					self.feedback.append("The rocket loses progresses by "+str(n) + "%")
				else:
					self.feedback.append("The rocket progresses by "+str(n) + "%")
				player.progress += player.mult*n
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
					self.feedback.append("You have lost "+str(-n)+" scientists.")
				else:
					self.feedback.append("You hire "+str(n)+" scientists")
				player.scientists += n
			if o == "addeng":
				if n < 0:
					self.feedback.append("You have lost "+str(-n)+" engineers.")
				else:
					self.feedback.append("You hire "+str(n)+" engineers")
				player.engineers += n
			if o == "addmat":
				if n < 0:
					self.feedback.append("You have lost "+str(-n)+" mathematitions.")
				else:
					self.feedback.append("You hire "+str(n)+" mathematitions")
				player.maths += n
			if o == "addcam":
				if n < 0:
					self.feedback.append("You have lost "+str(-n)+" campaigners.")
				else:
					self.feedback.append("You hire "+str(n)+" campaigners")
				player.campaigners += n
			if o == "addpop":
				sciHired = 0
				engHired = 0
				mathsHired = 0
				camHired = 0
				for i in range(n):
					rand = random.randint(1, 4)
					if rand == 1:
						sciHired += 1
					if rand == 2:
						engHired += 1
					if rand == 3:
						mathsHired += 1
					if rand == 4:
						camHired += 1
				
				self.feedback.append("You hire "+str(sciHired)+" scientists")
				player.scientists += sciHired
				self.feedback.append("You hire "+str(engHired)+" engineers")
				player.engineers += engHired
				self.feedback.append("You hire "+str(mathsHired)+" mathematitions")
				player.maths += mathsHired
				self.feedback.append("You hire "+str(camHired)+" campaigners")
				player.campaigners += camHired
				
			if o == "subpop":
				sciHired = 0
				engHired = 0
				mathsHired = 0
				camHired = 0
				for i in range(n):
					rand = random.randint(1, 4)
					if rand == 1:
						sciHired -= 1
					if rand == 2:
						engHired -= 1
					if rand == 3:
						mathsHired -= 1
					if rand == 4:
						camHired -= 1
				
				self.feedback.append("You hire "+str(sciHired)+" scientists")
				player.scientists += sciHired
				self.feedback.append("You hire "+str(engHired)+" engineers")
				player.engineers += engHired
				self.feedback.append("You hire "+str(mathsHired)+" mathematitions")
				player.maths += mathsHired
				self.feedback.append("You hire "+str(camHired)+" campaigners")
				player.campaigners += camHired
				
			if o == "overtime":
				rand = n * ((2*player.campaigners) - (player.engineers * player.cost))
				rand2 = player.mult * n * ((.2*player.scientists)+1)*player.engineers*0.4
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
				
				self.feedback.append("The rocket progresses by "+str(rand2)+"%")
				player.progress += rand2
			if o == "addmult":
				if n < 0:
					if player.mult + n < 0:
						self.feedback.append("Your plans cannot grow any grander.")
						break
					else:
						self.feedback.append("Your spaceship plans have grown.")
						player.mult += n
				else:
					self.feedback.append("Your spaceship plans have shrunk.")
					player.mult += n
			if o == "multprog":
				if n < 1:
					self.feedback.append("Your progress has reduced")
				else:
					self.feedback.append("Your progress has advanced")
				player.progress *= n
			if o == "addcost":
				if n < 0:
					if player.cost + n < 0:
						self.feedback.append("The cost cannot be reduced further.")
						break
					else:
						self.feedback.append("The cost has reduced.")
						player.cost += n
				else:
					self.feedback.append("The cost has increased.")
					player.cost += n
			if o == "multcost":
				if n < 1:
					self.feedback.append("Your costs have reduced")
				else:
					self.feedback.append("Your costs have inrceased")
				player.progress *= n
				
		return self.feedback

class Prompt(object):
	def __init__(self, name, prompt, results, cooldown):
		self.name = name
		self.prompt = prompt
		self.results = results
		self.cooldown = cooldown
		self.daysSince = 0
	

#Staff management
hire1 = Prompt("", ["Your advisor from the government approches you:", "I would like to suggest we hire new staff."], [Result("Sure, I'll leave it up to you.", "You manage to hire 2 new people.", [["addmoney", -4], ["addpop", 2]]), Result("Let's hire some Campaigners.", "You attempt to hire campaigners.", [["addmoney", -2], ["addcam", 1]]), Result("Let's just focus on working today.", "after convincing your staff to work overtime..", [["overtime", 0.2]])], 2)
#hire2 = engineers, scientists
#hire3 = maths, campaigners
#fire1 = sci, eng, mat
fire1 = Prompt("", ["That one advisor from the government approches you:", "We have hired too many people and we are losing money", "somebody needs to get fired."], [Result("But we are getting so much done.", "After not firing anyone...", [["addfail", 2]]), Result("I'll leave it up to you.", "After that government advisor fires some people...", [["subpop", 3], ["addfail", -2]]),Result("Fire some of those engineers.", "After firing some engineers...", [["addeng", -2], ["addfail", -1]])], 6)
#Money and materials
bakesale = Prompt("", ["One of your campaigners suggests:", "We should have a bake sale to raise money."], [Result("Sure, but only if I can have some too.", "After having a bakesale", [["addmoney", 2], ["addflav", "The bake sale premotes working in the areospace industy"], ["addpop", 1]]), Result("No, I hate baked goods", "After not having a bake sale..", [["addflav", "Some people were really looking forward to that bake sale."],["subpop", 1]])], 3)
adcampaign = Prompt("", ["One of your mathmatitions suggests", "an add campaign to hire people."], [Result("Yeah, we need the staff", "After creating an amazing ad campaign...", [["addmoney", -4], ["addpop", 4]]), Result("No, we don't have enough money.", "After not creating an amazing ad campaign...", [["addflav", "Nothing changes"]])], 5)
materials = Prompt("", ["One of your scientists approaches you:", "We need to discuss our materials."], [Result("How about all carbon fiber?", "After using hi-tech materials:", [["addfail", -4], ["addcost", 2]]), Result("Why not normal materials, like steel?", "After deciding to use standard materials:", [["addflav", "Engineers are attracted to the ease of their jobs."], ["addeng", 1]]), Result("Lets think cheap. Duct-tape cheap.", "After deciding to use low-cost materials:", [["addcost", -.5], ["addmult", .1], ["addfail", 20], ["addflav", "Some of your mathmatitions can't handle the absurdity of this project."], ["addmat", -2]])], 99)
fuels = Prompt("", ["An engineer approaches you:", "So, uh.. What should we use for fuel?"], [Result("Nuclear would be the most effeicent", "After deciding to place a nuclear reactor within the rocket", [["addfail", -10], ["addmoney", -10]]), Result("Rocket fuel, duh.", "After using standard rocket fuel..", [["addfail", -5], ["addmoney", -7]]), Result("Car fuel, we are low on funds", "After deciding to use car fuel...", [["addflav", "Some people belive you aren't taking this job seriously"], ["subpop", 2],["addfail", -2], ["addmoney", -4]])], 99)


#Bad ideas
coffee = Prompt("", ["A few engineers approch you and ask:", "Can we install a coffee machine in the rocket?"], [Result("Sure, Why not?", "After installing a coffee machine on the rocket,", [["addmoney", -1], ["addprog", 2], ["addfail", 4], ["addeng", 1]]), Result("NO?", "After not installing a coffee machine...", [["addfail", -1]])], 1)			
toaster = Prompt("", ["One of those hippies from science department asks:", "Hey, we're low on funds right now. I suggest we turn our chassis into a toaster."], [Result("Sure, we need to save money.", "After switching over your chassis:", [["addmult", 2], ["addfail", 100], ["addmat", -2], ["addprog", 2]]), Result("We don't need to be THAT drastic..", "After reducing the size:", [["addmult", .2], ["addfail", -1], ["addsci", 1]]), Result("No way.", "After denying the toaster plan:", [["addmat", 1], ["addpop", 1]])], 3)
hotel = Prompt("", ["The CEO of a large hotel group has approched you", "and wishes install one of his hotels on the moon.", "He bribes you with quite a bit of money."], [Result("I guess so.", "The engineers begin to load materials to build the hotel on the moon.", [["multprog", .2], ["addmult", -.8], ["addfail", 30], ["addmoney", 30]]), Result("No.", "After focusing on building the rocket and not business deals:", [["addprog", 5], ["addpop", 1]])], 3)
#mtndew
#sodamachine

#interesting ideas
fsc = Prompt("", ["Upon seeing how well the rocket is going", "an advisor from the Futuristic Science Corp.", "wishes to partner with you."], [Result("Together we will do great things.", "After partnering with the FSC...", [["addflav", "The project has drasticly increased in size."], ["addmoney", 20], ["addmult", 0.1]]), Result("I'm sorry, I would prefer to go alone.", "After making the mistake of not partnering with the FSC..", [["addflav", "You feel you have made a horrible mistake."]])], 99)

possiblequestions = [coffee, hire1, materials, fuels, adcampaign, fsc]	
questions = [coffee, hire1, hotel, toaster, materials, fuels, bakesale]

class Player(object):
	def __init__(self, mon, prog, fail, sci, eng, mat, cam):
		self.money = mon
		self.progress = prog
		self.failChance = fail
		self.fails = 0
		self.scientists = sci
		self.engineers = eng
		self.cost = 1
		self.maths = mat
		self.campaigners = cam
		self.mult = 1
		self.pop = 0
		#previous
		self.preMon = mon
		self.preProg = prog
		self.preFail = fail

player = Player(18, 0, 100, 1, 2, 1, 0)

class Achive(object):
	def __init__(self, Id, name, desc, img):
		self.id = Id
		self.name = name
		self.desc = desc
		self.img = img

#Atoast = Achive("toaster", "It could run on a toaster", "Succesfully launch a spaceship with a toaster chassis", )

def addQuestion(possiblequestions, parm, comp, limit, question):
	if comp == "greater":
		if parm > limit and not question in possiblequestions:
			possiblequestions.append(question)
		elif parm < limit and question in possiblequestions:
			possiblequestions.remove(question)
	elif comp == "lesser":
		if parm < limit and not question in possiblequestions:
			possiblequestions.append(question)
		elif parm > limit and question in possiblequestions:
			possiblequestions.remove(question)

funded = True	
mouse_down = False

done, running = False, True
def textbox(size, text):
	global capstrip1, capstrip2, vertstrip
	text = wraptext(text, 248)
	textbox = pygame.Surface(size)
	for i in range(size[1]):
		if i == 0:
			textbox.blit(capstrip2, [0, i])
		elif i == 1:
			textbox.blit(capstrip1, [0, i])
		elif i == size[1] - 2:
			textbox.blit(capstrip1, [0, i])
		elif i == size[1] - 1:
			textbox.blit(capstrip2, [0, i])
		else:
			textbox.blit(vertstrip, [0, i])
	return textbox
while running:
	player.pop = player.scientists + player.maths + player.campaigners + player.engineers
	
	#Before choosing an answer
	
	addQuestion(possiblequestions, player.money, "lesser", 6, hotel)
	
	addQuestion(possiblequestions, player.money, "lesser", 4, toaster)
	
	addQuestion(possiblequestions, player.money, "lesser", 8, bakesale)
	
	addQuestion(possiblequestions, player.pop, "greater", 10, fire1)
		
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
		
		
			
		
		gScreen.fill(WHITE)
		
		gScreen.blit(textbox([250, 50], ""), [0,0])
		
		for i in range(len(theQuestion.prompt)):
		
			gScreen.blit(font.render(theQuestion.prompt[i], True, BLACK), [200, 100 + i * 20])
			
		y = 0
		for i in theQuestion.results:
			displayresult = True
			for doing in i.doings:
				if doing[0] == "addmoney" and doing[1] * -1 > player.money:
					displayresult = False
			
			if displayresult:
				gScreen.blit(responseButton.image, [50, 450 + y * 50])
		
				gScreen.blit(font.render(i.desc,True,BLACK), [60, 455 + y * 50])
				
				if mouse_down:
					if hitDetect(mouse_pos, mouse_pos, [50, 450 + y * 50], [650, 475 + y * 50]):
						mouse_down = False
						feedback = i.decide(player)
						possiblequestions.remove(theQuestion)
						for q in questions:
							q.daysSince +=1
							if q.daysSince >= q.cooldown:
								possiblequestions.append(q)
						done = True
						break
				
				
		
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
		
		if hitDetect(mouse_pos, mouse_pos, [155 - 38, 10], [155 + 50 - 38, 60]):
			gScreen.blit(tippic, [mouse_pos[0], mouse_pos[1] + 20])
			gScreen.blit(font.render("This is your money. You run out, you get fired.", True, BLACK), [mouse_pos[0] + 10, mouse_pos[1] + 22])
		elif hitDetect(mouse_pos, mouse_pos, [233 - 38, 10], [233 + 50 - 38, 60]):
			gScreen.blit(tippic, [mouse_pos[0], mouse_pos[1] + 20])
			gScreen.blit(font.render("Rocket progress. Higher progress means better launch.", True, BLACK), [mouse_pos[0] + 10, mouse_pos[1] + 22])	
		elif hitDetect(mouse_pos, mouse_pos, [311 - 38, 10], [311 + 50 - 38, 60]):
			gScreen.blit(tippic, [mouse_pos[0], mouse_pos[1] + 20])
			gScreen.blit(font.render("Fail chance increases the chance of explosions.", True, BLACK), [mouse_pos[0] + 10, mouse_pos[1] + 22])
		elif hitDetect(mouse_pos, mouse_pos, [388 - 38, 10], [388 + 50 - 38, 60]):
			gScreen.blit(tippic, [mouse_pos[0]- 250, mouse_pos[1] + 20])
			gScreen.blit(font.render("Scientists increase the efficiency of your engineers.", True, BLACK), [mouse_pos[0] + 10 - 250, mouse_pos[1] + 22])
		elif hitDetect(mouse_pos, mouse_pos, [466 - 38, 10], [466 + 50 - 38, 60]):
			gScreen.blit(tippic, [mouse_pos[0] - 450, mouse_pos[1] + 20])
			gScreen.blit(font.render("Engineers spend money to buy resources and work on the rocket.", True, BLACK), [mouse_pos[0] + 10 - 450, mouse_pos[1] + 22])
		elif hitDetect(mouse_pos, mouse_pos, [544 - 38, 10], [544 + 50 - 38, 60]):
			gScreen.blit(tippic, [mouse_pos[0] - 450, mouse_pos[1] + 20])
			gScreen.blit(font.render("Mathematitians decrease the chance of failiure of launch.", True, BLACK), [mouse_pos[0] + 10 - 450, mouse_pos[1] + 22])
		elif hitDetect(mouse_pos, mouse_pos, [622 - 38, 10], [622 + 50 - 38, 60]):
			gScreen.blit(tippic, [mouse_pos[0] - 450, mouse_pos[1] + 20])
			gScreen.blit(font.render("Campaigners spend their time advertising and gaining more money.", True, BLACK), [mouse_pos[0] + 10 - 450, mouse_pos[1] + 22])
		
			
			
			#This is your money. You run out, you get fired.
			#Rocket progress. Higher progress means better launch.
			#Fail chance increases the chance of explosions.
			#Mathematitians decrease the chance of failiure of launch.
			#Scientists increase the efficiency of your engineers.
			#Engineers spend money to buy resources and work on the rocket.
			#Campaigners spend their time advertising and gaining more money.	 <----- Longest tooltip

			
			
		pygame.display.update()
		clock.tick(60)

	#after choosing an answer
	
	player.failChance -= 2*player.maths
	if player.failChance < 1:
		player.failChance = 1
	player.progress += player.mult * ((.2*player.scientists)+1)*player.engineers*0.4
	player.money += ((2 * player.campaigners) - (player.engineers + player.maths + player.scientists + player.cost*player.engineers))
	feedback1 = []
	feedback1.append("After a full day of work...")
	if player.campaigners > 0:
		feedback1.append("Your campaigners raise "+str(2*player.campaigners)+"K")
	if funded:
		#6 is default reduced per turn with 1 sci & math, and 2 eng
		player.money += 8
		feedback1.append("You gain 8K in government funding.")
		
	feedback1.append("You pay your employees "+str(player.maths+player.scientists+player.engineers)+"K")
	feedback1.append("Your engineers spend "+str(player.engineers*player.cost)+"K")
	feedback1.append("Your mathematitions reduce chance of failiure by "+str(2*player.maths)+"%")
	
	
	feedback1.append("")
	feedback1 += feedback
	feedback1.append("")
	feedback1.append("Net progress: "+str(player.progress - player.preProg)+"%")
	feedback1.append("Net money: "+str(player.money - player.preMon)+"K")
	feedback1.append("Net fail chance: "+str(player.failChance - player.preFail)+"%")
	#feedback1.append("Current progress: "+str(player.progress)+"%")
	player.preMon, player.preProg, player.preFail = player.money, player.progress, player.failChance
	
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
				
			elif event.type == pygame.MOUSEBUTTONUP:
				mouse_down = False
		mouse_pos = pygame.mouse.get_pos()

		#launch button, and continue button.
		if hitDetect(mouse_pos, mouse_pos, [10,640], [180, 690]) and mouse_down:
			mouse_down = False
			successChance = player.progress / player.failChance
			launchChance = random.randint(0, 100)
			rand = 100 - launchChance
			
			if launchChance <= successChance:
				print "LAUNCH SUCCESSFUL!"
				
			if launchChance > successChance and launchChance <= successChance + (rand * 1 / 3):
				print "LAUNCH Failure 1!"
				
			if launchChance > successChance + (rand * 1 / 3) and launchChance <= successChance + (rand * 2 / 3):
				print "LAUNCH Failure 2!"
				
			if launchChance > successChance + (rand * 2 / 3):
				print "LAUNCH Failure 3!"
				
			player.fails += 1
			player.progress, player.cost, player.mult = 0, 1, 1
			
			done = True
		if hitDetect(mouse_pos, mouse_pos, [10,580], [180, 630]) and mouse_down:
			done = True
				
		
		gScreen.blit(continuepic, [10, 580])
		gScreen.blit(launchpic, [10, 640])

		pygame.display.update()
		clock.tick(60)

