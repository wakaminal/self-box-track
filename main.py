from __future__ import print_function
import sys
import cv2
from random import randint
import time
import os
# opencv中自带了8个目标跟踪的算法
trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
# BOOSTING：算法原理类似于Haar cascades (AdaBoost)，是一种很老的算法。这个算法速度慢并且不是很准
# MIL：比BOOSTING准一点
# KCF：速度比BOOSTING和MIL更快，与BOOSTING和MIL一样不能很好地处理遮挡问题
# TLD：会产生较多的false-positives
# MedianFlow：对于快速移动的目标和外形变化迅速的目标效果不好
# MOSSE：算法速度非常快，但是准确率比不上KCF和CSRT。在一些追求算法速度的场合很适用
# CSRT：比KCF更准一些，但是速度比KCF稍慢


def createTrackerByName(trackerType):  # 追踪算法类型
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)

    return tracker


No = 0
if __name__ == '__main__':

    vecPoints = []

    while True:

        vecPoints.clear()

        # 选择追踪算法
        while True:
            print('\n------------------------------------------------------------------\n'
                  '\n>> 可测试算法有  BOOSTING  MIL  KCF  TLD  MEDIANFLOW  MOSSE  CSRT'
                  '\n>> 请输入要测试的算法并按回车，如需退出请输入exit。')

            tType = input('>> ')

            if tType == 'exit':
                sys.exit(0)  # sys.exit()程序直接提出，不显示异常  sys.exit(arg)捕捉异常，可以打印异常消息等
            if tType == 'BOOSTING':
                print('>> 选择BOOSTING成功！')
                break
            elif tType == 'MIL':
                print('>> 选择MIL成功！')
                break
            elif tType == 'KCF':
                print('>> 选择KCF成功！')
                break
            elif tType == 'TLD':
                print('>> 选择TLD成功！')
                break
            elif tType == 'MEDIANFLOW':
                print('>> 选择MEDIANFLOW成功！')
                break
            elif tType == 'MOSSE':
                print('>> 选择MOSSE成功！')
                break
            elif tType == 'CSRT':
                print('>> 选择CSRT成功！')
                break
            else:
                print('>> 选择失败!')
                continue

        print('>> 输入1选择本地视频进行播放'
              '\n>> 输入2选择实时摄像头播放')

        judgement = input('>> ')

        if judgement == '1':
            while True:
                print('\n+----------------+'
                      '\n|  1.步行的人_1  |'
                      '\n|  2.步行的人_2  |'
                      '\n|  3.步行的人_3  |'
                      '\n|  4.车          |'
                      '\n|  5.超车        |'
                      '\n|  6.大卫        |'
                      '\n|  7.跳绳        |'
                      '\n|  8.摩托越野    |'
                      '\n|  9.熊猫        |'
                      '\n|  10.大众汽车   |'
                      '\n+----------------+'
                      '\n\n>> 请输入要播放视频的序列号（例如4）')

                videoNo = input('>> ')

                if videoNo == '1':
                    videoName = 'pedestrian1.mpg'
                    print('>> 选择《步行的人_1》成功！')
                    break
                elif videoNo == '2':
                    videoName = 'pedestrian2.mpg'
                    print('>> 选择《步行的人_2》成功！')
                    break
                elif videoNo == '3':
                    videoName = 'pedestrian3.mpg'
                    print('>> 选择《步行的人_3》成功！')
                    break
                elif videoNo == '4':
                    videoName = 'car.mpg'
                    print('>> 选择《车》成功！')
                    break
                elif videoNo == '5':
                    videoName = 'carchase.mpg'
                    print('>> 选择《超车》成功！')
                    break
                elif videoNo == '6':
                    videoName = 'david.mpg'
                    print('>> 选择《大卫》成功！')
                    break
                elif videoNo == '7':
                    videoName = 'jumping.mpg'
                    print('>> 选择《跳绳》成功！')
                    break
                elif videoNo == '8':
                    videoName = 'motocross.mpg'
                    print('>> 选择《摩托越野》成功！')
                    break
                elif videoNo == '9':
                    videoName = 'panda.mpg'
                    print('>> 选择《熊猫》成功！')
                    break
                elif videoNo == '10':
                    videoName = 'volkswagen.mpg'
                    print('>> 选择《大众汽车》成功！')
                    break
                else:
                    print('>> 序列号有误，请重新输入！')
                    continue

            video = cv2.VideoCapture('.\\datasets\\' + videoName)

            if not video.isOpened():
                print('>> 读取视频失败')
                continue

            print('\n+--------------------------+'
                  '\n|  点击 c 逐帧播放视频     |'
                  '\n|  点击 q 开始选择目标     |'
                  '\n|  点击空格开始播放并跟踪  |'
                  '\n|  播放期间按 q 退出播放   |'
                  '\n+--------------------------+\n')
            # time.strftime(format[, t])：接收以时间元组，并返回以可读字符串表示的当地时间，格式由参数format决定
            # format：格式字符串  t：可选的参数t是一个struct_time对象  返回：以可读字符串表示的当地时间
            # %Y：四位数的年份表示（000-9999） %m：月份（01-12） %d：月内中的一天（0-31）%H：24小时制小时数（0-23）%M：分钟数（00=59）%S：秒（00-59）
            # 如果不提供t，使用localtime() 函数返回的当前时间。格式必须是字符串。如果t的任何字段在允许的范围之外，那么异常ValueError将会被引发。
            time_t = time.strftime('%Y.%m.%d %H-%M-%S', time.localtime(time.time()))
            outDir = 'E:\\targetTracking\\pyMultiTracker\\saveVideo\\Video-' + time_t
            os.mkdir(outDir)  # os.mkdir(path)创建一级目录  os.rmdir(path)删除目录  os.removdirs(path)删除多级目录 os.remove(path)删除文件
            outFile_1 = outDir + '\\videoNoTrack.avi'
            outFile_2 = outDir + '\\videoWithTrack.avi'

            # video.get(cv2.CAP_PROP_FRAME_WIDTH)：获得视频每帧的宽度
            # video.get(cv2.CAP_PROP_FRAME_HEIGHT)：获得视频每帧的高度
            # video.get(cv2.CAP_PROP_FPS)：获得录制视频的帧速率
            s = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            r = video.get(cv2.CAP_PROP_FPS)
            # VideoWriter(filename, fourcc, fps, frameSize[, isColor]) -> < VideoWriter object >
            # fourcc：指定编码器  fps：要保存的视频的帧率 frameSize：要保存的文件的画面尺寸  isColor：是黑白画面还是彩色的画面
            write_1 = cv2.VideoWriter(outFile_1, 0, r, s, True)
            write_2 = cv2.VideoWriter(outFile_2, 0, r, s, True)

            success, frame = video.read()

            if not success:
                print('>> 读取视频失败')
                continue

            cv2.imshow('Tracker', frame)
            while True:
                # cv2.waitKey(parameter)控制imshow()图像的持续时间，parameter=NONE&0：一直显示，除此之外持续显示的毫秒数
                # 但若在该时间内按任意键，程序将继续，获取键盘输入的值
                key = cv2.waitKey(1)
                if key == ord('c') or key == ord('C'):  # ord('c')返回c的ASCII码
                    success, frame = video.read()
                    cv2.imshow('Tracker', frame)
                    write_1.write(frame)
                    write_2.write(frame)
                if key == ord('q') or key == ord('Q'):
                    break
            # cv.destroyWindow(winname)：关闭winname指定的窗口
            cv2.destroyWindow('Tracker')

            bboxes = []
            colors = []

            while True:
                # draw bounding boxes over objects
                # selectROI's default behaviour is to draw box starting from the center
                # when fromCenter is set to false, you can draw box starting from top left corner

                # cv2.selectROI(windowName, img, showCrosshair=None, fromCenter=None):通过鼠标选取感兴趣的矩形区域
                # showCrosshair:是否在矩形里画十字线   fromCenter：是否从矩形框的中心开始画
                # 返回元组[min_x,min_y,w,h] min_x：矩形框中最小的x值
                bbox = cv2.selectROI('Tracker', frame)  # 选定ROI
                bboxes.append(bbox)
                # randint（n,m)产生的是一个n*m维的矩阵，矩阵的元素或者是0或者是1，是随机的。
                # 如果想产生一个范围的数，可以设置一个区间，randint(2,3,[1 6])，就是产生一个2*3随机矩阵，这个矩阵的元素是区间[1 6]的随机数。
                colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))  # 选定一个ROI，就扩展一种颜色
                print("Press q to quit selecting boxes and start tracking")
                print("Press any other key to select next object")
                k = cv2.waitKey(0) & 0xFF
                if (k == 113):  # q is pressed
                    break

            # print('Selected bounding boxes {}'.format(bboxes))

            # Create MultiTracker object
            # cv2.MultiTracker_create() 创建多对象追踪器
            multiTracker = cv2.MultiTracker_create()

            # Initialize MultiTracker
            for bbox in bboxes:
                # multiTracker需要两个输入：初始视频帧/通过边界框确定的对象位置
                multiTracker.add(createTrackerByName(tType), frame, bbox)
                temp = []
                vecPoints.append(temp)

            print('>> 开始播放')

            # Process video and track objects
            while video.isOpened():
                success, frame = video.read()
                if not success:
                    break

                write_1.write(frame)
                # write_2.write(frame)

                # get updated location of objects in subsequent frames
                success, boxes = multiTracker.update(frame)

                # draw tracked objects
                # 将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
                for i, newbox in enumerate(boxes):
                    p1 = (int(newbox[0]), int(newbox[1]))  # p1=(x_min,y_min)
                    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))  # p2(x_max,y_max)
                    # cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) → None
                    # pt1:矩形顶点  pt2：与pt1相对的矩形的顶点  即矩形的对角顶点
                    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

                for i, newbox in enumerate(boxes):  # 储存矩形中心点
                    vecPoints[i].append(
                        (int(newbox[0] + (newbox[2] * 0.5)) * 2, int(newbox[1] + (newbox[3] * 0.5)) * 2))

                if len(vecPoints) > 0:  # 把各矩形中心点连成轨迹
                    for i in range(len(vecPoints)):
                        for j in range(len(vecPoints[i]) - 1):
                            cv2.line(frame, vecPoints[i][j], vecPoints[i][j + 1], colors[i], 1, 8, 1)

                for i, newbox in enumerate(boxes):  # 添加文字
                    # cv2.putText(image, text, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    # text:要添加的文字  (5，50):要添加的位置  cv2.FONT_HERSHEY_SIMPLEX:字体类型  0.75:字体大小
                    # (0,0,255):字体颜色   2：字体粗细
                    cv2.putText(frame, 'id_' + str(i + 1), (int(newbox[0]), int(newbox[1]) - 3), cv2.FONT_HERSHEY_PLAIN,
                                1, colors[i], 1)

                # show frame
                cv2.imshow('Tracker', frame)

                # write_1.write(frame)
                write_2.write(frame)

                # quit on ESC button
                if cv2.waitKey(30) == ord('q') or cv2.waitKey(30) == ord('Q'):
                    break

            write_1.release()
            write_2.release()
            print('\n>> 视频保存完毕。')
            cv2.destroyWindow('Tracker')
            print('>> 播放完毕')

        elif judgement == '2':

            video = cv2.VideoCapture(0)

            if not video.isOpened():
                print('>> 发生错误，请检查摄像头是否已断开！')
                continue

            time_t = time.strftime('%Y.%m.%d %H-%M-%S', time.localtime(time.time()))
            outDir = 'E:\\targetTracking\\pyMultiTracker\\saveVideo\\Camera-' + time_t
            os.mkdir(outDir)
            outFile_1 = outDir + '\\videoNoTrack.avi'
            outFile_2 = outDir + '\\videoWithTrack.avi'

            s = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            r = video.get(cv2.CAP_PROP_FPS)

            write_1 = cv2.VideoWriter(outFile_1, 0, r, s, True)
            write_2 = cv2.VideoWriter(outFile_2, 0, r, s, True)
            # print(outDir)

            print('>> 请按空格开始截取图片')

            while True:
                success, frame = video.read()
                if not success:
                    print('>> 发生错误，请检查摄像头是否已断开！')
                    break

                cv2.imshow('Tracker', frame)

                write_1.write(frame)
                write_2.write(frame)

                # cv2.imwrite('E:\\targetTracking\\pyMultiTracker\\saveVideo\\pic\\' + str(No) + '.bmp', frame)
                # No = No + 1

                if cv2.waitKey(1) == ord(' '):
                    break

            bboxes = []
            colors = []

            while True:  # 选择感兴趣区域
                # draw bounding boxes over objects
                # selectROI's default behaviour is to draw box starting from the center
                # when fromCenter is set to false, you can draw box starting from top left corner
                bbox = cv2.selectROI('Tracker', frame)
                bboxes.append(bbox)
                colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
                print("Press q to quit selecting boxes and start tracking")
                print("Press any other key to select next object")
                k = cv2.waitKey(0) & 0xFF
                if (k == 113):  # q is pressed
                    break

            # print('Selected bounding boxes {}'.format(bboxes))

            # Create MultiTracker object
            multiTracker = cv2.MultiTracker_create()

            # Initialize MultiTracker
            for bbox in bboxes:
                multiTracker.add(createTrackerByName(tType), frame, bbox)
                temp = []
                vecPoints.append(temp)

            print('>> 开始播放')

            # Process video and track objects
            while video.isOpened():
                success, frame = video.read()
                if not success:
                    break

                write_1.write(frame)
                # write_1.write(frame)
                # write_2.write(frame)
                print('before-' + str(id(frame)))

                # get updated location of objects in subsequent frames
                success, boxes = multiTracker.update(frame)

                # draw tracked objects
                for i, newbox in enumerate(boxes):
                    p1 = (int(newbox[0]), int(newbox[1]))
                    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

                for i, newbox in enumerate(boxes):
                    vecPoints[i].append(
                        (int(newbox[0] + (newbox[2] * 0.5)) * 2, int(newbox[1] + (newbox[3] * 0.5)) * 2))

                if len(vecPoints) > 0:
                    for i in range(len(vecPoints)):
                        for j in range(len(vecPoints[i]) - 1):
                            cv2.line(frame, vecPoints[i][j], vecPoints[i][j + 1], colors[i], 1, 8, 1)

                for i, newbox in enumerate(boxes):
                    cv2.putText(frame, 'id_' + str(i + 1), (int(newbox[0]), int(newbox[1]) - 3), cv2.FONT_HERSHEY_PLAIN,
                                1, colors[i], 1)

                # show frame
                cv2.imshow('Tracker', frame)

                # write_1.write(frame)
                write_2.write(frame)
                # write_2.write(frame)
                print('after-' + str(id(frame)))

                # cv2.imwrite('E:\\targetTracking\\pyMultiTracker\\saveVideo\\pic\\' + str(No) + '.bmp', frame)
                # No = No + 1

                # quit on ESC button
                if cv2.waitKey(30) == ord('q') or cv2.waitKey(30) == ord('Q'):
                    break

            write_1.release()
            write_2.release()
            print('\n>> 视频保存完毕。')
            cv2.destroyWindow('Tracker')
            print('\n>> 播放完毕\n')

        else:
            print('>> 输入有误')

    sys.exit(1)
