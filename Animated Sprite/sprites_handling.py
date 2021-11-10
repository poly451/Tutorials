# https://github.com/russs123/pygame_tutorials/tree/main/sprite_tutorial
import os, sys
from tutorial_06 import Game

# *************************************************************

if __name__ == "__main__":
	# please_draw = "draw_fall"
	# ----
	# please_draw = "draw_walksheet_back"
	# please_draw = "draw_walksheet_left"
	please_draw = "draw_walksheet_front"
	# please_draw = "draw_walksheet_right"
	# ----
	# please_draw = "draw_slashsheet_back"
	# please_draw = "draw_slashsheet_left"
	# please_draw = "draw_slashsheet_front"
	# please_draw = "draw_slashsheet_right"
	# ----
	# please_draw = "draw_spellsheet_back"
	# please_draw = "draw_spellsheet_left"
	# please_draw = "draw_spellsheet_front"
	# please_draw = "draw_spellsheet_right"
	# ----
	# move = True
	filepath = ""
	row_kind = ""
	row_kinds = ["back", "left", "right", "front"]
	number_of_frames_in_row = -1
	if please_draw == "draw_fall":
		filepath = os.path.join("data", "images", "baldric", "baldric_fallsheet.png")
		# filepath = os.path.join("data", "images", "baldric", "baldricfallsheet_copy02.png")
		mygame = Game(filepath=filepath)
		mygame.read_data()
		# mygame.set_image_list_walksheet("back", 6)
		# mygame.image_list = mygame.image_list_fall
	# ----------------------------------------------------
	elif please_draw == "draw_walksheet_back":
		filepath = os.path.join("data", "images", "baldric", "baldric_walksheet.png")
		mygame = Game(filepath=filepath)
		mygame.set_image_list_walksheet("back", 9)
	elif please_draw == "draw_walksheet_left":
		filepath = os.path.join("data", "images", "baldric", "baldric_walksheet.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_walksheet("left", 9)
	elif please_draw == "draw_walksheet_front":
		filepath = os.path.join("data", "images", "baldric", "baldric_walksheet.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_walksheet("front", 9)
	elif please_draw == "draw_walksheet_right":
		filepath = os.path.join("data", "images", "baldric", "baldric_walksheet.png")
		# filepath = os.path.join("data", "images", "baldric", "baldric_walksheet06.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_walksheet("right", 9)
	# ----------------------------------------------------
	elif please_draw == "draw_spellsheet_back":
		filepath = os.path.join("data", "images", "baldric", "baldric_SpellSheet02.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_spellsheet("back", 7)
	elif please_draw == "draw_spellsheet_left":
		filepath = os.path.join("data", "images", "baldric", "baldric_SpellSheet02.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_spellsheet("left", 7)
	elif please_draw == "draw_spellsheet_front":
		filepath = os.path.join("data", "images", "baldric", "baldric_SpellSheet02.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_spellsheet("front", 7)
	elif please_draw == "draw_spellsheet_right":
		filepath = os.path.join("data", "images", "baldric", "baldric_SpellSheet02.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_spellsheet("right", 7)
	# ----------------------------------------------------
	elif please_draw == "draw_slashsheet_back":
		filepath = os.path.join("data", "images", "baldric", "baldric_SlashSheet.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_slashsheet("back", 6)
	elif please_draw == "draw_slashsheet_left":
		filepath = os.path.join("data", "images", "baldric", "baldric_SlashSheet.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_slashsheet("left", 6)
	elif please_draw == "draw_slashsheet_front":
		filepath = os.path.join("data", "images", "baldric", "baldric_SlashSheet.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_slashsheet("front", 6)
	elif please_draw == "draw_slashsheet_right":
		filepath = os.path.join("data", "images", "baldric", "baldric_SlashSheet.png")
		mygame = Game(move=False, filepath=filepath)
		mygame.set_image_list_slashsheet("right", 6)
	# elif please_draw == "draw_spellsheet_front":
	# 	raise NotImplemented
	# 	row_kind = "right"
	# 	number_of_frames_in_row = 9
	# 	print("In: draw_walksheet_right")
	# 	filepath = os.path.join("data", "images", "baldric", "baldric_SpellSheet02_trimmed.png")
	# 	mygame = Game(move=False, filepath=filepath)
	# 	mygame.set_image_list_spellsheet("spell_right", number_of_frames_in_row)
	# 	mygame.main()
	# 	sys.exit()
	else:
		s = "I don't recognize this: {}".format(please_draw)
		raise ValueError(s)
		# ----
	mygame.main()

