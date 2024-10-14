import os
import cv2
from tqdm import tqdm

path = r'E:\tmp\3\equirect_depth'
save_path = r'E:\tmp\3\depth'

os.makedirs(save_path, exist_ok=True)

items = os.listdir(path)
for item in tqdm(items):
    name = item.split('.')[0]
    img = cv2.imread(os.path.join(path, item))
    img = img[:, 512:1536]
    cv2.imwrite(os.path.join(save_path, name + '.png'), img)