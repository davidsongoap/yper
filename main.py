import pygame
from sys import exit
from palette import Colors 

pygame.init()

# window settings
background_colour = Colors.DARK_BLUE1
width, height = (910, 614)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Yper')
current_font = 'FiraCode-Medium.ttf'

def show_text(string, x=width//2, y=height//2, color=Colors.GREEN, size=50):
	font = pygame.font.SysFont(current_font, size) 
	text = font.render(string, True,color) 
	textRect = text.get_rect()  
	textRect.center = x,y
	screen.blit(text, textRect)

def quit_game():
	pygame.quit()
	exit()

def process_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit_game()
		if event.type == pygame.K_ESCAPE:
			quit_game()

def build_screen():
	screen.fill(background_colour)
	show_text("YPER",size=200)
	pygame.display.flip()

if __name__ == "__main__":
	while 1:
		process_events()
		build_screen()

quit_game()
