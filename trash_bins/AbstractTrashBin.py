from PIL import Image
from exceptions import InvalidPathError

class AbstractTrashBin:
    img: Image
    name: str

    def __init__(self, img_path: str, name: str):
        try:
            self.img = Image.open(img_path)
        except IOError:
            raise InvalidPathError("This image file does not exist!")
        
        self.name = name

    def move_bin(self):
        ...

    def cycle_bin(self):
        ...