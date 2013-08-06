#!/usr/bin/env python

import numpy as np
from skimage.color import rgb2hsv, hsv2rgb

from util import center, hsv_dtype, rgb_dtype, get_hsv_spectrum, read_image, write_image

def generate(image, width=4096, height=4096):
  image_width, image_height, image_bands = image.shape
  left = center(image_width, width)
  top = center(image_height, height)
  result = np.zeros((width, height, image_bands), dtype=image.dtype)
  result[left:left+image_width, top:top+image_height] = image

  result = rgb2hsv(result)
  flattened = result.view(hsv_dtype)
  flattened.shape = -1 # Throws an exception if a copy must be made
  flattened[np.argsort(flattened, order=['H', 'S', 'V'])] = get_hsv_spectrum()

  return hsv2rgb(result).view(image.dtype)

def numcolors(image):
  return np.unique(image.view(rgb_dtype)).size

def numpixels(image):
  return image.view(rgb_dtype).size

def test(image):
  return numcolors(image) == numpixels(image)

if __name__ == '__main__':
  import argparse
  import sys

  parser = argparse.ArgumentParser(description="Generates an image with every RGB color exactly once")
  parser.add_argument('command',
    choices=['generate', 'test'],
    default='generate')
  parser.add_argument('-i', '--input',
    type=argparse.FileType('r'),
    default=sys.stdin)
  parser.add_argument('-o', '--output',
    type=argparse.FileType('w'),
    default=sys.stdout)

  args = parser.parse_args()
  image = read_image(args.input)

  if args.command == 'generate':
    write_image(args.output, generate(image))
  elif args.command == 'test':
    imagecolors = numcolors(image)
    imagepixels = numpixels(image)
    print("This image has {} colors and {} pixels".format(imagecolors, imagepixels))
    sys.exit(imagecolors != imagepixels)