# # import sys
# #
# # print(type(sys.maxsize))
#
# # import tensorflow as tf
# # tf.test.is_gpu_available()
#
# import operator
#
# # 查看摄像头
# # import cv2
# #
# # video_capture = cv2.VideoCapture(1)
#
#
# # arrange
# # persons = [[] for _ in range(1)]
# # print(persons)
# # label = [0.1,0.2]
# # x = [[0.1,[304, 160, 54, 18]], [0.2,[369, 208, 44, 120]], [0.3,[255, 211, 43, 114]]]
# # x = x[:10]
# # for i in range(len(x)):
# #     if x[i][0] in label:
# #         persons[i] = x[i][1]
# # print(persons)
#
# # print(x)
# # x.sort(key=lambda x : x[0], reverse=True)  # 对嵌套列表第0维从大到小排序
# #
# # print(x)
# # x= x[:2]
# # print(x)
# # print('person' in ['person', 'thumbs-up'])
#
# import sys
#
# hand_labels = ['thumbs-up', 'thumbs-down', 'one', 'two', 'three', 'four', 'five']
# eye_labels = ['openeye', 'closeeye']
#
#
# def xywh2xyxy(boxs):
#     """
#     将嵌套列表的bounding box list 从xywh format 改成 xyxy format
#     :param boxs: [[xywh],[],[]]
#     :return: [[xyxy],[],[]]
#     """
#     xyxy = []
#     for i in range(len(boxs)):
#         temp = [0] * 4
#         temp[0] = int(boxs[i][0])
#         temp[1] = int(boxs[i][1])
#         temp[2] = int(boxs[i][2] + boxs[i][0])
#         temp[3] = int(boxs[i][3] + boxs[i][1])
#         xyxy.append(temp)
#     return xyxy
#
#
# def xyxy2center_point(xyxy):
#     """
#     :param xyxy: [x_topleft, y_topleft, x_bottomright,y_bottomright]
#     :return: [x_center, y_center]
#     """
#     return [(xyxy[0] + xyxy[2]) // 2, (xyxy[1] + xyxy[3]) // 2]
#
#
# def manhattan_distance(xy1, xy2):
#     """
#
#     :param xy1:
#     :param xy2:
#     :return: xy1和xy2的曼哈顿距离
#     """
#     return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
#
#
# class Processor(object):
#     def __init__(self, num_player_indevice, voting_fps):
#         self.num_player_indevice = num_player_indevice  # 设备限制人数
#         self.hand_constraint = 2  # 每个人有两只手
#         self.eye_constraint = 1  # 每个人有一双眼睛
#         self.persons = [[259, 278], [517, 263]]  # 从左到右的person边界框中心点坐标
#         # self.persons = [[259, 278]]
#         self.id_status_deque = {}  # 稳定器
#         self.id_status_voting = {}  # 稳定输出
#         # deque初始化
#         for i in range(1, num_player_indevice + 1):
#             pass
#
#     def assign_object2person(self, boxs, conf, cls):
#         # 存储 hand/eye: [[cls,conf,[center_point]],[],[]]
#         hand_list = []
#         eye_list = []
#         # 按照personid-1 存储hand,eye结果
#         final_handlist = [[] for _ in range(self.num_player_indevice)]
#         final_eyelist = [[] for _ in range(self.num_player_indevice)]
#         for i in range(len(cls)):
#             if cls[i] in hand_labels:
#                 hand_list.append([cls[i], conf[i], xyxy2center_point(boxs[i])])
#             elif cls[i] in eye_labels:
#                 eye_list.append([cls[i], conf[i], xyxy2center_point(boxs[i])])
#
#         # 测试输出
#         print('hand:', hand_list)
#         print('eye:', eye_list)
#
#         # 关联hand
#         try:
#             for i in range(len(hand_list)):
#                 shortest = sys.maxsize
#                 index_shortest = None
#                 for j in range(len(self.persons)):
#                     distance = manhattan_distance(hand_list[i][2], self.persons[j])
#                     if distance < shortest:
#                         index_shortest = j
#                         shortest = distance
#                 final_handlist[index_shortest].append(hand_list[i])
#         except:
#             print('没有person可以和hand posture关联')
#
#         # 关联eye
#         try:
#             for i in range(len(eye_list)):
#                 shortest = sys.maxsize
#                 index_shortest = None
#                 for j in range(len(self.persons)):
#                     distance = manhattan_distance(eye_list[i][2], self.persons[j])
#                     if distance < shortest:
#                         index_shortest = j
#                         shortest = distance
#                 final_eyelist[index_shortest].append(eye_list[i])
#         except:
#             print('没有person可以和eye关联')
#
#         print(final_handlist)
#         print(final_eyelist)
#         # 去重
#         try:
#             for i in range(len(final_handlist)):
#                 if len(final_handlist[i]) > self.hand_constraint:
#                     final_handlist[i].sort(key=lambda x: x[1], reverse=True)  # 对嵌套列表cof维度从大到小排序
#                     final_handlist[i] = final_handlist[i][:self.hand_constraint]
#             for i in range(len(final_eyelist)):
#                 if len(final_eyelist[i]) > self.eye_constraint:
#                     final_eyelist[i].sort(key=lambda x: x[1], reverse=True)  # 对嵌套列表cof维度从大到小排序
#                     final_eyelist[i] = final_eyelist[i][:self.eye_constraint]
#         except:
#             print('processor: 去重失败')
#
#         print(final_handlist)
#         print(final_eyelist)
#
#
# process = Processor(2, 10)
# 'thumbs-up', 0.94362426, [562, 287]
# box = [[261, 151, 304, 163], [481, 91, 537, 110], [435, 78, 600, 448], [190, 98, 329, 459], [315, 180, 347, 219],
#        [543, 243, 582, 331], [461, 258, 502, 336]]
# conf = [0.7580769, 0.78516906, 0.9438776, 0.97876006, 0.8106501, 0.94362426, 0.9789412]
# cls = ['closeeye', 'openeye', 'person', 'person', 'thumbs-up', 'thumbs-up', 'thumbs-up']
# print(box, conf, cls)
#
# process.assign_object2person(box, conf, cls)
