# STL
import math
import random

# PDM
from PIL import Image, ImageDraw


class ImageGenerator:
    def __init__(self) -> None:
        pass

    def spotifyToData(self):
        
        for (let index = 0; index < totalPlanets; index++) {
            planetData.push({
                id: index,
                color: randomColor(),
                xRadius: (index + 1.5) * 4,
                zRadius: (index + 1.5) * 2,
                size: random(0.5, 1),
                speed: random(0.1, 0.6),
                offset: random(0, Math.PI * 2),
                rotationSpeed: random(0.01, 0.03),
                textureMap: textures[index]
            });
        }