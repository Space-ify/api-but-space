# STL
import math, random, numpy
import json


# PDM
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
        # print(str(track) + "\n")
        pop = popToPop(track.get("popularity"))
        
        

        return track

def popToPop(pop):

    tens = max(10,10**(pop//20))
    r = random.randrange(900000000,1000000000)/1000000
    population = int(pop*r*tens)
    print(f" {pop} = pop:" + str(population))
    return population


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