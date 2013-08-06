import numpy as np
from skimage.color import rgb2hsv
from skimage.io import imread # skimage.io.imsave seems to be broken?
from scipy.misc import imsave
from tempfile import mkdtemp
from os import path
from shutil import rmtree

hsv_dtype = np.dtype([('H', float), ('S', float), ('V', float)])
rgb_dtype = np.dtype([('R', float), ('G', float), ('B', float)])

def np_product(*arrays, **kwargs):
  arrays = arrays * kwargs.pop('repeat', 1)
  num_arrays = len(arrays)
  arr = np.empty(map(len, arrays) + [num_arrays], **kwargs)
  for index, array in enumerate(np.ix_(*arrays)):
    arr[..., index] = array
  return arr.reshape(-1, num_arrays)

def center(small, large):
  return (large - small) // 2

def get_rgb_spectrum():
  return np_product(np.arange(0., 1., 1./256.), dtype=float, repeat=3)

def get_hsv_spectrum():
  # FIXME: optimize
  return np.sort(rgb2hsv(get_rgb_spectrum()[np.newaxis, ...])[0, ...].view(hsv_dtype).reshape(-1), order=['H', 'S', 'V'])

def read_image(f):
  return imread(f)/256. # skimage is inconsistent with whether RGB is 0-1 or 0-255

def write_image(f, image):
  if hasattr(f, 'write'):
    tmpdirname = mkdtemp()
    tmpfilename = path.join(tmpdirname, 'tmpfile.png')
    imsave(tmpfilename, image)
    with open(tmpfilename, 'rb') as tmpfile:
      f.write(tmpfile.read())
    rmtree(tmpdirname)
  else:
    imsave(f, image)