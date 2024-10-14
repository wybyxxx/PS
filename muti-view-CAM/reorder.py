import os

def reorder(folder_path):
    # 获取所有以数字命名的文件
    files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    # 按照数字大小排序
    files.sort(key=lambda x: int(x.split('.')[0]))
    print(files)
    # # 重命名文件
    for index, file in enumerate(files):
        old_file_path = os.path.join(folder_path, file)
        new_file_name = f"{index}.jpg"
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(old_file_path, new_file_path)

    print("重命名完成！")


if __name__ == '__main__':
    reorder(r'E:\tmp\3\blender_create')
    reorder(r'D:\Files\jxufe\data\medical\3d\1')
    reorder(r'D:\Files\jxufe\data\medical\3d\2')

