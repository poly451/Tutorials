import pygame
import os
import constants
# -------------------------------------------------------------
#                        class SpecialEffects
# -------------------------------------------------------------

class SpecialEffects(pygame.sprite.Sprite):
	def __init__(self, animation_name):
		super().__init__()
		self.animation_name = animation_name
		self.image_list = []
		self.empty = None
		self.image_counter = 0
		self.show = False
		self.x, self.y = 0, 0

	def read_data(self, x, y):
		self.image_list = self.set_image_list_short()
		filepath = os.path.join("data", "images", "empty.png")
		self.empty = pygame.image.load(filepath).convert_alpha()
		self.x, self.y = x, y

	def set_image_list_short(self):
		# pygame.display.set_caption('FallSheet')
		path = os.path.join("data", "images", "special_effects", self.animation_name)
		if os.path.isdir(path) == False: raise ValueError("Error")
		filenames = os.listdir(path)
		if len(filenames) == 0:
			s = "path: {}".format(path)
			raise ValueError(s)
		# ----
		image_list = []
		for filename in filenames:
			if filename == ".DS_Store": continue
			filepath = os.path.join(path, filename)
			try:
				an_image = pygame.image.load(filepath).convert_alpha()
			except Exception as e:
				s = "filepath: {}".format(filepath)
				t = "{}\n{}\n".format(e, s)
				raise ValueError(t)
			an_image = pygame.transform.scale(an_image, (constants.TILESIZE, constants.TILESIZE))
			image_list.append(an_image)
		if len(image_list) == 0:
			raise ValueError("Error")
		return image_list

	# in class SpecialEffects
	def update_classes(self, x, y):
		if self.show == False: return False
		# ----
		if self.image_counter == len(self.image_list):
			self.image_counter = 0
			self.show = False
		if self.show == False:
			self.image = self.empty
		elif self.show == True:
			self.image = self.image_list[self.image_counter]
		else:
			raise ValueError("Error")
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(x * constants.TILESIZE, y * constants.TILESIZE)
		self.image_counter += 1
		return True

