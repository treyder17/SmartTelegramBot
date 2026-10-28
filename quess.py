import random

bot = random.randint(1,10)

while True:
   player = int(input("guess my number:"))
   if bot == player:
       print("Win!")
       break
   else:
       print("Try again")