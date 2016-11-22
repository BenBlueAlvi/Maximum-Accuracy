import random

#(self, name, prompt, results, cooldown):
while True:
	thePrompt = ""
	name = raw_input("name of the prompt?   ")
	if name == "":
		break
	question = raw_input("Question?   ")
	results = []
	while True:
		result_desc = raw_input("response:   ")
		if result_desc == "":
			break
		result_result = raw_input("result:   ")
		result_doings = []
		while True:
			doing_name = raw_input("Name of the doing?   ")
			if doing_name == "":
				break
			doing_amount = raw_input("Amount?   ")
			result_doings.append([doing_name, int(doing_amount)])
			
		result_cooldown = raw_input("Cooldown?")
		results.append("Result("+ result_desc + "," + result_result + "," + str(result_doings) +")")
		
	thePrompt = "Prompt("+ name + "," + question + "," + str(results) + ")"
	print thePrompt
	
	
	
	
	
	prompts = open("prompts.txt", 'w')
	prompts.write(thePrompt + "\n")
	prompts.close()