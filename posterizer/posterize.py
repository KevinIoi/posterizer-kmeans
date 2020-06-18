from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import argparse
from parse_util import boolParse, smootherParse, kernelParse
from os import path
from pathlib import Path

def main(args):
    try:
        outfile = open(Path(args.outPath[0])),'w')
        outfile.close()
    except:
        raise FileNotFoundError("invalid output path provided {}".format(args.outPath[0]))

    # PIL has been exceptions than me
    img = Image.open(Path(args.inPath[0]))

    # apply smoothing if requested
    if args.smoother:
        img = np.array(img)
        pool_smoothing(img,kernel_size=args.kernel,
                    stride=args.stride, method=args.smoother)

    altered_img = posterize(img, degree=args.K[0])
    altered_img.save(args.outPath[0])

def posterize(original_img, degree = 5):
    '''
        Applies k-means clustering to find the dominant colours
        in an image and resets all pixels to be the closest dominant
        colour

        params:
            original_img (array or image): image to be altered
            degree(int): degree to posterize the image,
                lower value means higher level of alteration
        return:
            PIL image:
                posterized image
    '''
    if not isinstance(original_img,np.ndarray):
        np_img = np.array(original_img)
    else:
        np_img = original_img

    # reshape to list of rgb (or greyscale) tuples
    dims = np_img.shape
    np_img.shape = (np.prod(dims[:-1]),dims[-1])

    # fit model to get dominant colours
    model = KMeans(n_clusters=degree,random_state=101)
    model.fit(np_img)
    centroids = model.cluster_centers_

    # replace pixels with their closest dominant colour
    for idx, pixel_label in enumerate(model.labels_):
        np_img[idx] = centroids[pixel_label]
    np_img.shape = dims

    return Image.fromarray(np_img)

def pool_smoothing(img, kernel_size=(2,2), stride=(1,1), method='avg'):
    '''
        Inplace function for smoothing via kernel pooling

        params:
            filter (np.array): grid of pixels being pooled
            kernel_size (tuple): dimensions of kernel smoother
            stride (tuple): movement of kernel
            method (str): the type of pooling to perform
                MUST be {'avg', 'min', 'max'}
    '''
    dims = img.shape

    if len(dims)>3:
        raise ValueError("Not able to pool img with dimensions {}".format(dims))
    if (dims[0]/kernel_size[0])%stride[0] != 0 or (dims[1]/kernel_size[1])%stride[1]:
        raise ValueError("kernel size and stride combination do not fit image dimensions, {},{}".format(kernel_size, stride))

    if method == 'avg':
        pool_func = lambda x: np.mean(np.mean(x, axis=0), axis=0)
    elif method == 'max':
        pool_func = lambda x: np.min(np.min(x, axis=0), axis=0)
    elif method =='min':
        pass
    else:
        raise ValueError("Invalid pooling method provided: {}".format(method))


    for idy in range(dims[0]//kernel_size[0]):
        y = idy*stride[0]
        for idx in range(dims[1]//kernel_size[1]):
            x = idx*stride[1]
            smoothed = pool_func(img[y:y+kernel_size[1],x:x+kernel_size[0]])
            for target_y in range(y,y+kernel_size[1]):
                for target_x in range(x,x+kernel_size[0]):
                    img[target_y,target_x] = smoothed


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process input parameters')
    parser.add_argument('--K', metavar='--K', type=int, nargs=1,
                help='int, posterization level, lower the value more posterized image becomes (aka # clusters)')
    parser.add_argument('--inPath', metavar='--inPath', type=str, nargs=1,
                help='str, adr of image to posterize')
    parser.add_argument('--outPath', metavar='--outPath', type=str, nargs=1,
                help='str, adr to save posterized img')
    parser.add_argument('--smoother', metavar='--smoother', type=smootherParse, default=None,
                help='Optional; str, defines what smoothing method should be used')
    parser.add_argument('--kernel', metavar='--kernel', type=kernelParse, default="2,2",
                help='Optional; str, smoothing kernel size')
    parser.add_argument('--stride', metavar='--stride', type=kernelParse, default="1,1",
                help='Optional; str, smoothing stride size')
    args = parser.parse_args()

    main(args)
