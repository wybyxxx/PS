# 根据0文件夹中剩余的图片名称，删除1 2文件夹中多余的图片
import os
import shutil
# 文件夹路径
folder0 = r'E:\jxufe\data\medical\triple\2'
folder1 = r'E:\jxufe\data\medical\triple\1'
folder2 = r'E:\jxufe\data\medical\triple\0'

def filter_photos(folder0, folder1, folder2):
    # 获取第一组剩下的照片文件名（不包括扩展名）
    remaining_photos = os.listdir(folder0)
    # 函数用于保留具有相同文件名的照片
    def retain_photos(src_folder):
        # 遍历源文件夹中的所有文件
        for filename in os.listdir(src_folder):
            if filename not in remaining_photos:
                os.remove(os.path.join(src_folder, filename))
    # 处理第二组和第三组照片
    retain_photos(folder1)
    retain_photos(folder2)

filter_photos(folder0, folder1, folder2)
