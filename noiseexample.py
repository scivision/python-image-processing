#!/usr/bin/python
""" Michael Hirsch
GPLv3+
crude example of reducing banding interference in image.
Should not just toss in a zero to reduce sidelobes--should use a smoother taper
"""
from __future__ import division
from numpy import log10, absolute,asarray,real
from numpy.fft import fft2,ifft2,fftshift,fft,ifftshift
from scipy.ndimage import imread
from scipy.io import loadmat
from matplotlib.pyplot import figure,show,subplots
#from matplotlib.colors import LogNorm
from os.path import expanduser,splitext

def main(fn,clip,zo,zw,minmax,imgvarname):
    ext = splitext(fn)[1]
    if ext.lower() == '.mat':
        mat = loadmat(fn)
        img = mat[imgvarname]
    else:
        img = imread(fn,flatten=True)

    if clip[0] is not None:
        img = img[clip[2]:clip[3],clip[0]:clip[1]]

    I = fft2(img)

    Ifilt = zeroout(I,zo,zw)

    imgfilt = real(ifft2(Ifilt)) #discards miniscule imaginary component left over

    plots(img,imgfilt,Ifilt,minmax)

def zeroout(I,zo,zw):
    """crude filter for mitigating band interference"""
    if zo[0] is None:
        return I

    zo = asarray(zo).reshape((-1,2)) #to iterate over as x,y pairs

    I = fftshift(I.copy())

    zw2 = zw//2 #TODO generalize to odd and even!
    for z in zo:
        I[z[1],z[0]-zw2:z[0]+zw2+1] = 5  # very crude! could use smoother shape to reduce sidelobes

    return ifftshift(I)

def plots(img,imgfilt,Ifilt,mm):
    fg = figure()
    ax = fg.gca()
    hi = ax.imshow(img,cmap='gray',interpolation='none',vmin=mm[0],vmax=mm[1])
    ax.set_title('original JPG image')
    fg.colorbar(hi)

    fg = figure()
    ax = fg.gca()
    Ifs = fftshift(Ifilt)
    hi = ax.imshow(absolute(10*log10(Ifs)),cmap='gist_heat',interpolation='none')
    ax.set_title('FFT(image)) [dB]')
    fg.colorbar(hi)
#%% collapse to 1-D
    vsum = img.sum(axis=0)
    vsum /= vsum.max()
    fg,(ax0,ax1) = subplots(2,1)
    ax0.plot(vsum)
    ax0.set_title('UNfiltered: sum down rows')
    #ax0.set_xlabel('x-pixel')
    ax0.set_ylabel('$\sum_y$')
    ax0.autoscale(True,tight=True)
    ax0.grid(True)

    vsumfilt = imgfilt.sum(axis=0)
    vsumfilt /= vsumfilt.max()
    ax1.plot(vsumfilt)
    ax1.set_title('filtered: sum down rows')
    ax1.set_xlabel('x-pixel')
    ax1.set_ylabel('$\sum_y$')
    ax1.autoscale(True,tight=True)
    ax1.grid(True)

    fg,(ax0,ax1) = subplots(2,1)
    I1d = fft(vsum)
    ax0.plot(absolute(10*log10(I1d)))
    ax0.set_title('FFT($\sum_{y,unfilt}$) [dB]',y=1.05)
    ax0.set_ylabel('$\sum_y$ dB')
    ax0.autoscale(True,tight=True)
    ax0.grid(True)

    If1d = fft(vsumfilt)
    ax1.plot(absolute(10*log10(If1d)))
    ax1.set_title('FFT($\sum_{y,filt}$) [dB]',y=1.08)
    ax1.set_ylabel('$\sum_y$ dB')
    ax1.autoscale(True,tight=True)
    ax1.grid(True)

#    hsum = img.sum(axis=1)
#    hsum /= hsum.max()
#    ax = figure().gca()
#    ax.plot(hsum)
#    ax.set_title('sum across columns')

#%% filtered image
    fg = figure(); ax = fg.gca()
    hi = ax.imshow(imgfilt, cmap = 'gray',interpolation='none',vmin=mm[0],vmax=mm[1])
    ax.set_title('Filtered image')
    fg.colorbar(hi)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser('read and analyse image files')
    p.add_argument('fn',help='file to analyse',nargs='?',default=None,type=str)
    p.add_argument('-c','--clip',help='xmin xmax ymin ymax pixel coordinates to clip',nargs=4,type=int,default=(None,None,None,None))
    p.add_argument('-z','--zero',help='center(s) of regions to zero out for interference filter',nargs='+',type=int,default=[None])
    p.add_argument('-w','--zerowidth',help='horizontal (x) width to zero out from specified places',type=int,default=1)
    p.add_argument('-l','--minmax',help='min max pixel values in colormap (for plotting only)',nargs=2,type=int,default=(None,None))
    p.add_argument('-n','--imgvarname',help='name of image variable in matlab .mat file',type=str,default=None)
    a = p.parse_args()

    if a.fn is None:
        from easygui import fileopenbox
        fn = fileopenbox('pick image to analyse')
    else:
        fn = a.fn

    if fn is not None:
        main(expanduser(fn),a.clip,a.zero, a.zerowidth, a.minmax, a.imgvarname)
        show()
    else:
        exit('no file selected')