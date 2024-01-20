from PIL import Image

# Open an image file
image_path = "./assets/trash.jpg"
img = Image.open(image_path)

# Now, 'img' is a Pillow Image object, and you can perform various operations on it
# For example, you can display the image:
img.show()