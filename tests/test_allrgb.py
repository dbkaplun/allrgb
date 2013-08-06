#!/usr/bin/env python

import unittest
from skimage.io import ImageCollection

import allrgb

class TestAllRGB(unittest.TestCase):
  def setUp(self):
    self.images = ImageCollection('tests/images/*', load_func=allrgb.read_image)

  def test_allrgb(self):
    for image in self.images:
      self.assertTrue(allrgb.test(allrgb.generate(image)))

if __name__ == '__main__':
  unittest.main()
