#!/usr/bin/env python3
from time import time
import numpy as np
from skimage import color, data
import skimage.restoration as skres
from scipy.signal import wiener, medfilt2d
from matplotlib.pyplot import subplots, show

img = color.rgb2gray(data.astronaut())
img += 0.5 * img.std() * np.random.randn(*img.shape)
img.clip(0.0, 1.0, img)
# %%
tic = time()
denoise_wie = wiener(img)
print("Wiener {:.1f} sec".format(time() - tic))
tic = time()
denoise_med = medfilt2d(img)
print("Median {:.1f} sec".format(time() - tic))
tic = time()
denoise_tvc = skres.denoise_tv_chambolle(img)
print("TV Chambolle {:.1f} sec".format(time() - tic))
tic = time()
denoise_tvb = skres.denoise_tv_bregman(img, weight=10.0)
print("TV Bregman {:.1f} sec".format(time() - tic))
tic = time()
denoise_bil = skres.denoise_bilateral(img, multichannel=False)
print("Bilateral {:.1f} sec".format(time() - tic))
# %%
fg, axs = subplots(2, 3, sharex=True, sharey=True, figsize=(12, 10))
axs = axs.ravel()
axs[0].imshow(img, cmap="gray")
axs[1].imshow(denoise_wie, cmap="gray")
axs[2].imshow(denoise_med, cmap="gray")
axs[3].imshow(denoise_tvc, cmap="gray")
axs[4].imshow(denoise_tvb, cmap="gray")
axs[5].imshow(denoise_bil, cmap="gray")

axs[0].set_title("Original noisy")
axs[1].set_title("Wiener")
axs[2].set_title("Median")
axs[3].set_title("TV Chambolle")
axs[4].set_title("TV Bregman")
axs[5].set_title("Bilateral")

for a in axs:
    a.autoscale(True, tight=True)
fg.tight_layout()
show()
