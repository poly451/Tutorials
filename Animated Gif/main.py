# Helpful articles/functions
# Programmatically generate video or animated GIF in Python?
# https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
# Custom Frame Duration for Animated Gif in Python ImageIO
# https://stackoverflow.com/questions/38433425/custom-frame-duration-for-animated-gif-in-python-imageio
import imageio
import os

def assemble_animated_gif(dir_path, filenames, filename_out):
    filepath_out = os.path.join(dir_path, filename_out)
    images = []
    for filename in filenames:
        temp = os.path.join(dir_path, filename)
        image = imageio.imread(temp)
        images.append(image)
    imageio.mimsave(filepath_out, images, format='GIF', duration=1)

def assemble_filenames(name, number):
    filenames = []
    for i in range(1, number, 1):
        s = "{}{}.gif".format(name, i)
        filenames.append(s)
    return filenames

def main():
    dir_path = os.path.join("data", "gif02")
    filenames = assemble_filenames("face", 13)
    assemble_animated_gif(dir_path, filenames, "gif02.gif")

if __name__ == "__main__":
    main()
