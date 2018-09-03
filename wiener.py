#!/usr/bin/env python
import numpy as np
from skimage import color, data, restoration
from matplotlib.pyplot import subplots, show
from scipy.signal import convolve2d

img = color.rgb2gray(data.astronaut())
psf = np.ones((5, 5)) / 25
noisy = convolve2d(img, psf, 'same')
noisy += 0.1 * noisy.std() * np.random.standard_normal(noisy.shape)
deconvolved_img = restoration.wiener(noisy, psf, 1100)

fg, ax = subplots(1, 2, figsize=(12, 5))

ax[0].imshow(img)
ax[1].imshow(deconvolved_img)

show()
