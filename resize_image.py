from PIL import Image

def resize_img():
    img = input("Enter image need to resize: ")
    my_img = Image.open(f"{img}.png")
    size = int(input("Enter size of new image: "))
    my_img = my_img.resize((size, size))
    my_img.save(f"{img}_resized.png")

resize_img()