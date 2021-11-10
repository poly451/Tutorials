import pygame
import utils
import os
# -------------------------------------------------------------
#                        class SpriteSheet_Fall
# -------------------------------------------------------------

class SpriteSheet_Fall:
	def __init__(self, image, images_in_strip):
		self.sheet = image
		self.images_in_strip = images_in_strip

	def get_an_image(self, number_of_rows, column_number, width, height, scale):
		# print("frame: {}".format(frame))
		# print("width: {}".format(width))
		# print("height: {}".format(height))
		# print("scale: {}".format(scale))
		# ---- ----
		width += 18
		# ----
		x_start = -5
		x_increment = -64
		y_start = -15
		y_increment = -63
		# ----
		x = x_start
		y = y_start + (y_increment * (column_number - 1))
		xy = []
		xy.append((x, y))
		# ----
		x = x_start
		for i in range(number_of_rows-1):
			x_old = x
			x = x_old + x_increment
			elem = (x, y)
			# print("x:", x)
			xy.append(elem)
		# ----
		image_list = []
		for x, y in xy:
			# an_image = pygame.image.load(filepath).convert_alpha()
			# an_image = pygame.transform.scale(an_image, (constants.TILESIZE, constants.TILESIZE))
			# ----
			image = pygame.Surface((width, height)).convert_alpha()
			image.blit(self.sheet, (x, y))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# ----
			# filename = "player_{}.png".format(utils.get_unique_number())
			# filepath = os.path.join("data", filename)
			# pygame.image.save(image, filepath)
			# ----
			image_list.append(image)
		return image_list

# -------------------------------------------------------------
#                        class SpriteSheet_Cycle
# -------------------------------------------------------------

class SpriteSheet_Cycle:
	def __init__(self, image, images_in_strip):
		self.sheet = image

	def get_images_walksheet(self, number_of_rows, column_number, width, height, scale):
		width += 18
		# ----
		x_start = -5
		x_increment = -64
		y_start = -15
		y_increment = -63
		# ----
		x = x_start
		y = y_start + (y_increment * (column_number - 1))
		xy = []
		xy.append((x, y))
		# ----
		x = x_start
		for i in range(number_of_rows-1):
			x_old = x
			x = x_old + (x_increment)
			elem = (x, y)
			# print("x:", x)
			xy.append(elem)
		# print(xy)
		image_list = []
		for x, y in xy:
			image = pygame.Surface((width, height)).convert_alpha()
			image.blit(self.sheet, (x, y))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			image_list.append(image)
		return image_list

	def get_images_slashsheet(self, number_of_rows, column_number, width, height, scale):
		# print("get_images_slashsheet in sprites_myclasses. number_of_rows: {}".format(number_of_rows))
		# ----
		width += 18
		# ----
		x_start = -5
		# x_start = 550
		x_increment = -64
		y_start = -15
		y_increment = -63
		# ----
		x = x_start
		y = y_start + (y_increment * (column_number - 1))
		xy = []
		xy.append((x, y))
		# ----
		x = x_start
		for i in range(number_of_rows-1):
			x_old = x
			x = x_old + (x_increment)
			elem = (x, y)
			# print("x:", x)
			xy.append(elem)
		# print(xy)
		image_list = []
		for x, y in xy:
			image = pygame.Surface((width, height)).convert_alpha()
			image.blit(self.sheet, (x, y))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			image_list.append(image)
		return image_list

	def get_images_spellsheet(self, number_of_rows, column_number, width, height, scale):
		width += 18
		# ----
		x_start = -5
		x_increment = -64
		y_start = -15
		y_increment = -63
		# ----
		x = x_start
		y = y_start + (y_increment * (column_number - 1))
		xy = []
		xy.append((x, y))
		# ----
		x = x_start
		for i in range(number_of_rows-1):
			x_old = x
			x = x_old + (x_increment)
			elem = (x, y)
			# print("x:", x)
			xy.append(elem)
		# print(xy)
		image_list = []
		for x, y in xy:
			image = pygame.Surface((width, height)).convert_alpha()
			image.blit(self.sheet, (x, y))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			image_list.append(image)
		return image_list

# # -------------------------------------------------------------
# #                        class WalkCycle_Back_OLD
# # -------------------------------------------------------------
#
# class SpriteSheet_WalkCycle_Back_OLD:
# 	def __init__(self, image, images_in_strip):
# 		self.sheet = image
# 		self.images_in_strip = images_in_strip
#
# 	def get_an_image(self, frame, width, height, scale, colour):
# 		# ---- ----
# 		image = pygame.Surface((width, height)).convert_alpha()
# 		# ----
# 		myinc = -64
# 		fx1 = 0
# 		fy1 = 0
# 		fx2 = (fx1 + myinc)
# 		fy2 = 0
# 		fx3 = fx2 + myinc
# 		fy3 = 0
# 		fx4 = fx3 + myinc
# 		fy4 = 0
# 		fx5 = fx4 + myinc
# 		fy5 = 0
# 		fx6 = fx5 + myinc
# 		fy6 = 0
# 		fx7 = fx6 + myinc
# 		fy7 = 0
# 		fx8 = fx7 + myinc
# 		fy8 = 0
# 		fx9 = fx8 + myinc
# 		fy9 = 0
# 		# ----
#
# 		if frame == 0:
# 			image.blit(self.sheet, (fx1, fy1))
# 			image = pygame.transform.scale(image, (width * scale, height * scale))
# 			# print(fx1, fy1)
# 		elif frame == 1:
# 			image.blit(self.sheet, (fx2, fy2))
# 			image = pygame.transform.scale(image, (width * scale, height * scale))
# 			# print(fx2, fy2)
# 		elif frame == 2:
# 			image.blit(self.sheet, (fx3, fy3))
# 			image = pygame.transform.scale(image, (width * scale, height * scale))
# 			# print(fx3, fy3)
# 		elif frame == 3:
# 			image.blit(self.sheet, (fx4, fy4))
# 			image = pygame.transform.scale(image, (width * scale, height * scale))
# 			# print(fx4, fy4)
# 		elif frame == 4:
# 			image.blit(self.sheet, (fx5, fy5))
# 			image = pygame.transform.scale(image, (width * scale, height * scale))
# 			# print(fx5, fy5)
# 		elif frame == 5:
# 			image.blit(self.sheet, (fx6, fy6))
# 			image = pygame.transform.scale(image, (width * scale, height * scale))
# 			# print(fx6, fy6)
# 		elif frame == 6:
# 			image.blit(self.sheet, (fx7, fy7))
# 			image = pygame.transform.scale(image, (width * scale, height * scale))
# 			# print(fx7, fy7)
# 		elif frame == 7:
# 			image.blit(self.sheet, (fx8, fy8))
# 			image = pygame.transform.scale(image, (width * scale, height * scale))
# 			# print(fx8, fy8)
# 		elif frame == 8:
# 			image.blit(self.sheet, (fx9, fy9))
# 			image = pygame.transform.scale(image, (width * scale, height * scale))
# 			# print(fx9, fy9)
# 		return image

# -------------------------------------------------------------
#                        class SpriteSheet_left
# -------------------------------------------------------------

class SpriteSheet_WalkCycle_Left:
	def __init__(self, image, images_in_strip):
		self.sheet = image
		self.images_in_strip = images_in_strip

	def get_an_image(self, frame, width, height, scale, colour):
		# ---- ----
		image = pygame.Surface((width, height)).convert_alpha()
		# ----
		myinc = -64
		inc_y = -64
		fx1 = 0
		fy1 = inc_y
		fx2 = (fx1 + myinc)
		fy2 = inc_y
		fx3 = fx2 + myinc
		fy3 = inc_y
		fx4 = fx3 + myinc
		fy4 = inc_y
		fx5 = fx4 + myinc
		fy5 = inc_y
		fx6 = fx5 + myinc
		fy6 = inc_y
		fx7 = fx6 + myinc
		fy7 = inc_y
		fx8 = fx7 + myinc
		fy8 = inc_y
		fx9 = fx8 + myinc
		fy9 = inc_y
		# ----
		if frame == 0:
			image.blit(self.sheet, (fx1, fy1))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# print(fx1, fy1)
		elif frame == 1:
			image.blit(self.sheet, (fx2, fy2))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# print(fx2, fy2)
		elif frame == 2:
			image.blit(self.sheet, (fx3, fy3))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# print(fx3, fy3)
		elif frame == 3:
			image.blit(self.sheet, (fx4, fy4))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# print(fx4, fy4)
		elif frame == 4:
			image.blit(self.sheet, (fx5, fy5))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# print(fx5, fy5)
		elif frame == 5:
			image.blit(self.sheet, (fx6, fy6))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# print(fx6, fy6)
		elif frame == 6:
			image.blit(self.sheet, (fx7, fy7))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# print(fx7, fy7)
		elif frame == 7:
			image.blit(self.sheet, (fx8, fy8))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# print(fx8, fy8)
		elif frame == 8:
			image.blit(self.sheet, (fx9, fy9))
			image = pygame.transform.scale(image, (width * scale, height * scale))
			# print(fx9, fy9)
		return image

# -------------------------------------------------------------
#                        class SpriteSheet_Front
# -------------------------------------------------------------

class SpriteSheet_WalkCycle_Front:
	def __init__(self, image, images_in_strip):
		self.sheet = image
		self.images_in_strip = images_in_strip

	def get_an_image(self, frame, width, height, scale, colour):
		# print("frame: {}".format(frame))
		# print("width: {}".format(width))
		# print("height: {}".format(height))
		# print("scale: {}".format(scale))
		# ---- ----
		image = pygame.Surface((width, height)).convert_alpha()
		# ----
		myinc = -64
		inc_y = -64 * 2
		fx1 = 0
		fy1 = inc_y
		fx2 = (fx1 + myinc)
		fy2 = inc_y
		fx3 = fx2 + myinc
		fy3 = inc_y
		fx4 = fx3 + myinc
		fy4 = inc_y
		fx5 = fx4 + myinc
		fy5 = inc_y
		fx6 = fx5 + myinc
		fy6 = inc_y
		fx7 = fx6 + myinc
		fy7 = inc_y
		fx8 = fx7 + myinc
		fy8 = inc_y
		fx9 = fx8 + myinc
		fy9 = inc_y
		# ----
		if frame == 0:
			image.blit(self.sheet, (fx1, fy1))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 1:
			image.blit(self.sheet, (fx2, fy2))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 2:
			image.blit(self.sheet, (fx3, fy3))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 3:
			image.blit(self.sheet, (fx4, fy4))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 4:
			image.blit(self.sheet, (fx5, fy5))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 5:
			image.blit(self.sheet, (fx6, fy6))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 6:
			image.blit(self.sheet, (fx7, fy7))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 7:
			image.blit(self.sheet, (fx8, fy8))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 8:
			image.blit(self.sheet, (fx9, fy9))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		return image

# -------------------------------------------------------------
#                        class SpriteSheet_Right
# -------------------------------------------------------------

class SpriteSheet_WalkCycle_Right:
	def __init__(self, image, images_in_strip):
		self.sheet = image
		self.images_in_strip = images_in_strip

	def get_an_image(self, frame, width, height, scale, colour):
		# print("frame: {}".format(frame))
		# print("width: {}".format(width))
		# print("height: {}".format(height))
		# print("scale: {}".format(scale))
		# ---- ----
		image = pygame.Surface((width, height)).convert_alpha()
		# ----
		myinc = -64
		inc_y = -64 * 3
		fx1 = 0
		fy1 = inc_y
		fx2 = (fx1 + myinc)
		fy2 = inc_y
		fx3 = fx2 + myinc
		fy3 = inc_y
		fx4 = fx3 + myinc
		fy4 = inc_y
		fx5 = fx4 + myinc
		fy5 = inc_y
		fx6 = fx5 + myinc
		fy6 = inc_y
		fx7 = fx6 + myinc
		fy7 = inc_y
		fx8 = fx7 + myinc
		fy8 = inc_y
		fx9 = fx8 + myinc
		fy9 = inc_y
		# ----
		if frame == 0:
			image.blit(self.sheet, (fx1, fy1))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 1:
			image.blit(self.sheet, (fx2, fy2))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 2:
			image.blit(self.sheet, (fx3, fy3))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 3:
			image.blit(self.sheet, (fx4, fy4))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 4:
			image.blit(self.sheet, (fx5, fy5))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 5:
			image.blit(self.sheet, (fx6, fy6))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 6:
			image.blit(self.sheet, (fx7, fy7))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 7:
			image.blit(self.sheet, (fx8, fy8))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 8:
			image.blit(self.sheet, (fx9, fy9))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		return image

# -------------------------------------------------------------
#                        class SlashSheet
# -------------------------------------------------------------

class SpriteSheet_WalkCycle_Right_OLD:
	def __init__(self, image, images_in_strip):
		self.sheet = image
		self.images_in_strip = images_in_strip

	def get_an_image(self, frame, width, height, scale, colour):
		# print("frame: {}".format(frame))
		# print("width: {}".format(width))
		# print("height: {}".format(height))
		# print("scale: {}".format(scale))
		# ---- ----
		image = pygame.Surface((width, height)).convert_alpha()
		# ----
		myinc = -64
		inc_y = -64 * 3
		fx1 = 0
		fy1 = inc_y
		fx2 = (fx1 + myinc)
		fy2 = inc_y
		fx3 = fx2 + myinc
		fy3 = inc_y
		fx4 = fx3 + myinc
		fy4 = inc_y
		fx5 = fx4 + myinc
		fy5 = inc_y
		fx6 = fx5 + myinc
		fy6 = inc_y
		fx7 = fx6 + myinc
		fy7 = inc_y
		fx8 = fx7 + myinc
		fy8 = inc_y
		fx9 = fx8 + myinc
		fy9 = inc_y
		# ----
		if frame == 0:
			image.blit(self.sheet, (fx1, fy1))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 1:
			image.blit(self.sheet, (fx2, fy2))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 2:
			image.blit(self.sheet, (fx3, fy3))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 3:
			image.blit(self.sheet, (fx4, fy4))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 4:
			image.blit(self.sheet, (fx5, fy5))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 5:
			image.blit(self.sheet, (fx6, fy6))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 6:
			image.blit(self.sheet, (fx7, fy7))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 7:
			image.blit(self.sheet, (fx8, fy8))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		elif frame == 8:
			image.blit(self.sheet, (fx9, fy9))
			image = pygame.transform.scale(image, (width * scale, height * scale))
		return image
