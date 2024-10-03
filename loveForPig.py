import cv2
import numpy as np
import os
import time

def resize_image(image, new_width=100):
    (h, w) = image.shape[:2]
    aspect_ratio = h / w
    new_height = int(aspect_ratio * new_width / 2)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def is_frame_black(frame):
    return np.mean(frame) < 10  # 判断是否为黑帧

def rgb_to_ansi(r, g, b):
    # 将 RGB 转换为 ANSI 颜色代码
    return f"\033[38;2;{r};{g};{b}m"

def update_binary_display(frame, prev_frame, new_width):
    # 输出每个像素对应的字符和颜色
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            pixel = frame[i, j]
            prev_pixel = prev_frame[i, j] if prev_frame is not None else None
            
            # 如果当前像素与前一帧像素不同，才更新
            if prev_pixel is None or not np.array_equal(pixel, prev_pixel):
                char = '1' if np.mean(pixel) > 128 else '0'  # 根据灰度值决定字符
                color = rgb_to_ansi(pixel[2], pixel[1], pixel[0])  # BGR 转 RGB
                print(f"\033[{i+1};{j+1}H{color}{char}\033[0m", end='')  # 使用光标定位输出字符

def main(video_file):
    cap = cv2.VideoCapture(video_file)
    prev_frame = None

    # 使用 ANSI 控制码移动光标到左上角，避免整屏刷新
    print("\033[2J")  # 初始化清屏并移动光标
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = resize_image(frame)

        if is_frame_black(resized_frame):
            continue  # 跳过黑帧

        update_binary_display(resized_frame, prev_frame, resized_frame.shape[1])
        prev_frame = resized_frame.copy()  # 保存当前帧以供下一帧比较
        
        time.sleep(0.01)  # 控制帧率

    cap.release()

if __name__ == "__main__":
    video_file = 'video.mp4'  # 替换为你的视频文件名
    main(video_file)
