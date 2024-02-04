# STL
import math, random
import numpy as np
import json
import requests
import cv2
from sklearn.cluster import KMeans
import api.utils as utils


from PIL import Image, ImageDraw


class Transformer:

    def __init__(self,playlist) -> None:
        self.tracklist = []
        self.translatePlaylist(playlist)


    def translatePlaylist(self,playlist) -> None:

        tracks = playlist.get("tracks", {}).get("items",{})

        for track in tracks:

            trackData = self.__planetToData(track.get("track",{}))
            self.tracklist.append(trackData)
            # print(f"new track data: " + trackData)
        pass

    
    def __planetToData(self,track):
        # print(track)

        details = track
        pop = pop_to_pop(track.get("popularity",{}))
        name = track.get("name",{})
        artist_name = track.get("artists",{})
        is_explicit = track.get("explicit",{})

        album_img = track.get("album").get("images")[0].get("url")

        r = random.randrange(0,100)
        save_path = (f"{r}") + ".jpeg"

        download_image(album_img, save_path)
        downscale(save_path, save_path, 0.1)

        top_colors = get_top_colors(save_path,3)
        if top_colors.any(): print("Top colors:", top_colors)

        utils.create_elliptical_gradient(512,256,tuple(top_colors[0]), tuple(top_colors[1]), tuple(top_colors[2]),save_path)

        texture_path = random_texture()
        utils.color_multiply(save_path,texture_path, save_path)

        return track
    






def random_texture():

    n = random.randrange(1,5)
    input_str = (f"textures/{n}.jpg")
    out_str = (f"textures/{n}.1.jpg")
    downscale(input_str,out_str,1/4)
    return out_str




def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded and saved at {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")



def pop_to_pop(pop):

    tens = max(10,10**(pop//20))
    r = random.randrange(900000000,1000000000)/1000000
    population = int(pop*r*tens)
    # print(f" {pop} = pop:" + str(population))
    return population


def get_top_colors(image_url, num_colors):

    # response = requests.get(image_url)
    # print(response)

    image = cv2.imread(image_url)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pixels = image.reshape((-1, 3))

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_
    colors = colors.astype(int)

    return colors



def downscale(input, output, factor):
    
    original_image = Image.open(input)

    new_width = int(original_image.width * factor)
    new_height = int(original_image.height * factor)

    downscaled_image = original_image.resize((new_width, new_height), Image.LANCZOS)
    downscaled_image.save(output)

    pass


def create_rgb_gradient(color1, color2, color3, height):
    width = 2 * height

    gradient_image = Image.new('RGB', (width, height))

    pixels = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        ratio = y / (height - 1)
        intermediate_color1 = np.array(color1) * (1 - ratio) + np.array(color2) * ratio
        intermediate_color2 = np.array(color2) * (1 - ratio) + np.array(color3) * ratio

        for x in range(width):
            ratio_x = x / (width - 1)
            final_color = intermediate_color1 * (1 - ratio_x) + intermediate_color2 * ratio_x
            final_color = [int(final_color[0]), int(final_color[1]), int(final_color[2])]
            final_color = tuple(final_color)
            gradient_image.putpixel((x, y), final_color)

    return gradient_image




def main():

    data = {}

    # print("_")
    with open("test_playlist.json","r") as f:
        data = f.read()
        # print(data)

    playlist = json.loads(data)
    # print(playlist)
    t = Transformer(playlist)


if __name__ == "__main__":
        main() 