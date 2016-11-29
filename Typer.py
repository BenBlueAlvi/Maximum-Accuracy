import io
import time

thetext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

#change to force indents on multi-line strings

#maximum length before indent
fullline = 100

def wraptext(text):
    Denting = True
    global fullline
    count = fullline
    outtext = ""
    while Denting:
        if len(text) > fullline:
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
                            outtext = outtext+thistext[:len(thistext)-(i+1)]+"\n"
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
    
print wraptext(thetext)
raw_input(":")