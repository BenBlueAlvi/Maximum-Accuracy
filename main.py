import random
import math
import pygame

clock = pygame.time.Clock()

pygame.mixer.pre_init(22050, -16, 3, 8)
pygame.mixer.init()

debug = True
def prints(stuff):
	global debug
	if debug:
		print stuff

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREY = (150,150,150)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
TEAL = (0, 255, 255)


pygame.init()
font = pygame.font.SysFont('Calibri', 15, True, False)
achiveFont = pygame.font.SysFont('Calibri', 10, True, False)

size = (700, 700)
gScreen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Maximum Accuracy")

def getImg(name):
	full = "Assets/"+name+".png"
	print "Loading: "+full
	try:
		return pygame.image.load(full)
	except pygame.error:
		print "File not found. Substituting"
		return pygame.image.load("Assets/achives/wip.png")

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
achiveBox = getImg("achives/achiveBox")
explosion = pygame.mixer.Sound("Assets/soundfx/Explosion.wav")
launch = pygame.mixer.Sound("Assets/soundfx/Launch.wav")
select = pygame.mixer.Sound("Assets/soundfx/Blip_Select.wav")
new_day = pygame.mixer.Sound("Assets/soundfx/New_Day.wav")
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
	
def wraptext(text, fullline, Font):
	Denting = True
	count = fullline
	size = Font.size(text)
	outtext = []
	while Denting:
		if Font.size(text)[0] > fullline:
			#Search for ammount of charachters that can fit in set fullline size
			thistext = ""
			for i in range(900):
				if Font.size(thistext + text[i])[0] > fullline:
					count = len(thistext)
					break
				else:
					thistext += text[i]
			thistext = text[:count]
			#is it indentable
			if " " in thistext:
				for i in range(len(thistext)):
					#find first space from end
					if thistext[len(thistext)-(i+1)] == " ":
						#split text, add indent, update count
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
			outtext.append(text)
	return outtext

rand = wraptext("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", 100, font)
for i in rand:
	print i
del rand

def textbox(size, text, Font):
	global capstrip1, capstrip2, vertstrip
	#text = wraptext(text, 292, Font)
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

class shipPart(object):
	def __init__(self, name, cost, percent, fail, image):
		self.name = name
		self.cost = cost
		self.perc = percent
		self.fail = fail
		self.img = image

#part variables start with P, part types are B (booster), M (main), C (chassis), materials have M with a T (tape), I (iron), N (nano)
#frames and materials
Pframe = getImg("parts/Scaffold")
PMT = shipPart("Tape", -.2, 0, 0.5, getImg("parts/matTape"))
PMI = shipPart("Iron", 0, 0, 0, getImg("parts/mainMatIron"))
PMN = shipPart("Nano", 0.5, 10, -.2, getImg("parts/matNano"))
#Boosters
PBnormal = shipPart("Normal", 0.2, 30, 0, getImg("parts/boosterNormal"))
PBsilo = shipPart("Silo", 0.1, 28, 0.4, getImg("parts/boosterSilo"))
#Mains
PMnuclear = shipPart("Nuclear", 0.5, 60, 0.1, getImg("parts/mainNuclear"))
PMnormal = shipPart("Normal", 0.4, 50, 0, getImg("parts/mainNorm"))
PMcar = shipPart("Car", 0.3, 40, 0.1, getImg("parts/mainCar"))
#Chassis
PCtoaster = shipPart("Toaster", 0.1, 4, 1, getImg("parts/chassisToaster"))
PCnormal = shipPart("Normal", 0.4, 20, 0, getImg("parts/chassisNormal"))
PChotel = shipPart("Hotel", 0.4, 100, 1, getImg("parts/chassisHotel"))

#takes in materials
def frameImg(mat):
	thisship = pygame.Surface((200, 240), pygame.SRCALPHA, 32).convert_alpha()
	thisship.blit(Pframe, [0, 0])
	thisship.blit(mat.img, [0, 0])
	return thisship

#takes in parts
def spaceshipimg(pl):
	thisship = pygame.Surface((200, 240), pygame.SRCALPHA, 32).convert_alpha()
	thisship.blit(pl.booster.img, [0, 60])
	thisship.blit(pl.booster.img, [140, 60])
	thisship.blit(pl.main.img, [60, 100])
	thisship.blit(pl.chassis.img, [70, 0])
	return thisship

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
					self.feedback.append("The rocket loses "+str(-n) + "% progress.")
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
				sciHired = 0
				for i in range(abs(n)):
					if n > 0:
						break
					else:
						if player.scientists - 1 < 0:
							break
						else:
							sciHired -= 1
				if sciHired < 0:
					self.feedback.append("You have lost "+str(-sciHired)+" scientists.")
				else:
					self.feedback.append("You hire "+str(n)+" scientists")
					sciHired = n
				player.scientists += sciHired
			if o == "addeng":
				engHired = 0
				for i in range(abs(n)):
					if n > 0:
						break
					else:
						if player.engineers - 1 < 0:
							break
						else:
							engHired -= 1
				if engHired < 0:
					self.feedback.append("You have lost "+str(-engHired)+" engineers.")
				else:
					self.feedback.append("You hire "+str(n)+" engineers")
					engHired = n
				player.engineers += engHired
			if o == "addmat":
				matHired = 0
				for i in range(abs(n)):
					if n > 0:
						break
					else:
						if player.maths - 1 < 0:
							break
						else:
							matHired -= 1
				if matHired < 0:
					self.feedback.append("You have lost "+str(-matHired)+" mathematitions.")
				else:
					self.feedback.append("You hire "+str(n)+" mathematitions")
					matHired = n
				player.maths += matHired
			if o == "addcam":
				camHired = 0
				for i in range(abs(n)):
					if n > 0:
						break
					else:
						if player.campaigners - 1 < 0:
							break
						else:
							camHired -= 1
				if camHired < 0:
					self.feedback.append("You have lost "+str(-camHired)+" campaigners.")
				else:
					self.feedback.append("You hire "+str(n)+" campaigners")
					camHired = n
				player.campaigners += camHired
			if o == "addpop":
				sciHired = 0
				engHired = 0
				matHired = 0
				camHired = 0
				for x in range(n):
					rand = random.randint(1, 4)
					if rand == 1:
						sciHired += 1
					if rand == 2:
						engHired += 1
					if rand == 3:
						matHired += 1
					if rand == 4:
						camHired += 1
				if sciHired > 0:
					self.feedback.append("You gain "+str(sciHired)+" scientists")
					player.scientists += sciHired
				if engHired > 0:
					self.feedback.append("You gain "+str(engHired)+" engineers")
					player.engineers += engHired
				if matHired > 0:
					self.feedback.append("You gain "+str(matHired)+" mathematitions")
					player.maths += matHired
				if camHired > 0:
					self.feedback.append("You gain "+str(camHired)+" campaigners")
					player.campaigners += camHired		
			if o == "subpop":
				sciHired = 0
				engHired = 0
				matHired = 0
				camHired = 0
				while n > 0:
					rand = random.randint(1, 4)
					n -= 1
					if rand == 1:
						if player.scientists - 1 < 0:
							n += 1
						else:
							sciHired += 1
					if rand == 2:
						if player.engineers - 1 < 0:
							n += 1
						else:
							engHired += 1
					if rand == 3:
						if player.maths - 1 < 0:
							n += 1
						else:
							matHired += 1
					if rand == 4:
						if player.campaigners - 1 < 0:
							n += 1
						else:
							camHired += 1
					if player.scientists <= 0 and player.engineers <= 0 and player.maths <= 0 and player.campaigners <= 0:
						n = -1
				if sciHired > 0:
					self.feedback.append("You lose "+str(sciHired)+" scientists")
					player.scientists -= sciHired
				if engHired > 0:
					self.feedback.append("You lose "+str(engHired)+" engineers")
					player.engineers -= engHired
				if matHired > 0:
					self.feedback.append("You lose "+str(matHired)+" mathematitions")
					player.maths -= matHired
				if camHired > 0:
					self.feedback.append("You lose "+str(camHired)+" campaigners")
					player.campaigners -= camHired
				if n == -1:
					self.feedback.append("You have no employees remaining.")
			
			if player.campaigners < 0:
				player.campaigners = 0
			if player.maths < 0:
				player.maths = 0
			if player.scientists < 0:
				player.scientists = 0
			if player.engineers < 0:
				player.engineers = 0
			
			if o == "overtime":
				player.time += n
				if n > 0:
					self.feedback.append("Your employees work overtime.")
				else:
					self.feedback.append("Your employees spend less time working.")
			if o == "multprog":
				if n < 1:
					self.feedback.append("Your progress has reduced")
				else:
					self.feedback.append("Your progress has advanced")
				player.progress *= n
			if o == "addIfactor":
				if n < 1:
					self.feedback.append("Mathematitians are having an easy time working on the rocket.")
				else:
					self.feedback.append("Mathematitians are having a hard time working on the rocket.")
				
				player.impossiblilyFactor += n
				if player.impossiblilyFactor <= 0:
					player.impossiblilyFactor = 0.1
			if o == "reduce":
				if player.material == PMI:
					player.material = PMT
				elif player.material == PMN:
					player.material = PMI
				self.feedback.append("Your project has shrunk.")
				player.setpart("material")
			if o == "addTime":
				if n < 0:
					if player.baseTime + n < 0:
						self.feedback.append("Your work hours cannot shrink any more.")
					else:
						self.feedback.append("Your work hours have shrunk.")
						player.baseTime += n
				else:
					if player.baseTime + n > 3:
						self.feedback.append("You cannot go above a 24 hour workday.")
					else:
						self.feedback.append("Your work hours have increased.")
						player.baseTime += n
			if o == "addflav":
				self.feedback.append(n)
			if o == "spec":
				if n == "caffinate":
					rand = True
					for x in range(len(player.specs)):
						if "caffine" in player.specs[x]:
							rand = False
							if "4" in player.specs[x]:
								player.specs[x] = "caffine5"
								self.feedback.append("Your employees are overcaffinated.")
								Acaffine.get()
							if "3" in player.specs[x]:
								player.specs[x] = "caffine4"
								self.feedback.append("Your employees are exremely hyper.")
							if "2" in player.specs[x]:
								player.specs[x] = "caffine3"
								self.feedback.append("Your employees are very active.")
							if "1" in player.specs[x]:
								player.specs[x] = "caffine2"
								self.feedback.append("Your employees are caffinated.")
					if rand:
						player.specs.append("caffine1")
						self.feedback.append("Your employees have access to caffine.")
				else:
					player.specs.append(n)
			if o == "removeSpec":
				if n in player.specs:
					player.specs.remove(n)
			if o == "rocketspec":
				player.rocketspecs.append(n)
			
			if o == "setMat":
				player.material = n
				if n == "tape":
					self.feedback.append("Your frame is cardboard duct taped together.")
				if n == "iron":
					self.feedback.append("Your frame is made from steel and iron.")
				if n == "nano":
					self.feedback.append("The ship has carbon fiber framing.")
				player.setpart("material")
			if o == "setpart":
				player.setpart(n)
		
		return self.feedback

class Prompt(object):
	def __init__(self, name, prompt, results, cooldown):
		self.name = name
		self.prompt = prompt
		self.results = results
		self.cooldown = cooldown
		self.daysSince = 0
#Staff management

hire1 = Prompt("hire1", ["Your advisor from the government approches you:", "I would like to suggest we hire new staff."], [Result("Sure, I'll leave it up to you.", "You manage to hire 2 new people.", [["addmoney", -4], ["addpop", 2]]), Result("Let's hire some Campaigners.", "You attempt to hire campaigners.", [["addmoney", -2], ["addcam", 2]]), Result("Let's hire some of thoose math people.", "After hiring some mathematitions people...", [["addmoney", -2], ["addmat", 2]]), Result("We need more science, we can never have enough science!", "After searching for more science.", [["addmoney", -2], ["addsci", 2], ["addflav", "Your science has increased!"]])], 4) 
hire2 = Prompt("hire2", ["A large group of papers is sitting on your desk", "They appear to all be applications for jobs"], [Result("This person has a good scientific reputation.", "A new scientist has joined your team.", [["addsci", 1]]), Result("This person seems highly caffinated, but could be a good engineer.", "A jittery engineer has joined your crew", [["addeng", 1], ["spec", "caffinate"]]), Result("BURN ALL THE PAPERS!", "...is something important on fire?", [["addfail", 1], ["addprog", -2], ["addflav", "Yes, yes something important was on fire"], ["spec", "charred"]])], 3)
#Result("Let's just focus on working today.", "after convincing your staff to work overtime..", [["overtime", 0.2]])], 2)
overtime = Prompt("overtime", ["Some particullarly hard working engineers", "are requesting the facility stay open later tonight so they can work overtime."], [Result("I suppose we can do that", "after your staff works overtime..", [["overtime", 0.3]]), Result("I don't think that's such a good idea.", "After convincing your staff not to work overtime...", [["addmoney", 2], ["addflav", "You recive an endorsement from the local health officials."]])], 2)
fire1 = Prompt("fire1", ["That one advisor from the government approches you:", "We have hired too many people and we are losing money", "somebody needs to get fired."], [Result("But we are getting so much done.", "After not firing anyone...", [["addfail", 2]]), Result("I'll leave it up to you.", "After that government advisor fires some people...", [["subpop", 3], ["addfail", -2]]),Result("Fire some of those engineers.", "After firing some engineers...", [["addeng", -2], ["addfail", -1]])], 6)
#fire2 = sci, mat, none
fire2 = Prompt("fire2", ["Your money is low, and you are loosing more.", "You need a way to stop your money"], [Result("Why don't we just hire more campaigners?", "After putting out an ad campaign:", [["addcam", 2], ["addmoney", -6], ["overtime", -.2]]), Result("How about we reduce costs?", "After using less expensive materials:", [["reduce", 1], [""]]), Result("Why not just reduce the work hours?", "You reduce the work hours.", [["addTime", -.2], ["addflav", "Your workers are more well rested at work."], ["addIfactor", -.1]])], 10)

#Money and materials
bakesale = Prompt("bakesale", ["One of your campaigners suggests:", "We should have a bake sale to raise money."], [Result("Sure, but only if I can have some too.", "After having a bakesale", [["addmoney", 2], ["addflav", "The bake sale premotes working in the areospace industy"], ["addpop", 1]]), Result("No, I hate baked goods", "After not having a bake sale..", [["addflav", "Some people were really looking forward to that bake sale."],["subpop", 1]])], 3)
adcampaign = Prompt("adcampaign", ["One of your mathmatitions suggests", "an add campaign to hire people."], [Result("Yeah, we need the staff", "After creating an amazing ad campaign...", [["addmoney", -4], ["addpop", 4]]), Result("No, we don't have enough money.", "After not creating an amazing ad campaign...", [["addflav", "Nothing changes"]])], 5)
materials = Prompt("materials", ["One of your scientists approaches you:", "We need to discuss our materials."], [Result("How about all carbon fiber?", "After using hi-tech materials:", [["addfail", -4], ["rocketspec", "hi-tech"], ["setMat", PMN]]), Result("Why not normal materials, like steel?", "After deciding to use standard materials:", [["addflav", "Engineers are attracted to the ease of their jobs."], ["addeng", 1], ["rocketspec", "steel"], ["setMat", PMI]]), Result("Lets think cheap. Duct-tape cheap.", "After deciding to use low-cost materials:", [["setMat", PMT], ["addfail", 20], ["addflav", "Some of your mathmatitions can't handle the absurdity of this project."], ["addmat", -2], ["rocketspec", "ductTape"]])], 99)
fuels = Prompt("fuels", ["An engineer approaches you:", "So, uh.. What should we use for fuel?"], [Result("Nuclear would be the most powerful.", "After deciding to place a nuclear reactor within the rocket:", [["addfail", 2], ["addmoney", -2], ["rocketspec", "fuelNuclear"], ["setpart", "Mnuclear"]]), Result("How about we design a rocket specific fuel?", "After deciding to design rocket fuel..", [["addfail", -5], ["addmon", -2], ["addIfactor", 0.1], ["rocketspec", "fuelRocket"], ["setpart", "Mnormal"]]), Result("Car fuel, we need to save money", "After deciding to use car fuel...", [["addflav", "Some people belive you aren't taking this job seriously"], ["subpop", 2],["addfail", -2], ["addmoney", -4], ["rocketspec", "fuelCar"], ["setpart", "Mcar"]])], 99)

#Bad ideas -- 
coffeeShipments = Prompt("coffeeShipments", ["A group of mathmatitions have been staying up all night:", "We need more shipments of caffinated beverages!"], [Result("Of course, coffee is a necissity.", "After ordering some caffine...", [["addmoney", -1], ["spec", "caffinate"], ["overtime", 0.1]]), Result("No, too much coffee is unhealthy", "After depriving your employees of caffine...", [["addfail", 5], ["overtime", -0.1], ["addflav", "The employees are quite tired."]])], 10)
coffee = Prompt("coffee", ["A few engineers approch you and ask:", "Can we install a coffee machine in the rocket?"], [Result("Sure, Why not?", "After installing a coffee machine on the rocket,", [["addmoney", -1], ["addprog", 2], ["addfail", 4], ["addeng", 1], ["spec", "caffinate"], ["rocketspec", "coffeeMachine"]]), Result("NO?", "After not installing a coffee machine...", [["addfail", -1]])], 1)			
toaster = Prompt("toaster", ["One of those hippies from science department asks:", "Hey, we're low on funds right now. I suggest we turn our chassis into a toaster."], [Result("Sure, we need to save money.", "After switching over your chassis:", [["setpart", "Ctoaster"], ["addfail", 50], ["addmat", -2], ["rocketspec", "ToasterChassis"]]), Result("We don't need to be THAT drastic..", "After reducing the size:", [["addfail", -1], ["addsci", 1]]), Result("No way.", "After denying the toaster plan:", [["addmat", 1], ["addpop", 1], ["setpart", "Cnormal"]])], 3)
hotel = Prompt("hotel", ["The CEO of a large hotel group has approched you", "and wishes install one of his hotels on the moon.", "He bribes you with quite a bit of money."], [Result("I guess so.", "The engineers begin to load materials to build the hotel on the moon.", [["multprog", .2], ["addfail", 10], ["addmoney", 20], ["addIfactor", 4], ["rocketspec", "hotel"], ["setpart", "Chotel"], ["addspec", "privateFund1"]]), Result("No.", "After focusing on building the rocket and not business deals:", [["addprog", 5], ["addpop", 1]])], 3)
silos = Prompt("silos", ["One very frugel lab assistant approches you:", "We don't have enough money to build the thrusters", "How about we use the silos from the sourounding farmland?"], [Result("What a wonderful idea!", "After refiting farm silos to work as thrusters...", [["addfail", 20], ["addsci", 1], ["addflav", "A hippy scientist joins your team"], ["rocketspec", "silos"], ["setpart", "Bsilo"]]), Result("Are you sane?", "After not taking the farmer's silos", [["addflav", "The farmers share some of their wages with you!"],["addmoney", 5]])], 99)
#mtndew
sodamachine = Prompt("sodamachine", ["A promising scientist asks if they can", "install a soda machine in the lab."], [Result("Sure, how much will it cost me?", "After installing a soda machine in the lab...", [["addmoney", -2], ["overtime", 0.2]]), Result("No, we don't have the money.", "After not installing a soda machine in the lab.", [["overtime", -0.1], ["addflav", "Your employees seem a bit slow today."]])], 10)
spaceSoda = Prompt("spaceSoda", ["A campainer approaches you:", "Can we put some coffee in the rocket?"], [Result("Of course, the extra sugar will help us do more research!", "After adding some soda to the rocket plans...", [["addmoney", -1], ["addfail", 3], ["addprog", 3], ["rocketspec", "soda"], ["spec", "caffinate"]]), Result("No, soda is unhealthy and will make the astronauts ill.", "After proritizing the health of your astronauts...", [["addfail", -1], ["addmat", 1], ["addflav", "A mathmatition joins due to reports of a healthy climate."]])], 10)

#interesting ideas
fsc = Prompt("fsc", ["Upon seeing how well the rocket is going,", "an advisor from the Futuristic Science Corp.", "wishes to partner with you."], [Result("Together we will do great things.", "After partnering with the FSC...", [["addflav", "The project has drasticly increased in size."], ["spec", "JoinedFSC"], ["addmoney", 20], ["addmult", 0.1]]), Result("I'm sorry, I would prefer to go alone.", "After making the mistake of not partnering with the FSC..", [["addflav", "You feel you have made a horrible mistake."]])], 99)
theProject = Prompt("theProject", ["The FSC has requested a transfer of some of your engineers", "to work on some kind of classified project."], [Result("Sure, as long as we benefit from this project.", "You transfer some of your engineers and scientists over...", [["addeng", -3], ["addsci", -3], ["spec", "theProject"]]), Result("No, this is too supsecious.", "After declining the FSC's offer...", [["addflav", "Nothing happends, or has it?"]])], 10)
ai = Prompt("Ai", ["The FSC has finally completeled the project", "They have created a super intelegent AI and wish to install it", "in the lab to help progress."], [Result("YES! This is exactly what we need!", "After installing the AI in the lab...", [["spec", "AI"], ["addflav", "The AI makes complex equations easier."], ["addIfactor", -0.5]]), Result("I'm worried about the consequences of this, also rogue AIs are scary.", "After declining the FSC's offer...", [["addflav", "A saddened scientist leaves"], ["addsci", -1], ["addflav", "The FSC no longer wishes to work with you"], ["removeSpec", "JoinedFSC"]])], 99)
pen = Prompt("pen", ["One of your trusted scientists exclaims:", "After doing some amazing science,", "I have discovered that it will be impossible", "to write with pen in space!", "We need to develop a space pen!"], [Result("Yes, the space pen will be a big success!", "After funding a space pen project...", [["addmoney", -3], ["spec", "spacePen"]]), Result("I'm surounded by idiots, JUST USE A PENCIL!", "After deciding to use pencils...", [["addflav", "Paper costs decrease."]])], 10)
birthday = Prompt("birthday", ["Today is the birthday of one of your employees,", "They want to organize a party."], [Result("Lets take some time off work in celebration.", "After partying in the lounge:", [["overtime", -.2], ["addmon", -.5], ["addflav", "People are drawn to the friendly workplace."], ["addpop", 2]]), Result("Celebrate after work. It shouldn't interfere with your job.", "After postponing the party:", [["addflav", "Your employees are slacking off."], ["addfail", 2]])], -1)

#MATERIALS AND FUELS MUST BE THE FIRST 2 QUESTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
possiblequestions = [materials, fuels, coffee, hire1, adcampaign, silos, pen, coffeeShipments, spaceSoda, hire2, overtime, spaceSoda, sodamachine]	

#Player object
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
		self.full = 100
		self.pop = 0
		self.days = 0
		self.specs = []
		self.rocketspecs = []
		self.impossiblilyFactor = 1
		self.baseTime = 1
		self.time = 1
		#previous
		self.preMon = mon
		self.preProg = prog
		self.preFail = fail
		#ship type stuff
		self.material = PMI
		self.booster = PBnormal
		self.main = PMnormal
		self.chassis = PCnormal
		#the images of the frame, and the compleated product
		self.frame = frameImg(PMI)
		self.ship = spaceshipimg(self)
		self.questionsAnswered = []
	def setpart(self, part):
		if part == "material":
			pass
		if part == "Bsilo":
			player.booster = PBsilo
		if part == "Bnorm":
			player.booster = PBnormal
		if part == "Mnuclear":
			player.main = PMnuclear
		if part == "Mnorm":
			player.main = PMnormal
		if part == "Mcar":
			player.main = PMcar
		if part == "Ctoaster":
			player.chassis = PCtoaster
		if part == "Cnormal":
			player.chassis = PCnormal
		if part == "Chotel":
			player.chassis = PChotel
		
		self.impossiblilyFactor = 1+self.booster.fail+self.main.fail+self.chassis.fail+self.material.fail
		self.cost = self.booster.cost + self.main.cost + self.chassis.cost + self.material.cost
		self.full = self.booster.perc + self.main.perc + self.chassis.perc + self.material.perc
		self.ship = spaceshipimg(player)
		self.frame = frameImg(player.material)
		prints("fail factor: "+str(self.impossiblilyFactor))
		prints("cost: "+str(self.cost))
		prints("full: "+str(self.full))

player = Player(18, 0, 100, 1, 2, 1, 0)

class Achive(object):
	def __init__(self, Id, name, desc, img):
		self.box = achiveBox
		self.id = Id
		self.name = font.render(name, True, BLACK)
		self.desc = wraptext(desc, 245, achiveFont) 
		self.img = getImg("achives/" + img)

		#if you are going to get the achive
		self.gotten = False
		self.timer = 0
		self.waittimer = 0
		self.length = len(self.desc) * 11 + 4
		self.cords = [0,(self.length + 50) * -1]
		self.yvel = 1
		self.divider = 1
		self.descbox = textbox([300, self.length], "", achiveFont)

		self.getd = False
	def update(self):
		if self.timer > 0:
			gScreen.blit(self.box, self.cords)
			gScreen.blit(self.name, [self.cords[0] + 50, self.cords[1] + 3])
			gScreen.blit(self.descbox, [self.cords[0], self.cords[1] + 50])	
			for i in range(len(self.desc)):
				gScreen.blit(achiveFont.render(self.desc[i], True, BLACK), [self.cords[0] + 4, self.cords[1] + 52 + i * 11])
				
			#gScreen.blit(self.desc, [self.cords[0] + 50, self.cords[1] + 19])
			gScreen.blit(self.img, [self.cords[0] +2, self.cords[1] + 2])
			#print self.yvel
			if self.timer < (self.length + 50): 
				self.yvel = -1
				
			if self.timer % 10 == 0:
				if self.timer > (self.length + 50):
					self.divider += 1
				elif self.timer <=(self.length + 50):
					self.divider -= 1
			if self.cords[1] >= 0:
				if self.waittimer >= 0:
					self.waittimer -= 1
					self.yvel = 0
					self.timer = (self.length + 50)
			
			if self.divider <= 0:
				self.divider = 1
			#print self.divider
			self.cords[1] += self.yvel / (self.divider / 5.00)
			self.timer -= 1
	def get(self):
		if not self.getd:
			self.timer = (self.length + 50) * 2 + 2
			self.waittimer = 100
			self.getd = True
	
		
#Achivements, take in a 4 strings, the first being the id of the achivement, the second being the name of the achivement, the third being the description of the achivement, and the fourth being the name of the achivement's image

#start all achivements with A to prevent overlapping variables.

Abegining = Achive("begining", "Day 1", "you win nothing, because it's impossible to get this achivement", "wip")
Atoast = Achive("toaster", "It could run on a toaster", "Succesfully launch a spaceship with a toaster chassis", "wip")
Anukes = Achive("nukes", "Fallout", "Blow up a nuke in midair, destroying the lab", "wip")
Aai = Achive("ai", "That cake is a lie", "Get some cake from a friendly AI", "cake")
Ahl = Achive("hl3", "Half life 3 confirmed", "Succesfully launch your third rocket using a radioactive power source", "wip")
Acaffine = Achive("caffine", "Caffinated Crew", "Build a ship with 5 caffinated additions", "coffee")

allAchives = [Atoast, Anukes, Abegining, Aai, Ahl, Acaffine]
			
#Takes in the list of possible questions, the player parameter, a list of requirement lists, and a question.
#If the question meets all the requirements, it is appeneded to possiblequestions
#Requirement lists take in a player parameter, an test opperator, and a integer or spec id depending on the opperator:
#Opperators: -----
#greater - equivelent to > sign, takes in a player parameter that is an integer and an integer
#lesser - equivelent to < sign, takes in a player parameter that is an integer and an integer
#spec - tests if the specified spec id is in the specified player parameter spec id list, takes in a player parameter spec id list and a spec id
#daysSince - Tests if it has been the specified integer number of days scince the specified question has been asked, takes in an integer and a Prompt
def addQuestion(possiblequestions, requirements, question):
	#Matches keeps track of the number of requirements passed
	matches = []
	for i in requirements:
	
		if i[1] == "greater":
			if i[0] > i[2] and not question in possiblequestions:
				matches.append(True)
				
		elif i[1] == "lesser":
			if i[0] < i[2] and not question in possiblequestions:
				matches.append(True)
			
		elif i[1] == "notSpec":
			if i[2] in i[0]:
				if question in possiblequestions:
					pass
			else:
				matches.append(True)
		elif i[1] == "spec":
			if i[2] in i[0]:
				matches.append(True)
		elif i[1] == "daysSince":
			if i[0] <= i[2].daysSince and i[2].daysSince >= 1:
				matches.append(True)	
	if len(matches) == len(requirements):
		if not question in possiblequestions:
			possiblequestions.append(question)
			print "Requirements met for", question.name
		else:
			print "Requirements met for "+ question.name + " BUT IT WAS ALREADY IN possiblequestions!"

	else:
		if question in possiblequestions:
			possiblequestions.remove(question)
			print "Requirements no longer met for " + question.name + ". Removing"
		else:
			print "Requirements not met for", question.name

funded = True	
mouse_down = False
done, running = False, True

day = 0
month = 1
year = 1957
while running:
	day += 1
	if day >= 30:
		month += 1
		day = 1
	if month >= 12:
		month = 0
		year += 1
	
	date = font.render(str(month) + "/" + str(day) + "/" + str(year), True, BLACK)
	player.days += 1
	player.pop = player.scientists + player.maths + player.campaigners + player.engineers
	player.time = player.baseTime
	for q in player.questionsAnswered:
		q.daysSince +=1
		if q.daysSince >= q.cooldown:
			if q not in possiblequestions:
				possiblequestions.append(q)
			q.daysSince = 0
	
	#Before choosing an answer
	#Stat logging
	print "[][][][][][][][][][][][][][][][][] Day " + str(player.days) + " [][][][][][][][][][][][][][][][][]"
	
	#see if a question can be added
	addQuestion(possiblequestions, [[player.money, "greater", 6], [player.rocketspecs, "notSpec", "hotel"]], hotel)
	addQuestion(possiblequestions, [[player.money, "lesser", 4]], toaster)
	addQuestion(possiblequestions, [[player.money, "lesser", 8]], bakesale)
	addQuestion(possiblequestions, [[player.pop, "greater", 10]], fire1)
	addQuestion(possiblequestions, [[player.money, "greater", 25], [player.specs, "spec", "JoinedFSC"]], fsc)
	addQuestion(possiblequestions, [[player.rocketspecs, "notSpec", "coffeeMachine"]], coffee)
	addQuestion(possiblequestions, [[player.rocketspecs, "notSpec", "silos"]], silos)
	addQuestion(possiblequestions, [[player.specs, "notSpec", "spacePen"]], pen)
	addQuestion(possiblequestions, [[player.rocketspecs, "notSpec", "soda"]], spaceSoda)
	addQuestion(possiblequestions, [[10, "daysSince", fsc], [player.scientists, "greater", 2], [player.engineers, "greater", 2], [player.specs, "spec", "JoinedFSC"]], theProject)
	addQuestion(possiblequestions, [[10, "daysSince", theProject], [player.specs, "spec", "theProject"]], ai)
		
	theQuestion = possiblequestions[random.randint(0, len(possiblequestions) - 1)]
	
	print "-------------------------------------------------------------------------------------------------"
	rand = "Possible questions:"
	for i in possiblequestions:
		rand = rand + "  " + i.name
	print rand
	print "-------------------------------------------------------------------------------------------------"
	if player.days == 1 or player.days == 2:
		theQuestion = possiblequestions[0]

	#Add dev birthdays, because good times
	if month == 12 and day == 1:
		theQuestion = birthday
	if day == 28 and month == 4:
		theQuestion = birthday
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
		
		gScreen.blit(player.frame, [80, 120])
		gScreen.blit(player.ship, [400, 120])

		for i in range(len(theQuestion.prompt)):
		
			gScreen.blit(font.render(theQuestion.prompt[i], True, BLACK), [200, 100 + i * 20])
			
		y = 0
		for i in theQuestion.results:
			displayresult = True
			
			
			if displayresult:
				gScreen.blit(responseButton.image, [50, 450 + y * 50])
		
				gScreen.blit(font.render(i.desc,True,BLACK), [60, 455 + y * 50])
				
				if mouse_down:
					if hitDetect(mouse_pos, mouse_pos, [50, 450 + y * 50], [650, 475 + y * 50]):
						pygame.mixer.Sound.play(select)
						mouse_down = False
						feedback = i.decide(player)
						print "Question:", theQuestion.name
						print "Answer:", i.desc
						possiblequestions.remove(theQuestion)
						if not theQuestion in player.questionsAnswered: 
							player.questionsAnswered.append(theQuestion)
						
						done = True
						break
				y+= 1
		
		gScreen.blit(date, [10,10])
		pygame.draw.rect(gScreen, YELLOW, [155 - 38, 60, 50, (player.money * -1) / 20])
		gScreen.blit(moneypic, [155 - 38, 10])
		
		pygame.draw.rect(gScreen, GREEN, [233 - 38, 60, 50, ((player.progress/player.full) * -100) / 2])
		gScreen.blit(progresspic, [233 - 38, 10])
		
		pygame.draw.rect(gScreen, RED, [311 - 38, 60, 50, (player.failChance * -1) / 2])
		gScreen.blit(failurepic, [311 - 38, 10])
		
		pygame.draw.rect(gScreen, BLUE, [388 - 38, 60, 50, (player.scientists * -1)])
		gScreen.blit(sciencepic, [388 - 38, 10])
		
		pygame.draw.rect(gScreen, GREY, [466 -38, 60, 50, (player.engineers * -1)])
		gScreen.blit(engiespic, [466 -38, 10])
		
		pygame.draw.rect(gScreen, PURPLE, [544 - 38, 60, 50, (player.maths * -1)])
		gScreen.blit(mathspic, [544 - 38, 10])
		
		pygame.draw.rect(gScreen, TEAL, [622 - 38, 60, 50, (player.campaigners * -1)])
		gScreen.blit(campainerspic, [622 - 38, 10])

		gScreen.blit(font.render(str(player.money)+"K",True,BLACK), [155 - 38, 60])
		gScreen.blit(font.render(str(round(player.progress/player.full*100, 2))+"%",True,BLACK), [233 - 38, 60])
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

			
		for achive in allAchives:
			achive.update()
		pygame.display.update()
		clock.tick(60)

	#after choosing an answer
	Abegining.get()
	if "AI" in player.specs:
		Aai.get()
	player.failChance -= round(player.time * math.sqrt(player.maths) / player.impossiblilyFactor, 2)
	if player.failChance < 1:
		player.failChance = 1
	player.progress += round(player.time * ((.2*player.scientists)+1)*player.engineers*0.4, 2)
	player.money += ((2 * player.campaigners) - (player.engineers + player.maths + player.scientists + player.cost*player.engineers))
	feedback1 = []
	feedback1.append("After a full day of work...")
	if player.campaigners > 0:
		feedback1.append("   Your campaigners raise "+str(2*player.campaigners)+"K")
	if funded:
		#6 is default reduced per turn with 1 sci & math, and 2 eng
		player.money += 8
		feedback1.append("   You gain 8K in government funding.")
	if "privateFund1" in player.specs:
		player.money += 4
		feedback1.append("   You gain 4K from private sectors.")
		
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
			if player.failChance >= 100:
				successChance = 0
			else:		
				successChance = (100 - player.failChance) * (player.progress / player.full)
			print "success Chance:", successChance
			launchChance = random.randint(0, 100)
			rand = 100 - launchChance
			if launchChance <= successChance:
				print "LAUNCH SUCCESSFUL!"
				if "ToasterChassis" in player.rocketspecs:
					Atoast.get()
				if "fuelNuclear" in player.rocketspecs and fails == 2:
					Ahl.get()
				pygame.mixer.Sound.play(launch)
				player.money += 50
			if launchChance > successChance and launchChance <= successChance + (rand * 1 / 3):
				print "LAUNCH Failure 3!"
				pygame.mixer.Sound.play(explosion)
				if "fuelNuclear" in player.rocketspecs:
					Anukes.get()
			if launchChance > successChance + (rand * 1 / 3) and launchChance <= successChance + (rand * 2 / 3):
				print "LAUNCH Failure 2!"
				pygame.mixer.Sound.play(explosion)
			if launchChance > successChance + (rand * 2 / 3):
				print "LAUNCH Failure 1!"
				pygame.mixer.Sound.play(explosion)
				

			player.rocketspecs = []
			player.fails += 1
			player.progress, player.cost, player.failChance = 0, 1, 100 - player.fails
			done = True
		if hitDetect(mouse_pos, mouse_pos, [10,580], [180, 630]) and mouse_down:
			done = True
			pygame.mixer.Sound.play(new_day)
		
		gScreen.blit(continuepic, [10, 580])
		gScreen.blit(launchpic, [10, 640])
		
		for achive in allAchives:
			achive.update()
		
		pygame.display.update()
		clock.tick(60)

