# detector import
from __future__ import division, print_function, absolute_import
from yoloall import YOLOall
from timeit import time
import cv2
from PIL import Image
import tensorflow as tf
import os
# from tensorflow.compat.v1 import InteractiveSession
from tensorflow import InteractiveSession
from tensorflow import Session

# system import

# from detector import detector
from gamelogic import gamelogic
from processor import processor
# from GUI import gui,audio

import sys
import threading


def detectandprocess(yoloall):
    """
    init system
    """
    # init web cam
    fps = 0
    writer_fps = 25  # 保存帧率
    writeVideo_flag = False  # Save video
    video_capture = cv2.VideoCapture(0)
    # video_capture = cv2.VideoCapture(1)
    # video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 5000)
    # video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 5000)
    w = int(video_capture.get(3))
    h = int(video_capture.get(4))
    print('Camera:', (w, h))

    # init parameters
    num_player_indevice = 1  # 本机设备检测人数
    qsize = 32  # 稳定器长度

    # init system
    try:
        # init processor
        process = processor.Processor(num_player_indevice, qsize)

        # init gamelogic
        game = gamelogic.Game()

        # init gui

        print('################\n狼人杀系统初始化成功\n################')
    except:
        print('################\n狼人杀系统初始化失败\n################')

    # 存储
    if writeVideo_flag:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('./output/output.avi', fourcc, writer_fps, (w, h))

    while True:
        # stream
        ret, frame = video_capture.read()  # frame shape 640*480*3
        frame = cv2.flip(frame, 180)  # 图像翻转
        if ret is not True:
            break
        t1 = time.time()
        image = Image.fromarray(frame[..., ::-1])  # bgr to rgb 仅yolo使用

        """detector res"""
        boxs, confidence, class_names = yoloall.detect_image(image)

        """processor处理预测结果"""
        boxs_xyxy = processor.xywh2xyxy(boxs)  # 转换坐标
        process.arrange_person(boxs_xyxy, confidence, class_names)  # person排列和过滤
        process.assign_object2person(boxs_xyxy, confidence, class_names)  # hand和eye关联和过滤
        process.voting()  # 稳定输出结果

        # test visual img
        new_frame = yoloall.vis(frame, boxs_xyxy, confidence, class_names)

        # 存储
        if writeVideo_flag:
            out.write(frame)

        """测试视频输出"""
        fps = (fps + (1. / (time.time() - t1))) / 2
        cv2.putText(new_frame, "FPS: %f" % (fps), (int(20), int(40)), 0, 5e-3 * 200, (145, 145, 145), 2)
        cv2.namedWindow("YOLO4_Deep_SORT", 0)
        # cv2.resizeWindow('YOLO4_Deep_SORT', 1024, 768)
        cv2.resizeWindow('YOLO4_Deep_SORT', w, h)
        cv2.imshow('YOLO4_Deep_SORT', new_frame)

        # Press Q to stop!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # exit system
    if writeVideo_flag:
        out.release()

    cv2.destroyAllWindows()
    video_capture.release()


def test():
    # 初始化
    day = 1  # 游戏轮次
    game = gamelogic.Game()  # 游戏逻辑
    # 检测模块
    # GUI
    # Audio
    # 初始化成功

    # 配置游戏
    game.start_game(num_players=4)  # 开始游戏
    # 测试
    # print(game.get_id_list())
    # print(game.get_character_list())
    # print(game.get_status_list())

    # 赋予角色

    """
    准备进入夜晚
    """

    """
    如果第一晚,执行赋予角色
    """

    """
    夜晚行动
    """

    # 游戏逻辑
    game.movement_werewolf(day, 1)
    game.movement_seer(2)
    game.movement_witch(day, 3, 1)
    print(game.announce_night(day))
    print(game.get_status_list())
    print(game.progress)
    print(game.is_gameover(game.get_character_list()))

    # 夜晚结束

    """
    进入白天
    """
    # 宣布死讯


if __name__ == '__main__':
    # detector init
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    # session = InteractiveSession(config=config)
    # session = Session(config=config)

    # threading
    import threading
    t1 = threading.Thread(target=detectandprocess, args=(YOLOall(),))


    def threadfun(t):  # 线程任务函数 threadfun()
        while True:
            t += 1
            time.sleep(1)
            print(t)


    t2 = threading.Thread(target=threadfun, args=(1,))
    t1.start()
    t2.start()
