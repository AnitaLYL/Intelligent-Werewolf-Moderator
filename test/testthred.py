import threading
import time
import pygame
import cv2


def printer(t):  # 让多个线程来执行它
    while True:
        t += 1
        time.sleep(1)
        print(t)


def video():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()  # frame shape 640*480*3
        frame = cv2.flip(frame, 180)  # 图像翻转
        if ret is not True:
            print('cant')
            break
        # image = Image.fromarray(frame[..., ::-1])  # bgr to rgb 仅yolo使用
        cv2.imshow('YOLO4_Deep_SORT', frame)


def audio():
    a = pygame.mixer.init()
    pygame.mixer.music.load("test/speech_male_sample.wav")
    pygame.mixer.music.play()


def threadfun(t):  # 线程任务函数 threadfun()
    while True:
        t += 1
        time.sleep(1)
        print(t)


ta = threading.Thread(target=threadfun, args=(1,))  # 创建一个线程ta，执行 threadfun()
tb = threading.Thread(target=video)  # 创建一个线程tb，执行threadfun()
ta.start()  # 调用start()，运行线程
tb.start()
