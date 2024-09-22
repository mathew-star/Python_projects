from termcolor import colored
import pyfiglet

result = pyfiglet.figlet_format("Password", font="slant")
print(colored(result, 'green'))
