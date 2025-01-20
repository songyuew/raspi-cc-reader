from cc_parser import reader
from update_screen import updateScreen


updateScreen("Swipe the card ==>","","","")
while(True):
    card = reader()
    if card["status"] == "OK":
        updateScreen(card["pan"],card["exp"],card["ch"],"")
    elif card["status"] == "exit":
        updateScreen("Terminated","","","")
        break
    else:
        updateScreen(card["status"],"Swipe the card ==>","","")



