#!/usr/bin/env python
# title           :create_map_tiles_from_image.py
# description     : Creates the tiles and structure needed for leaflet images by providing it an image location
# author          :Chris Sprance / Entrada Interactive
# date            :06/02/15
# usage           : Creates a gui using Gooey
# notes           :
# python_version  :2.7.5
# ==============================================================================
# gdal2tiles.py -p raster -z 0-6 -w none eso.jpg
from gooey import Gooey, GooeyParser


class CreateMapTilesFromImage(object):
    """Creates the tiles and structure needed for leaflet images by providing it an image location"""

    def __init__(self, image_path):
        super(CreateMapTilesFromImage).__init__()
        self.image_path = image_path
