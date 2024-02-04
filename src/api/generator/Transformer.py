# STL
import os
import json
import math
import concurrent.futures
import random
import threading

# PDM
import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans

# LOCAL
import api.utils as utils

class Transformer:
    def __init__(self, playlist) -> None:
        self.tracklist = []
        self.translatePlaylist(playlist)
        # print(self.tracklist)

    def translatePlaylist(self, playlist) -> None:
        tracks = playlist.get("tracks", {}).get("items", {})

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_track, track, i) for i, track in enumerate(tracks)]

            for future in concurrent.futures.as_completed(futures):
                try:
                    trackData, output_path = future.result()
                    self.tracklist.append(trackData)
                    os.remove(output_path)
                except Exception as e:
                    print(f"Error processing track: {e}")

    def process_track(self, track, i):
        thread_id = threading.current_thread().ident
        # print(track.get("popularity", {}))
        # print(track.keys())
        track = track.get("track",{})
        # print(track.keys())

        population = pop_to_pop(track.get("popularity", {}))
        size = get_planet_size(population)

        name = track.get("name", {})
        artist_name = track.get("artists", {})[0].get("name", {})
        is_explicit = track.get("explicit", {})

        album_img = track.get("album").get("images")[0].get("url")

        save_path = (f"{thread_id}") + ".jpeg"

        download_image(album_img, save_path)
        downscale(save_path, save_path, 0.1)

        top_colors = get_top_colors(save_path, 3)
        # if top_colors.any(): print("Top colors:", top_colors)

        utils.create_elliptical_gradient(
            512,
            256,
            tuple(top_colors[0]),
            tuple(top_colors[1]),
            tuple(top_colors[2]),
            save_path,
        )

        texture_path = random_texture()
        utils.color_multiply(save_path, texture_path, save_path)

        song_length = track.get("duration_ms", {})
        speed = determineSpeed(song_length)

        textureMap = utils.image_to_base64_string(save_path)

        preview = track.get("preview_url")
        print(preview)

        track_as_dict = {
            "id": i,
            "size": size,
            "speed": speed,
            "name": name,
            "artists": artist_name,
            "textureMap": textureMap,
            "rotationSpeed": (random.randrange(15000, 25000) / 1000000),
            "offset": random.randint(0, 10),
            "xRadius": (i * 4) + 6,
            "is_explicit": is_explicit,
            "population": population,
            "preview": preview
        }

        return track_as_dict, save_path

    # def planet_to_data(self, track, i):

    #     print(track)

    #     pop = pop_to_pop(track.get("popularity", {}))
    #     size = get_planet_size(pop)

    #     # get_planet_size(pop_to_pop(1))
    #     # get_planet_size(pop_to_pop(20))
    #     # get_planet_size(pop_to_pop(50))
    #     # get_planet_size(pop_to_pop(100))

    #     name = track.get("name", {})
    #     artist_name = track.get("artists", {})[0].get("name", {})
    #     is_explicit = track.get("explicit", {})

    #     album_img = track.get("album").get("images")[0].get("url")

    #     save_path = (f"{random.randrange(0,100)}") + ".jpeg"

    #     download_image(album_img, save_path)
    #     downscale(save_path, save_path, 0.1)

    #     top_colors = get_top_colors(save_path, 3)
    #     # if top_colors.any(): print("Top colors:", top_colors)

    #     utils.create_elliptical_gradient(
    #         512,
    #         256,
    #         tuple(top_colors[0]),
    #         tuple(top_colors[1]),
    #         tuple(top_colors[2]),
    #         save_path,
    #     )

    #     texture_path = random_texture()
    #     utils.color_multiply(save_path, texture_path, save_path)

    #     song_length = track.get("duration_ms", {})
    #     speed = determineSpeed(song_length)

    #     textureMap = utils.image_to_base64_string(save_path)

    #     preview = track.get("preview_url")
    #     print(preview)

    #     track_as_dict = {
    #         "id": i,
    #         "size": size,
    #         "speed": speed,
    #         "name": name,
    #         "artists": artist_name,
    #         "textureMap": textureMap,
    #         "rotationSpeed": (random.randrange(15000, 25000) / 1000000),
    #         "offset": random.randint(0, 10),
    #         "xRadius": (i * 4) + 6,
    #         "is_explicit": is_explicit,
    #         "population": pop,
    #         "preview": preview
    #     }

    #     return track_as_dict, save_path


def get_planet_size(value, min_value=9000, max_value=10000000000):
    dec = (value - min_value) / (max_value - min_value)

    if dec < 0.3:
        norm = dec + (0.3 - dec) / 2 + (random.randrange(1, 5) * 0.1) + 0.2
    elif dec > 0.8:
        norm = dec - (dec - 0.8) / 2 + (random.randrange(1, 5) * 0.1) + 0.2
    else:
        norm = dec + 0.2

    return norm


def determineSpeed(ms):
    return 0.05


def random_texture():
    n = random.randrange(1, 5)
    input_str = f"textures/{n}.jpg"
    out_str = f"textures/{n}.1.jpg"
    downscale(input_str, out_str, 1 / 4)

    return out_str


def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Image downloaded and saved at {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def pop_to_pop(pop):
    tens = max(10, 10 ** (pop // 20))
    r = random.randrange(900000000, 1000000000) / 1000000
    population = int(pop * r * tens)

    return population


def get_top_colors(image_url, num_colors):
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

    gradient_image = Image.new("RGB", (width, height))

    # pixels = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        ratio = y / (height - 1)
        intermediate_color1 = np.array(color1) * (1 - ratio) + np.array(color2) * ratio
        intermediate_color2 = np.array(color2) * (1 - ratio) + np.array(color3) * ratio

        for x in range(width):
            ratio_x = x / (width - 1)
            final_color = (
                intermediate_color1 * (1 - ratio_x) + intermediate_color2 * ratio_x
            )
            final_color = [
                int(final_color[0]),
                int(final_color[1]),
                int(final_color[2]),
            ]
            final_color = tuple(final_color)
            gradient_image.putpixel((x, y), final_color)

    return gradient_image


def main():
    data = {}

    with open("test_playlist.json", "r") as f:
        data = f.read()

    playlist = json.loads(data)
    t = Transformer(playlist)


if __name__ == "__main__":
    main()
