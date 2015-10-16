from PIL import Image

XOFF = 22;
YOFF = 35;

background = Image.open("t_0.png")
foreground = Image.open("t_30.png")
mask=Image.new('L', foreground.size, color=122)

background.paste(foreground, (XOFF, YOFF), mask)
background.save("overlayed.png")

# Image.eval(foreground, lamba x: x+(
#
# blended = Image.blend(background, foreground, 0.5)
# blended.show()
