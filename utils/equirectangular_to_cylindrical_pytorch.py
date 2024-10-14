import os
import cv2
import numpy as np
import math
import torch
from tqdm import tqdm


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

h, w = 1024, 2048
fov = 180
cylindrical_w = 2048
cylindrical_h = 1024

# Create meshgrid for the output cylindrical image
x, y = np.meshgrid(np.arange(cylindrical_w), np.arange(cylindrical_h))

# Constants for the conversion
fov = (fov / 180) * math.pi  # 180 degrees field of view
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

px = torch.from_numpy(px).long().to(DEVICE)
py = torch.from_numpy(py).long().to(DEVICE)


def equirectangular_to_cylindrical_pytorch(img, px, py, device=DEVICE):
    img_tensor = torch.from_numpy(img).to(device)
    # print('===========',img_tensor.device, px.device,py.device)
    cylindrical_img = img_tensor[py, px].cpu().numpy()

    return cylindrical_img

if __name__ == '__main__':
    equirect_path = r'E:\tmp\3\res_images'
    cylindrical_path = r'E:\tmp\3\res_images_cylindrical'

    os.makedirs(cylindrical_path, exist_ok=True)

    items = os.listdir(equirect_path)

    for item in tqdm(items, desc='Processing images', unit='image'):
        name = item.split('.')[0]
        equirect = cv2.imread(os.path.join(equirect_path,item))

        cylindrical = equirectangular_to_cylindrical_pytorch(equirect, px, py)
        cv2.imwrite(os.path.join(cylindrical_path, name + '.png'), cylindrical)