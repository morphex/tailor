#!/usr/bin/python3

# Needs pip3 install termcolor

from termcolor import colored

print(colored('Hello', 'red'), colored('world!', 'green'))
print(colored("This is a test", 'green'), "of the termcolor module")
print("Question: ", colored("Why did the monkey cross the road", "blue"),
      colored("??", "green"))
print("Answer: ", colored("I'm not sure.", "red"))
print("Answer: ", colored("I guess it just had to!!", "yellow"))
