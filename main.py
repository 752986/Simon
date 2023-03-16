import math
import random
from enum import Enum
import pygame
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.color import Color
from pygame.math import Vector2


CENTER = Vector2(512, 512)
SPACING = 32


def dist(p1: Vector2, p2: Vector2) -> float:
	return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)	


class SimonColor(Enum):
	GREEN = 0
	BLUE = 1
	YELLOW = 2
	RED = 3


class GameObject:
	bounds: Rect = Rect(0, 0, 0, 0)

	def update(self, delta: float):
		pass
	
	def draw(self, surface: Surface):
		pass


class Button(GameObject):
	highlight: bool

	def __init__(self, image_path: str, simon_color: SimonColor, color: Color, highlight_color: Color):
		self.base_image = pygame.image.load(image_path).convert_alpha()
		self.rect = self.base_image.get_rect()
		self.simon_color = simon_color
		self.color = color
		self.highlight_color = highlight_color
		self.highlight = False

	def pressed(self):
		pass

	def draw(self, surface: Surface):
		image = self.base_image.copy()
		image.fill(self.highlight_color if self.highlight else self.color, None, pygame.BLEND_MULT)
		surface.blit(image, self.rect)


def flash(button: Button, surface: Surface):
	# *really* messy way to do this, maybe find a better way
	button.highlight = True
	button.draw(surface)
	pygame.display.flip()
	pygame.time.wait(500)
	button.highlight = False
	button.draw(surface)
	pygame.display.flip()
	pygame.time.wait(100)


def main():
	screen = pygame.display.set_mode((1024, 1024))

	clock = pygame.time.Clock()

	# setup:
	green = Button("res/green.png", SimonColor.GREEN, Color("#85ad58"), Color("#acd77e"))
	blue = Button("res/blue.png", SimonColor.BLUE, Color("#46b0b5"), Color("#89e7eb"))
	yellow = Button("res/yellow.png", SimonColor.YELLOW, Color("#cca737"), Color("#f9e19e"))
	red = Button("res/red.png", SimonColor.RED, Color("#db6962"), Color("#f3b5ae"))
	green.rect.bottomright = (int(CENTER.x) - SPACING, int(CENTER.y) - SPACING)
	blue.rect.bottomleft = (int(CENTER.x) + SPACING, int(CENTER.y) - SPACING)
	yellow.rect.topright = (int(CENTER.x) - SPACING, int(CENTER.y) + SPACING)
	red.rect.topleft = (int(CENTER.x) + SPACING, int(CENTER.y) + SPACING)

	game_objects: list[GameObject] = [green, blue, yellow, red]

	sequence: list[SimonColor] = [random.choice(list(SimonColor))]
	index = 0


	# initial draw:
	screen.fill(Color("#2e2e2e"))
	for obj in game_objects:
		obj.draw(screen)

	for button in [green, blue, yellow, red]:
		if button.simon_color == sequence[0]:
			flash(button, screen)


	running = True
	while running:
		# events
		justClicked = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				justClicked = True


		# setup
		delta = clock.tick() / 1000

		screen.fill(Color("#2e2e2e"))


		# logic
		for obj in game_objects:
			obj.update(delta)
			obj.draw(screen)


		# TODO: fix cursor setting
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


		if justClicked:
			center_dist = dist(CENTER, Vector2(pygame.mouse.get_pos()))
			if center_dist > 270 and center_dist < 415:
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
				pressed: SimonColor = SimonColor.GREEN # throwaway value so the type checker stops complaining

				for button in [green, blue, yellow, red]:
					if button.rect.collidepoint(Vector2(pygame.mouse.get_pos())):
						button.pressed()
						pressed = button.simon_color
						break
				
				# center_difference = Vector2(pygame.mouse.get_pos()) - CENTER
				# if center_difference.x < 0 and center_difference.y < 0: # top left
				# 	green.pressed()
				# 	pressed = SimonColor.GREEN
				# elif center_difference.x > 0 and center_difference.y < 0: # top right
				# 	blue.pressed()
				# 	pressed = SimonColor.BLUE
				# elif center_difference.x < 0 and center_difference.y > 0: # bottom left
				# 	yellow.pressed()
				# 	pressed = SimonColor.YELLOW
				# elif center_difference.x > 0 and center_difference.y > 0: # bottom right
				# 	red.pressed()
				# 	pressed = SimonColor.RED

				if sequence[index] == pressed:
					index += 1
				else:
					print("YOU DIED!!!!!!")
					print(f"score: {len(sequence)}")
					running = False
				if index >= len(sequence): # start a new round
					sequence.append(random.choice(list(SimonColor)))
					index = 0
					for color in sequence:
						for button in [green, blue, yellow, red]:
							if button.simon_color == color:
								flash(button, screen)

		pygame.display.flip()

if __name__ == "__main__":
	main()