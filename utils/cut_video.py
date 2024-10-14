import cv2


def crop_video(video_path, output_path, crop_x1, crop_y1, crop_x2, crop_y2):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 获取视频的宽度、高度、帧率
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 裁剪的宽度和高度
    crop_width = crop_x2 - crop_x1
    crop_height = crop_y2 - crop_y1

    # 定义视频编码器并创建 VideoWriter 对象
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (crop_width, crop_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 裁剪帧 (y1:y2, x1:x2)
        cropped_frame = frame[crop_y1:crop_y2, crop_x1:crop_x2]

        # 写入裁剪后的帧
        out.write(cropped_frame)

    # 释放视频捕获器和视频写入器
    cap.release()
    out.release()
    print(f"Cropped video saved as {output_path}")


if __name__ == '__main__':
    video_path = r'E:\tmp\3\res_2d_output_video.mp4'  # 原始视频路径
    output_path = r'E:\tmp\3\res_2d_output_video_cut.mp4'  # 输出裁剪后视频的路径

    # 裁剪范围 (x1, y1) 到 (x2, y2)，根据你的需求调整
    crop_x1, crop_y1 = 512, 0  # 左上角坐标
    crop_x2, crop_y2 = 1536, 1024  # 右下角坐标

    crop_video(video_path, output_path, crop_x1, crop_y1, crop_x2, crop_y2)
