import cv2
import warnings
import os
 
# 过滤所有警告，可以使用 'ignore' 或 'always' 动作
warnings.filterwarnings('ignore')
# save_cam_list_path = r'E:\jxufe\data\medical\save_cam_list'
# os.makedirs(save_cam_list_path,exist_ok=True)
# 这里的代码不会输出任何由于上面的警告触发的消息
# 检测并列出可用的摄像头
def list_cameras():
    # 获取所有可用摄像头的索引
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            a=0
        else:
            print(f"Found camera: {index}")  # 打印找到的摄像头索引
            _, frame = cap.read()
            # cv2.imwrite(os.path.join(save_cam_list_path, f'{index}.jpg'), frame)
            cap.release()
        index += 1
 
# 主程序
if __name__ == '__main__':
    list_cameras()  # 列出所有可用摄像头
