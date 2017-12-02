import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import uuid

import skimage
import skimage.io
import skimage.filters
import skimage.feature
import skimage.morphology
import skimage.color
import skimage.draw
import skimage.measure
import skimage.transform

import pandas as pd

import sklearn
import sklearn.decomposition

import scipy
import scipy.ndimage
import numpy as np


def load(path):
    img_src=skimage.io.imread(path)
    img_src=skimage.color.rgb2hsv(img_src)
    return img_src

def resize(image):
    lx,ly,lz=image.shape
    k1=min(lx,ly)//50
    k2=k1//10
    if k1 % 2 ==0:
        k1+=1
    resize_k = ((lx//640), (ly//480))
    resized_image = skimage.transform.resize(image, (lx//(lx//640),ly//(ly//480)))
    return resized_image


def select_color(image, black_h = 0.35, black_s = 1, black_v = 0.15, alpha = 0.2, alpha_v = 0.25):
    h = image[:,:,0]
    s = image[:,:,1]
    v = image[:,:,2]
    mask_h = np.all([((black_h - alpha) < h), (h > (black_h + alpha))], axis=0)
    mask_s = np.all([((black_s - alpha) < s), (s > (black_s + alpha))], axis=0)
    mask_v = np.all([((black_v - alpha_v) < v), (v > (black_v + alpha_v))], axis=0)
    sel_img = image.copy()
    sel_img[mask_h.astype(bool),1] = 0
    sel_img[mask_v.astype(bool),:] = 1
    return sel_img


def find_contour(image, contour_level=0.21, perimiter_border=20000):
    contours = skimage.measure.find_contours(skimage.color.rgb2gray(skimage.color.hsv2rgb(image)), contour_level, fully_connected='low', positive_orientation='low')
    polygons = []
    plt.figure(0, figsize=(10, 10))

    for n, contour in enumerate(contours):
        pow_contour = np.power(contour, 2)
        p = np.sum(np.sqrt(np.abs(pow_contour[:,0] - pow_contour[:,1])))
        if p < perimiter_border:
            continue
        contour = skimage.measure.approximate_polygon(contour[:,[0,1]], 0.8)
        rr, cc = skimage.draw.polygon(contour[:, 1], contour[:, 0])
        polygons.append([rr,cc])
        plt.plot(contour[:, 1], contour[:, 0], 'k-', linewidth=3)
    plt.axis('off')
    filename = './media/{0}.svg'.format(str(uuid.uuid4()))
    plt.savefig(filename)
    
    return filename
    # with open('test.svg', mode='rb') as f:
    #     buf = f.read(-1)
    # return buf