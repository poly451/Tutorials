import os, sys
import pygame
import constants
import pygame
import utils
from environment import Environment
from image_classes import SpecialEffects
# ----------------------------------------------------
#                        class Player
# ----------------------------------------------------

class Player(pygame.sprite.Sprite):
	def __init__(self, character_name):
		super().__init__()
		self.init_pygame()
		# ----
		self.character_name = character_name
		self.width = 45
		self.height = 63
		self.scale = 3
		self.colour = constants.BLACK
		self.up = True
		self.x, self.y = 1, 1
		self.keep_looping = True
		self.image_counter = 0
		# ----
		self.movement = "idle"
		self.direction = "front"
		self.collision_distance = 0.111111111111111111
		# ----
		self.image_list_walk_back = []
		self.image_list_walk_left = []
		self.image_list_walk_right = []
		self.image_list_walk_front = []
		# ----
		self.image_list_spell_back = []
		self.image_list_spell_left = []
		self.image_list_spell_right = []
		self.image_list_spell_front = []
		# ----
		self.image_list_slash_back = []
		self.image_list_slash_left = []
		self.image_list_slash_right = []
		self.image_list_slash_front = []
		# ----
		self.image_list_travel_back = []
		self.image_list_travel_left = []
		self.image_list_travel_right = []
		self.image_list_travel_front = []
		# ----
		self.image_list_idle_back = []
		self.image_list_idle_left = []
		self.image_list_idle_right = []
		self.image_list_idle_front = []
		# ----
		self.image_list_fall = []
		self.image_list_unconscious = []
		# ----
		self.image_list = []
		self.image = None
		self.rect = None

	def read_data(self):
		# self.sprite_sheet_image = pygame.image.load(constants.WALKSHEET_PATH).convert_alpha()
		self.image_list_walk_back = self.set_image_list_sheet("walk", "back")
		self.image_list_walk_left = self.set_image_list_sheet("walk", "left")
		self.image_list_walk_right = self.set_image_list_sheet("walk", "right")
		self.image_list_walk_front = self.set_image_list_sheet("walk", "front")
		# ----
		self.image_list_spell_back = self.set_image_list_sheet("spell", "back")
		self.image_list_spell_left = self.set_image_list_sheet("spell", "left")
		self.image_list_spell_right = self.set_image_list_sheet("spell", "right")
		self.image_list_spell_front = self.set_image_list_sheet("spell", "front")
		# ----
		self.image_list_slash_back = self.set_image_list_sheet("slash", "back")
		self.image_list_slash_left = self.set_image_list_sheet("slash", "left")
		self.image_list_slash_right = self.set_image_list_sheet("slash", "right")
		self.image_list_slash_front = self.set_image_list_sheet("slash", "front")
		# ----
		self.image_list_idle_back = self.set_image_list_sheet("idle", "back")
		self.image_list_idle_left = self.set_image_list_sheet("idle", "left")
		self.image_list_idle_right = self.set_image_list_sheet("idle", "right")
		self.image_list_idle_front = self.set_image_list_sheet("idle", "front")
		# ----
		self.image_list_fall = self.set_image_list_short("fall")
		self.image_list_unconscious = self.set_image_list_short("unconscious")
		# self.image_list_idle = self.set_image_list_short("idle")
		# ---- ----
		if self.movement == "walk":
			self.image_list = self.image_list_walk_front
		elif self.movement == "spell":
			self.image_list = self.image_list_spell_front
		elif self.movement == "slash":
			self.image_list = self.image_list_slash_front
		elif self.movement == "fall":
			self.image_list = self.image_list_fall
		elif self.movement == "unconscious":
			self.image_list = self.image_list_unconscious
		elif self.movement == "idle":
			self.image_list = self.image_list_idle_front
		else:
			raise ValueError("Error")
		# ----

	def set_image_list_short(self, animation_name):
		pygame.display.set_caption('FallSheet')
		path = os.path.join("data", "images", "characters", self.character_name, animation_name)
		if os.path.isdir(path) == False: raise ValueError("Error")
		filenames = os.listdir(path)
		if len(filenames) == 0:
			s = "path: {}".format(path)
			raise ValueError(s)
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
		return image_list

	# in class Player
	def set_image_list_sheet(self, movement, direction):
		path = os.path.join("data", "images", "characters", self.character_name, movement, direction)
		if os.path.isdir(path) == False: raise ValueError("Error")
		filenames = os.listdir(path)
		if filenames is None: raise ValueError("Error")
		if len(filenames) == 0:
			s = "path: {}".format(path)
			raise ValueError(s)
		image_list = []
		for filename in filenames:
			if filename == ".DS_Store": continue
			filepath = os.path.join(path, filename)
			# an_image = None
			try:
				an_image = pygame.image.load(filepath).convert_alpha()
			except Exception as e:
				s = "filepath: {}".format(filepath)
				t = "{}\n{}\n".format(e, s)
				raise ValueError(t)
			# ----
			an_image = pygame.transform.scale(an_image, (constants.TILESIZE, constants.TILESIZE))
			image_list.append(an_image)
		return image_list

	# in class Player
	def change_direction(self, direction):
		if not direction in constants.DIRECTION_VALUES: raise ValueError("Error")
		self.movement = "walk"
		self.direction = direction
		self.change_animation(self.movement, self.direction)

	# in class Player
	def change_movement(self, movement):
		if not movement in constants.MOVEMENT_VALUES:
			s = "I do not recognize this movement: {}".format(movement)
			raise ValueError(s)
		self.change_animation(movement, self.direction)

	# in class Player
	def change_animation(self, movement, direction):
		self.movement = movement
		self.direction = direction
		# ----
		if self.movement not in constants.MOVEMENT_VALUES: raise ValueError("Error")
		if self.direction not in constants.DIRECTION_VALUES: raise ValueError("Error")
		# ----
		if self.movement == "walk":
			if self.direction == "back":
				self.image_list = self.image_list_walk_back
			elif self.direction == "left":
				self.image_list = self.image_list_walk_left
			elif self.direction == "right":
				self.image_list = self.image_list_walk_right
			elif self.direction == "front":
				self.image_list = self.image_list_walk_front
			else:
				raise ValueError("Error")
		elif self.movement == "spell":
			if self.direction == "back":
				self.image_list = self.image_list_spell_back
			elif self.direction == "left":
				self.image_list = self.image_list_spell_left
			elif self.direction == "right":
				self.image_list = self.image_list_spell_right
			elif self.direction == "front":
				self.image_list = self.image_list_spell_front
			else:
				raise ValueError("Error")
		elif self.movement == "slash":
			if self.direction == "back":
				self.image_list = self.image_list_slash_back
			elif self.direction == "left":
				self.image_list = self.image_list_slash_left
			elif self.direction == "right":
				self.image_list = self.image_list_slash_right
			elif self.direction == "front":
				self.image_list = self.image_list_slash_front
			else:
				raise ValueError("Error")
		elif self.movement == "idle":
			if self.direction == "back":
				self.image_list = self.image_list_idle_back
			elif self.direction == "left":
				self.image_list = self.image_list_idle_left
			elif self.direction == "right":
				self.image_list = self.image_list_idle_right
			elif self.direction == "front":
				self.image_list = self.image_list_idle_front
			else:
				raise ValueError("Error")
		elif self.movement == "fall":
			if self.direction in ["back", "front", "right", "left"]:
				# self.image_list = self.set_image_list_fallsheet()
				self.image_list = self.image_list_fall
			else:
				s = "I don't recognize this direction: {}".format(self.direction)
				raise ValueError(s)
		else:
			s = "I don't recognize this kind of movement: {}".format(self.movement)
			raise ValueError(s)
		if self.image_list is None: raise ValueError("Error")
		if len(self.image_list) == 0: raise ValueError("Error")

	def init_pygame(self):
		pygame.init()
		self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
		pygame.display.set_caption('Spritesheets')
		self.clock = pygame.time.Clock()

	def update(self):
		pass

	# in class Player
	def update_classes(self, image_counter, environment):
		try:
			self.image = self.image_list[image_counter]
			self.rect = self.image.get_rect()
			if self.movement == "walk":
				if self.direction == "right":
					if image_counter == 0:
						temp_x = self.x + 1
						temp_y = self.y
						temp_x = round(temp_x)
						temp_y = round(temp_y)
						if environment.obstacles.collision(temp_x, temp_y) == True:
							self.movement = "idle"
							self.change_animation(self.movement, self.direction)
						else:
							self.x += self.collision_distance
					else:
						self.x += self.collision_distance
				elif self.direction == "left":
					if image_counter == 0:
						temp_x = self.x - 1
						temp_y = self.y
						temp_x = round(temp_x)
						temp_y = round(temp_y)
						if environment.obstacles.collision(temp_x, temp_y) == True:
							self.movement = "idle"
							self.change_animation(self.movement, self.direction)
						else:
							self.x -= self.collision_distance
					else:
						self.x -= self.collision_distance
				elif self.direction == "front":
					if image_counter == 0:
						temp_x = self.x
						temp_y = self.y + 1
						temp_x = round(temp_x)
						temp_y = round(temp_y)
						if environment.obstacles.collision(temp_x, temp_y) == True:
							self.movement = "idle"
							self.change_animation(self.movement, self.direction)
						else:
							self.y += self.collision_distance
					else:
						self.y += self.collision_distance
				elif self.direction == "back":
					if image_counter == 0:
						temp_x = self.x
						temp_y = self.y - 1
						temp_x = round(temp_x)
						temp_y = round(temp_y)
						if environment.obstacles.collision(temp_x, temp_y) == True:
							self.movement = "idle"
							self.change_animation(self.movement, self.direction)
						else:
							self.y -= self.collision_distance
					else:
						self.y -= self.collision_distance
				else:
					s = "I don't recgonize this: {}".format(self.direction)
					raise ValueError(s)
			# ----
			if self.x > 13 or self.y > 13:
				s = "self.x, self.y: {},{} --> The value seems suspiciously high!"
				s = s.format(self.x, self.y)
				raise ValueError(s)
			self.rect = self.rect.move(self.x * constants.TILESIZE, self.y * constants.TILESIZE)
		except Exception as e:
			t = "len(self.image_list) = {}".format(len(self.image_list))
			s = "{}\n{}\n".format(e, t)
			raise ValueError(s)
		# -------------------------------------------------------
		if image_counter + 1 == len(self.image_list):
			if self.movement == "fall":
				self.movement = "unconscious"
				self.image_list = self.image_list_unconscious
			elif self.movement == "spell":
				self.movement = "idle"
				self.change_animation(self.movement, self.direction)
			elif self.movement == "walk":
				self.movement = "idle"
				self.change_animation(self.movement, self.direction)
				self.x = round(self.x)
				self.y = round(self.y)
				print("self.x, self.y: {},{}".format(self.x, self.y))
			elif self.movement == "slash":
				self.movement = "idle"
				self.change_animation(self.movement, self.direction)

# ----------------------------------------------------
#                        class Game
# ----------------------------------------------------
class Game:
	def __init__(self, zone_name, map_name, character_name):
		self.zone_name = zone_name
		self.map_name = map_name
		self.character_name = character_name
		# ----
		self.init_pygame()
		# ----
		self.player = Player(self.character_name)
		self.environment = Environment(self.zone_name, self.map_name)
		self.special_effect = SpecialEffects("sparks_effect")
		self.x, self.y = 1, 1
		self.keep_looping = True
		self.image_counter = 0
		# ----

	def read_data(self):
		self.player.read_data()
		self.environment.read_data()
		self.special_effect.read_data(self.player.x, self.player.y)

	def init_pygame(self):
		pygame.init()
		self.all_sprites = pygame.sprite.Group()
		self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
		pygame.display.set_caption('Spritesheets')
		self.font = pygame.font.Font(None, 35)
		self.clock = pygame.time.Clock()

	# in class Game
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.keep_looping = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.keep_looping = False
				elif event.key == pygame.K_r:
					self.image_counter = 0
				elif event.key == pygame.K_i:
					self.image_counter = 0
					self.player.change_movement("idle")
				elif event.key == pygame.K_w:
					self.image_counter = 0
					self.player.change_movement("walk")
				elif event.key == pygame.K_s:
					self.image_counter = 0
					self.special_effect.show = True
					self.player.change_movement("spell")
				elif event.key == pygame.K_f:
					self.image_counter = 0
					self.player.change_movement("fall")
				elif event.key == pygame.K_l:
					self.image_counter = 0
					self.player.change_movement("slash")
				# ===============================================
				elif event.key == pygame.K_UP:
					self.image_counter = 0
					self.player.change_direction("back")
				elif event.key == pygame.K_RIGHT:
					self.image_counter = 0
					self.player.change_direction("right")
				elif event.key == pygame.K_LEFT:
					self.image_counter = 0
					self.player.change_direction("left")
				elif event.key == pygame.K_DOWN:
					self.image_counter = 0
					self.player.change_direction("front")
				# ---- ----

	def update(self):
		pass

	# in class Game
	def update_classes(self):
		self.all_sprites = self.environment.update_classes(self.all_sprites)
		self.player.update_classes(self.image_counter, self.environment)
		self.all_sprites.add(self.player)
		# ----
		if self.special_effect.update_classes(self.player.x, self.player.y) == True:
			self.all_sprites.add(self.special_effect)

	# in class Game
	def draw(self):
		self.screen.fill(constants.BG_COLOR)
		self.update_classes()
		# ----
		self.all_sprites.update()
		self.all_sprites.draw(self.screen)
		# ----
		# ----
		mylist = []
		mylist.append("Currently:")
		mylist.append(self.player.movement)
		mylist.append(" ")
		mylist.append("Slash --> l")
		mylist.append("Spell --> s")
		mylist.append("Walk --> w")
		mylist.append("Fall --> f")
		utils.talk_dialog(self.screen, mylist, self.font, width_offset=1020,
						  height_offset=10, line_length=60,
						  color=constants.BLACK)
		# ----
		pygame.display.flip()
		# ---- ----
		self.image_counter += 1
		if self.image_counter >= len(self.player.image_list):
			self.image_counter = 0

	def goodbye(self):
		pygame.quit()
		sys.exit()

	def main(self):
		while self.keep_looping == True:
			self.clock.tick(10)
			self.handle_events()
			self.update()
			self.draw()
		self.goodbye()

# ***************************************

if __name__ == "__main__":
	character_name = "baldric"
	zone_name = "testing"
	map_name = "map01"
	mygame = Game(zone_name, map_name, character_name)
	mygame.read_data()
	mygame.main()
