# STL
import base64
from PIL import Image, ImageDraw


def image_to_base64_string(image_path: str):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def save_image_obj(image, save_path):
    image.save(save_path)

def crop_to_2_1_aspect_ratio(input_path, output_path):
    # Open the image
    img = Image.open(input_path)

    # Calculate the target width for a 2:1 aspect ratio
    target_width = int(img.height * 2)

    # Calculate the cropping box
    left_margin = (img.width - target_width) // 2
    right_margin = img.width - left_margin
    top_margin = 0
    bottom_margin = img.height

    # Crop the image
    cropped_image = img.crop((left_margin, top_margin, right_margin, bottom_margin))

    # Save the result
    cropped_image.save(output_path)

def color_multiply(image1_path, image2_path, output_path):
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    img2 = img2.resize(img1.size)

    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')

    weight1 = 0.75 
    weight2 = 0.25 

    multiplied_data = [
        tuple(int((p1 * weight1 + p2 * weight2) // (weight1 + weight2)) for p1, p2 in zip(data1, data2))
        for data1, data2 in zip(img1.getdata(), img2.getdata())
    ]

    multiplied_image = Image.new('RGB', img1.size)
    multiplied_image.putdata(multiplied_data)

    multiplied_image.save("images/test.png")


