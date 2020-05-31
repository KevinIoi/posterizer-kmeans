# posterizer-kmeans

An image posterizer using k-means clustering and kernel smoothing. Clustering is performed to extract the dominant colours from the images and group the
existing pixels to fit those centroid colours. The smoother helps to scrub out outlier pixels

## Examples


## Usage

The script is setup to run on the command line

Arguments are:
--K -> int, posterization level, lower the value more posterized image becomes (aka # clusters)
--inPath -> str, adr of image to posterize
--outPath -> str, adr to save posterized img
--smoother -> Optional; str, defines what smoothing method should be used; default None
--kernel -> Optional; str, smoothing kernel size; default (2,2)
--stride -> Optional; str, smoothing stride size; default (1,1)

If you use a smoother, please keep in mind that the stride and kernel size will have to fit to the provided image

Example:
```
python -m posterize \
    --K 5 \
    --inPath test-image.jpg  \
    --outPath altered-image.jpg \
    --smoother avg \
    --kernel 2,2 \
    --stride 1,1
```
or
```
python -m posterize \
    --K 5 \
    --inPath test-image.jpg  \
    --outPath altered-image.jpg
```

## Dependancies
- python 3.6+
- PIL
- sklearn
- numpy
