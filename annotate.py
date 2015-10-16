from PIL import Image, ImageDraw

RADIUS = 5
XPOS = 20
YPOS = 30

original = Image.open("t_0.png")
draw = ImageDraw.Draw(original)
draw.ellipse((XPOS-RADIUS, YPOS-RADIUS, XPOS+RADIUS, YPOS+RADIUS))
original.save("annotated.png")
