import cv2
import glob
import numpy as np
import math
def equirectangular_to_cylindrical(img, fov=240, cylindrical_w=2048, cylindrical_h=512):
    h, w, _ = img.shape

    # Define the dimensions of the cylindrical projection
#     cylindrical_w = w
#     cylindrical_h = int(h / 2)

    # Create meshgrid for the output cylindrical image
    x, y = np.meshgrid(np.arange(cylindrical_w), np.arange(cylindrical_h))

    # Constants for the conversion
    fov = (fov/180)*math.pi  # 180 degrees field of view
    r = cylindrical_w / fov

    # Calculate theta and phi for each pixel in the cylindrical image
    theta = (x - cylindrical_w / 2) / r
    phi = (y - cylindrical_h / 2) / r

    # Calculate corresponding coordinates in the equirectangular image
    lon = theta
    lat = phi

    px = ((lon + math.pi) / (2 * math.pi) * w).astype(int)
    py = ((lat + (math.pi / 2)) / math.pi * h).astype(int)

    # Ensure the indices are within bounds
    px = np.clip(px, 0, w - 1)
    py = np.clip(py, 0, h - 1)

    # Use the indices to map the pixels
    cylindrical_img = img[py, px]

    return cylindrical_img