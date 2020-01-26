Hello! This is a little program I wrote because I needed a cartoon portrait.

I found a dataset kindly provided by the awesome folks at Google. You can 
find it here:

https://google.github.io/cartoonset/

I wanted my portrait to resemble me as closely as possible, which was a problem since
it meant searching through 10,000 png files!

This was definitely a job for Python.

I'm in the middle of another project so I couldn't spend a lot of time on this.
That's why I used a text interface (the cmd module). 

All the cartoon faces you select are saved in: saved_image_names.txt.

It turns out, though, that (at least on my computer) when I use matplotlib to 
display the cartoon portraits I've selected that the final portrait will display 
but the program will crash.

I got around this by using cmd to select the photos and then using a function
outside of cmd to display them. It's awkward, but I didn't have the time to
do anything more sophisticated. It works.

Here is a mini-tutorial.

loadchoices default
Loads a default set of attributes which, if applied to the dataset, would select
every single face in the dataset.

printchoices
Prints the current set of attributes used to select faces from the dataset.

alterproperty eye_color 2 3
That's an example. There are 20 properties, eyecolor among them. To see a compete list
use the PRINTCHOICES command. Also use the printchoices command to find out which
values are allowed.

savechoices
Saves the attributes you've selected to a file.

loadchoices personal
Loads the choices you've saved to file.

Example 01:
# First use of the program. Run main.py.

Input "s":
> s

> loadchoices default
> alterproperty hair 30 31 32
> alterproperty eye_color 2 3
> alterproperty hair_color 2 3
> alterproperty glasses 6 7
> loadchoices personal
# loadchoices personal actually applies the filter you've created to the dataset.
> printfaces
# This will show you the characteristics of the faces you've selected.

To view the png file, end the program by typing: bye.
> bye

Run the program again. Now type "v".
> v

You will now see each png file. Close them by typing (on the Mac) Command + w.

# ----------------------------------------------------------------------------

I hope this has helped! It's a really cool dataset.

It would be cool to do a second version of this program so that even people
who didn't know Python could use it!

Let me know what you think! karen dot friesen at gmail dot com.
