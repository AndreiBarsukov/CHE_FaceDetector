
# Импорт необходимых модулей
import math
from imutils.video import VideoStream, FPS
import cv2
import numpy as np
import dlib
import json
import socket
from math import pi, radians, sin, sqrt, acos, degrees
	
import time
import asyncio


import os

rootDir = os.path.dirname(os.path.abspath(__file__))



class FaceShapeController:
    # # Ключевые точки DLIB
    # # Номера ключевых точек для определения смещений
    # __bottomJawPoint = (8, 30) 
    # __mouthCornerLeftPoint = (54, 30)
    # __mouthCornerRightPoint = (48, 30)
    # __browLeftPoint = (24, 30)
    # __browRightPoint = (19, 30)
    # __eyeBlinkLeftPoint = (43, 47)
    # __eyeBlinkRightPoint = (38, 40)
    
    # __rotateHeadXPoint = (8, 33, 27)    # Наклоны головы вперед/назад
    # __rotateHeadYPoint = (2, 33, 14)    # Поворот головы влево/вправо
    # __rotateHeadZPoint = (27,33)        # Поворот головы влево/вправо

    # Ключевые точки MEDIAPIPE
    # Номера ключевых точек для определения смещений
    __bottomJawPoint = (11, 16) 
    __mouthCornerLeftPoint = (291, 18)
    __mouthCornerRightPoint = (61, 18)
    __browLeftPoint = (334, 1)
    __browRightPoint = (105, 1)
    __eyeBlinkLeftPoint = (386, 374)
    __eyeBlinkRightPoint = (159, 145)
    
    __rotateHeadXPoint = (2, 1, 27)    # Наклоны головы вперед/назад
    __rotateHeadYPoint = (123, 1, 14)    # Поворот головы влево/вправо
    __rotateHeadZPoint = (164,10)        # Поворот головы влево/вправо

    __init_value = np.float64(0.0)
    __bottomJawNormalOffset = {"X": __init_value, "Y":__init_value}
    __bottomJawOffset = {"X": __init_value, "Y":__init_value}

    __mouthCornerLeftNormalOffset = {"X": __init_value, "Y":__init_value}
    __mouthCornerLeftOffset = {"X": __init_value, "Y":__init_value}

    __mouthCornerRightNormalOffset = {"X": __init_value, "Y":__init_value}
    __mouthCornerRightOffset = {"X": __init_value, "Y":__init_value}

    __browLeftNormalOffset = {"X": __init_value, "Y":__init_value}
    __browLeftOffset = {"X": __init_value, "Y":__init_value}

    __browRightNormalOffset = {"X": __init_value, "Y":__init_value}
    __browRightOffset = {"X": __init_value, "Y":__init_value}

    __eyeBlinkLeftNormalOffset = {"X": __init_value, "Y":__init_value}
    __eyeBlinkLeftOffset = {"X": __init_value, "Y":__init_value}

    __eyeBlinkRightNormalOffset = {"X": __init_value, "Y":__init_value}
    __eyeBlinkRightOffset = {"X": __init_value, "Y":__init_value}

    __rotateHeadXPointNormalOffset = {"X": __init_value, "Y":__init_value}
    __rotateHeadXPointOffset = {"X": __init_value, "Y":__init_value}

    __rotateHeadYPointNormalOffset = {"X": __init_value, "Y":__init_value}
    __rotateHeadYPointOffset = {"X": __init_value, "Y":__init_value}

    __rotateHeadZPointNormalOffset = {"point1": {"X": __init_value, "Y":__init_value}, "point2": {"X": __init_value, "Y":__init_value}}
    __rotateHeadZPointOffset = {"X": __init_value, "Y":__init_value}

    
    # Функции для вычисления угла между двумя прямыми
    def __scalar(self, x1, y1, x2, y2):
        return x1*x2 + y1*y2
    def __module(self, x, y):
        return sqrt(x ** 2 + y ** 2)
    def __GetDistanceBtwPoints(self, point1, point2):
        return math.sqrt((point2["X"] - point1["X"])^2 + (point2["Y"] - point1["Y"])^2)

    def RescaleOffset(self, current, min, max):
        return np.float64(current - min) / np.float64(max - min)

    def InitNormalOffset(self, points):
        # print(points)
        self.__bottomJawNormalOffset = {"X": points[self.__bottomJawPoint[0]]["X"] - points[self.__bottomJawPoint[1]]["X"], 
                                        "Y": points[self.__bottomJawPoint[0]]["Y"] - points[self.__bottomJawPoint[1]]["Y"]}

        self.__mouthCornerLeftNormalOffset = {"X": points[self.__mouthCornerLeftPoint[0]]["X"] - points[self.__mouthCornerLeftPoint[1]]["X"], 
                                              "Y": points[self.__mouthCornerLeftPoint[0]]["Y"] - points[self.__mouthCornerLeftPoint[1]]["Y"]}
        self.__mouthCornerRightNormalOffset =   {"X": points[self.__mouthCornerRightPoint[1]]["X"] - points[self.__mouthCornerRightPoint[0]]["X"], 
                                                 "Y": points[self.__mouthCornerRightPoint[0]]["Y"] - points[self.__mouthCornerRightPoint[1]]["Y"]}

        self.__browLeftNormalOffset = {"X": points[self.__browLeftPoint[0]]["X"] - points[self.__browLeftPoint[1]]["X"], 
                                       "Y": points[self.__browLeftPoint[0]]["Y"] - points[self.__browLeftPoint[1]]["Y"]}
        self.__browRightNormalOffset = {"X": points[self.__browRightPoint[1]]["X"] - points[self.__browRightPoint[0]]["X"], 
                                        "Y": points[self.__browRightPoint[0]]["Y"] - points[self.__browRightPoint[1]]["Y"]}

        self.__eyeBlinkLeftNormalOffset = {"X": points[self.__eyeBlinkLeftPoint[0]]["X"] - points[self.__eyeBlinkLeftPoint[1]]["X"], 
                                           "Y": points[self.__eyeBlinkLeftPoint[0]]["Y"] - points[self.__eyeBlinkLeftPoint[1]]["Y"]}

        self.__eyeBlinkRightNormalOffset = {"X": points[self.__eyeBlinkRightPoint[1]]["X"] - points[self.__eyeBlinkRightPoint[0]]["X"], 
                                            "Y": points[self.__eyeBlinkRightPoint[0]]["Y"] - points[self.__eyeBlinkRightPoint[1]]["Y"]}


        self.__rotateHeadXPointNormalOffset = {"X": points[self.__rotateHeadXPoint[0]]["X"] - points[self.__rotateHeadXPoint[1]]["X"], 
                                               "Y": points[self.__rotateHeadXPoint[0]]["Y"] - points[self.__rotateHeadXPoint[1]]["Y"]}
        self.__rotateHeadYPointNormalOffset = {"X": points[self.__rotateHeadYPoint[0]]["X"] - points[self.__rotateHeadYPoint[1]]["X"], 
                                               "Y": points[self.__rotateHeadYPoint[0]]["Y"] - points[self.__rotateHeadYPoint[1]]["Y"]}
        self.__rotateHeadZPointNormalOffset = {"point1": points[self.__rotateHeadZPoint[0]], 
                                               "point2": points[self.__rotateHeadZPoint[1]]}

    def SetBottomJawOffset(self, points):
        self.__bottomJawOffset = {"X": points[self.__bottomJawPoint[0]]["X"] - points[self.__bottomJawPoint[1]]["X"], 
                                  "Y": points[self.__bottomJawPoint[0]]["Y"] - points[self.__bottomJawPoint[1]]["Y"]}

    def GetBottomJawPosition(self, points):
        diff = {"X": points[self.__bottomJawPoint[0]]["X"] - points[self.__bottomJawPoint[1]]["X"], 
                "Y": points[self.__bottomJawPoint[0]]["Y"] - points[self.__bottomJawPoint[1]]["Y"]}
        resultX =  self.RescaleOffset(diff["X"], self.__bottomJawNormalOffset["X"], self.__bottomJawOffset["X"])
        # (diff["X"] - self.__bottomJawNormalOffset["X"]) / np.float64(self.__bottomJawOffset["X"] - self.__bottomJawNormalOffset["X"])
        resultY = self.RescaleOffset(diff["Y"], self.__bottomJawNormalOffset["Y"], self.__bottomJawOffset["Y"])
        (diff["Y"] - self.__bottomJawNormalOffset["Y"]) / np.float64(self.__bottomJawOffset["Y"] - self.__bottomJawNormalOffset["Y"])

        # print(resultX)
        # print("------------")

        if resultX == np.inf:
            resultX = 0
        if resultY == np.inf:
            resultY = 0

        resultX = self.ClampNegPos(resultX)
        resultY = self.ClampNegPos(resultY)

        return {"X": resultX, "Y": resultY}

    def SetSmileOffset(self, points):
        self.__mouthCornerLeftOffset = {"X": points[self.__mouthCornerLeftPoint[0]]["X"] - points[self.__mouthCornerLeftPoint[1]]["X"], 
                                        "Y": points[self.__mouthCornerLeftPoint[0]]["Y"] - points[self.__mouthCornerLeftPoint[1]]["Y"]}
        self.__mouthCornerRightOffset = {"X": points[self.__mouthCornerRightPoint[1]]["X"] - points[self.__mouthCornerRightPoint[0]]["X"], 
                                         "Y": points[self.__mouthCornerRightPoint[0]]["Y"] - points[self.__mouthCornerRightPoint[1]]["Y"]}

    def GetMouthCornerLeftPosition(self, points):
        diff = {"X": points[self.__mouthCornerLeftPoint[0]]["X"] - points[self.__mouthCornerLeftPoint[1]]["X"], 
                "Y": points[self.__mouthCornerLeftPoint[0]]["Y"] - points[self.__mouthCornerLeftPoint[1]]["Y"]}
        resultX = (diff["X"] - self.__mouthCornerLeftNormalOffset["X"]) / np.float64(self.__mouthCornerLeftOffset["X"] - self.__mouthCornerLeftNormalOffset["X"])
        resultY = (diff["Y"] - self.__mouthCornerLeftNormalOffset["Y"]) / np.float64(self.__mouthCornerLeftOffset["Y"] - self.__mouthCornerLeftNormalOffset["Y"])

        if resultX == np.inf:
            resultX = 0
        if resultY == np.inf:
            resultY = 0

        resultX = self.ClampNegPos(resultX)
        resultY = self.ClampNegPos(resultY)

        return {"X": resultX, "Y": resultY}

    def GetMouthCornerRightPosition(self, points):
        diff = {"X": points[self.__mouthCornerRightPoint[1]]["X"] - points[self.__mouthCornerRightPoint[0]]["X"], 
                "Y": points[self.__mouthCornerRightPoint[0]]["Y"] - points[self.__mouthCornerRightPoint[1]]["Y"]}
        resultX = (diff["X"] - self.__mouthCornerRightNormalOffset["X"]) / np.float64(self.__mouthCornerRightOffset["X"] - self.__mouthCornerRightNormalOffset["X"])
        resultY = (diff["Y"] - self.__mouthCornerRightNormalOffset["Y"]) / np.float64(self.__mouthCornerRightOffset["Y"] - self.__mouthCornerRightNormalOffset["Y"])

        if resultX == np.inf:
            resultX = 0
        if resultY == np.inf:
            resultY = 0

        resultX = self.ClampNegPos(resultX)
        resultY = self.ClampNegPos(resultY)

        return {"X": resultX, "Y": resultY}

    def SetBrowUpOffset(self, points):
        self.__browLeftOffset =     {"X": points[self.__browLeftPoint[0]]["X"] - points[self.__browLeftPoint[1]]["X"], 
                                 "Y": points[self.__browLeftPoint[0]]["Y"] - points[self.__browLeftPoint[1]]["Y"]}
        self.__browRightOffset = {"X": points[self.__browRightPoint[1]]["X"] - points[self.__browRightPoint[0]]["X"], 
                                  "Y": points[self.__browRightPoint[0]]["Y"] - points[self.__browRightPoint[1]]["Y"]}

    def GetBrowLeftPosition(self, points):
        diff = {"X": points[self.__browLeftPoint[0]]["X"] - points[self.__browLeftPoint[1]]["X"], 
                "Y": points[self.__browLeftPoint[0]]["Y"] - points[self.__browLeftPoint[1]]["Y"]}
        resultX = (diff["X"] - self.__browLeftNormalOffset["X"]) / np.float64(self.__browLeftOffset["X"] - self.__browLeftNormalOffset["X"])
        resultY = (diff["Y"] - self.__browLeftNormalOffset["Y"]) / np.float64(self.__browLeftOffset["Y"] - self.__browLeftNormalOffset["Y"])

        if resultX == np.inf:
            resultX = 0
        if resultY == np.inf:
            resultY = 0

        resultX = self.ClampNegPos(resultX)
        resultY = self.ClampNegPos(resultY)

        return {"X": resultX, "Y": resultY}

    def GetBrowRightPosition(self, points):
        diff = {"X": points[self.__browRightPoint[1]]["X"] - points[self.__browRightPoint[0]]["X"], 
                "Y": points[self.__browRightPoint[0]]["Y"] - points[self.__browRightPoint[1]]["Y"]}
        resultX = (diff["X"] - self.__browRightNormalOffset["X"]) / np.float64(self.__browRightOffset["X"] - self.__browRightNormalOffset["X"])
        resultY = (diff["Y"] - self.__browRightNormalOffset["Y"]) / np.float64(self.__browRightOffset["Y"] - self.__browRightNormalOffset["Y"])

        if resultX == np.inf:
            resultX = 0
        if resultY == np.inf:
            resultY = 0

        resultX = self.ClampNegPos(resultX)
        resultY = self.ClampNegPos(resultY)

        return {"X": resultX, "Y": resultY}

    def SetEyeBlinkLeftOffset(self, points):
        self.__eyeBlinkLeftOffset = {"X": points[self.__eyeBlinkLeftPoint[0]]["X"] - points[self.__eyeBlinkLeftPoint[1]]["X"], 
                                     "Y": points[self.__eyeBlinkLeftPoint[0]]["Y"] - points[self.__eyeBlinkLeftPoint[1]]["Y"]}

    def SetEyeBlinkRightOffset(self, points):
        self.__eyeBlinkRightOffset = {"X": points[self.__eyeBlinkRightPoint[1]]["X"] - points[self.__eyeBlinkRightPoint[0]]["X"], 
                                      "Y": points[self.__eyeBlinkRightPoint[0]]["Y"] - points[self.__eyeBlinkRightPoint[1]]["Y"]}

    def GetEyeBlinkLeftPosition(self, points):
        diff = {"X": points[self.__eyeBlinkLeftPoint[0]]["X"] - points[self.__eyeBlinkLeftPoint[1]]["X"], 
                "Y": points[self.__eyeBlinkLeftPoint[0]]["Y"] - points[self.__eyeBlinkLeftPoint[1]]["Y"]}
        resultX = (diff["X"] - self.__eyeBlinkLeftNormalOffset["X"]) / np.float64(self.__eyeBlinkLeftOffset["X"] - self.__eyeBlinkLeftNormalOffset["X"])
        resultY = (diff["Y"] - self.__eyeBlinkLeftNormalOffset["Y"]) / np.float64(self.__eyeBlinkLeftOffset["Y"] - self.__eyeBlinkLeftNormalOffset["Y"])

        if resultX == np.inf:
            resultX = 0
        if resultY == np.inf:
            resultY = 0

        resultX = self.ClampNegPos(resultX)
        resultY = self.ClampNegPos(resultY)

        return {"X": resultX, "Y": resultY}

    def GetEyeBlinkRightPosition(self, points):
        diff = {"X": points[self.__eyeBlinkRightPoint[1]]["X"] - points[self.__eyeBlinkRightPoint[0]]["X"], 
                "Y": points[self.__eyeBlinkRightPoint[0]]["Y"] - points[self.__eyeBlinkRightPoint[1]]["Y"]}
        resultX = (diff["X"] - self.__eyeBlinkRightNormalOffset["X"]) / np.float64(self.__eyeBlinkRightOffset["X"] - self.__eyeBlinkRightNormalOffset["X"])
        resultY = (diff["Y"] - self.__eyeBlinkRightNormalOffset["Y"]) / np.float64(self.__eyeBlinkRightOffset["Y"] - self.__eyeBlinkRightNormalOffset["Y"])

        if resultX == np.inf:
            resultX = 0
        if resultY == np.inf:
            resultY = 0

        resultX = self.ClampNegPos(resultX)
        resultY = self.ClampNegPos(resultY)

        return {"X": resultX, "Y": resultY}




    def GetVectorPoints(self, point1, point2):
        return {"X": point1["X"] - point2["X"], "Y": point1["Y"] - point2["Y"]}        

    def SetRorateHeadX(self, points):
        pass
        self.__rotateHeadZPointOffset = {"X": points[self.__rotateHeadZPoint[1]]["X"] - points[self.__rotateHeadZPoint[0]]["X"], 
                                        "Y": points[self.__rotateHeadZPoint[1]]["Y"] - points[self.__rotateHeadZPoint[0]]["Y"]}
    def GetRorateHeadX(self, points):
        diff = {"X": points[self.__rotateHeadXPoint[0]]["X"] - points[self.__rotateHeadXPoint[1]]["X"], 
                "Y": points[self.__rotateHeadXPoint[0]]["Y"] - points[self.__rotateHeadXPoint[1]]["Y"]}
        resultX = (diff["X"] - self.__rotateHeadXPointNormalOffset["X"]) / np.float64(self.__rotateHeadXPointOffset["X"] - self.__rotateHeadXPointNormalOffset["X"])
        resultY = (diff["Y"] - self.__rotateHeadXPointNormalOffset["Y"]) / np.float64(self.__rotateHeadXPointOffset["Y"] - self.__rotateHeadXPointNormalOffset["Y"])
        if resultX == np.inf:
            resultX = 0
        if resultY == np.inf:
            resultY = 0
 
        resultX = self.ClampNegPos(resultX)
        resultY = self.ClampNegPos(resultY)
        
        return resultY * 10 / 0.15 * 1

    def SetRorateHeadY(self, points):
        self.__rotateHeadYPointOffset = {"X": points[self.__rotateHeadYPoint[1]]["X"] - points[self.__rotateHeadYPoint[0]]["X"], 
                                        "Y": points[self.__rotateHeadYPoint[1]]["Y"] - points[self.__rotateHeadYPoint[0]]["Y"]}
    def GetRorateHeadY(self, points):
        diff = {"X": points[self.__rotateHeadYPoint[0]]["X"] - points[self.__rotateHeadYPoint[1]]["X"], 
                "Y": points[self.__rotateHeadYPoint[0]]["Y"] - points[self.__rotateHeadYPoint[1]]["Y"]}
        resultX = (diff["X"] - self.__rotateHeadYPointNormalOffset["X"]) / np.float64(self.__rotateHeadYPointOffset["X"] - self.__rotateHeadYPointNormalOffset["X"])
        resultY = (diff["Y"] - self.__rotateHeadYPointNormalOffset["Y"]) / np.float64(self.__rotateHeadYPointOffset["Y"] - self.__rotateHeadYPointNormalOffset["Y"])

        if resultX == np.inf:
            resultX = 0
        if resultY == np.inf:
            resultY = 0

        resultX = self.ClampNegPos(resultX)
        resultY = self.ClampNegPos(resultY)
        # print({"X": resultX, "Y": resultY})
        return resultX * 60 / 0.6

    def SetRorateHeadZ(self, points):
        pass
        self.__rotateHeadXPointOffset = {"X": points[self.__rotateHeadZPoint[1]]["X"] - points[self.__rotateHeadZPoint[0]]["X"], 
                                        "Y": points[self.__rotateHeadZPoint[1]]["Y"] - points[self.__rotateHeadZPoint[0]]["Y"]}
    def GetRorateHeadZ(self, points):
        normalVector = self.GetVectorPoints(self.__rotateHeadZPointNormalOffset["point2"], self.__rotateHeadZPointNormalOffset["point1"])
        offsetVector = self.GetVectorPoints(points[self.__rotateHeadZPoint[1]], points[self.__rotateHeadZPoint[0]])
        if points[self.__rotateHeadZPoint[1]]["X"] - self.__rotateHeadZPointNormalOffset["point1"]["X"] >= 0:
            sign_ang = 1
        else:
            sign_ang = -1
        sc = self.__scalar(offsetVector["X"], offsetVector["Y"], normalVector["X"], normalVector["Y"])
        md = self.__module(offsetVector["X"], offsetVector["Y"]) * self.__module(normalVector["X"], normalVector["Y"])
        ang = abs(acos(round(sc/md, 3)) * 180 / pi ) * sign_ang
        # print(ang)
        # print((ang - 0)/(35 - 0))    
        # return ((ang - 0)/(35 - 0))
        return ang * 2



    def ClampNegPos(self, value):
        if value > 1.0:
            return 1.0
        elif value < -1.0:
            return -1.0
        else:
            return value
