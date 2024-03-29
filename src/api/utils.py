# STL
import base64, math
import numpy as np
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
    img2 = Image.open(image2_path).resize(img1.size)

    weight1 = 0.75
    weight2 = 0.25

    result = Image.blend(img1, img2, weight2 / (weight1 + weight2))
    result.save(output_path)


def create_elliptical_gradient(width, height, color1, color2, color3, output_path):
    image = np.zeros((height, width, 3), dtype=np.uint8)

    center_x, center_y = width // 2, height // 2
    max_distance = np.sqrt((width / 2) ** 2 + (height / 2) ** 2)

    for y in range(height):
        for x in range(width):
            distance_x = abs(x - center_x)
            distance_y = abs(y - center_y)
            distance = np.sqrt((distance_x / (width / 2)) ** 2 + (distance_y / (height / 2)) ** 2)

            if distance <= 1:
                gradient = distance
                pixel_color = tuple(int(color1[i] * (1 - gradient) + color2[i] * gradient) for i in range(3))
            else:
                gradient = (distance - 1) / (max_distance - 1)
                pixel_color = tuple(int(color2[i] * (1 - gradient) + color3[i] * gradient) for i in range(3))

            image[y, x, :] = pixel_color

    Image.fromarray(image).save(output_path)