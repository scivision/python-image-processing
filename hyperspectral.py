#!/usr/bin/env python
from pathlib import Path
import imageio
from matplotlib.pyplot import show,subplots
#from spectral import rx
from numpy import empty,zeros_like,around,uint8

def quadstack(fn,xc,yc,xs,ys):
    fn = Path(fn).expanduser()
    imgr = rgba2gray(imageio.imread(fn)) #this has all four quadrants
#%% extract four quadrants from one image, knowing a priori the system geometry performance
    """
    """
    img = {} #we don't know if they'll all be the same size even due to affine distortion
    img['4278'] = imgr[yc[0]:yc[1],xc[0]:xc[1]]
    img['5577'] = imgr[yc[1]:yc[2],xc[0]:xc[1]]
    img['7320'] = imgr[yc[0]:yc[1],xc[1]:xc[2]]
    img['6300'] = imgr[yc[1]:yc[2],xc[1]:xc[2]]
#%% extract subimage
    ims = empty((4,ys[1]-ys[0],xs[1]-xs[0]),dtype=uint8)
    for i,I in enumerate(img):
        ims[i,...] = img[I][ys[0]:ys[1],xs[0]:xs[1]]

    return ims,img

def imgfilt(img,thres):
    """
    trivial intensity threshold "filter"
    """
    imgf = zeros_like(img,dtype=bool)
    imgf[img>thres] = True

    return imgf

def plots(img,imgproc,mm,full,thres):
    fg,ax = subplots(2,2)
    ax = ax.ravel()
    for a,I,f in zip(ax,img,full):
        hi = a.imshow(I,cmap='gray',interpolation='none')#,vmin=mm[0],vmax=mm[1])
        fg.colorbar(hi,ax=a)
        a.set_title(f)
        a.axis('off')
    fg.suptitle('original image')

    fg,ax = subplots(2,2)
    ax = ax.ravel()
    for a,I,f in zip(ax,imgproc,full):
        hi = a.imshow(I,cmap='gray',interpolation='none',vmin=0,vmax=1)
        #fg.colorbar(hi,ax=a)
        a.set_title(f)
        a.axis('off')
    fg.suptitle('threshold image >= {:.0f}'.format(thres))


def rgba2gray(rgba):
    """
    discards transparancy, assumes single m x n x 4 image
    """
    return around(rgba[...,:-1].dot([0.299,0.587,0.114])).astype(rgba.dtype)

if __name__ == '__main__':
    """
    ./hyperspectral.py fig10.png --xc 841 1235 1623 --yc 41 442 863 --xs 50 325 --ys 50 350
    ./hyperspectral.py fig12.png --xc 734 1081 1392 --yc 32 377 863 --xs 50 300 --ys 50 325
    """
    from argparse import ArgumentParser
    p = ArgumentParser('read and analyse hyperspectral image files')
    p.add_argument('fn',help='file to analyse')
    p.add_argument('--xc',help='x0 x1 x-pixel coordinates to clip',nargs=3,type=int)
    p.add_argument('--yc',help='y0 y1 y-pixel coordinates to clip',nargs=3,type=int)
    p.add_argument('--xs',help='x0 x1 x-pixel coordinates to clip within each subimage (ROI)',nargs=2,type=int,default=(None,None))
    p.add_argument('--ys',help='y0 y1 x-pixel coordinates to clip within each subimage (ROI)',nargs=2,type=int,default=(None,None))
    p.add_argument('-t','--thres',help='threshold above which detection is declared',type=float,default=100)
    p.add_argument('-l','--minmax',help='min max pixel values in colormap (for plotting only)',nargs=2,type=int,default=(None,None))
    p = p.parse_args()

    img,full= quadstack(p.fn,p.xc,p.yc,p.xs,p.ys)
    imgf = imgfilt(img,p.thres)
    plots(img, imgf, p.minmax,full,p.thres)

    show()
