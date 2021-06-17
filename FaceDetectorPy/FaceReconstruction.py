import cv2
import numpy as np
import dlib
import json
import socket
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt
import os
from FaceShapeController import FaceShapeController
from FaceDataModel import FaceDataModel
import cv2
import mediapipe as mp

rootDir = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow): 
    # ОБъект для расчета параметров лица
    faceController = FaceShapeController()
    # Индекс подключаемой камеры в строковом виде
    cameraIndexStr = "0"
    capture = cv2.VideoCapture(int(cameraIndexStr))
    # Ключевые точки лица
    points = {}
    # Параметры UDP
    UDP_ip = "127.0.0.1"
    UDP_port = 6868
    sendUDP = False
    # Подключение детектора, настроенного на поиск человеческих лиц
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
   
    mpDrawing = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh

   

    # Инициализация главного окна
    def __init__(self):

        QMainWindow.__init__(self)
        loadUi(rootDir + "\design.ui", self)

        self.setWindowTitle("FACE DETECTOR")
        self.btn_SwichSendVideo.setStyleSheet('background: rgb(0,150,50); color: rgb(255,255,255);')
        self.ButtonUIEnable(False)
        self.frameVideo.hide()

        self.btn_SwichSendUDP.clicked.connect(self.SwichSendUPD)
        self.btn_SwichSendVideo.clicked.connect(self.SwichSendVideo)

        self.btn_NormalizeFace.clicked.connect(self.NormalizeFace)
        self.btn_leftCloseEye.clicked.connect(self.LeftCloseEye)
        self.btn_rightCloseEye.clicked.connect(self.RightCloseEye)
        self.btn_browUp.clicked.connect(self.BrowUp)
        self.btn_lipsOpen.clicked.connect(self.LipsOpen)
        self.btn_smile.clicked.connect(self.Smile)

        self.btn_liftHead.clicked.connect(self.LiftHead)
        self.btn_turnHead.clicked.connect(self.TurnHead)
        self.btn_tiltHead.clicked.connect(self.TiltHead)
        self.btn_liftHead.hide()
        self.btn_turnHead.hide()
        self.btn_tiltHead.hide()

        self.btn_FaceReconstruction.clicked.connect(self.GetFaceReconstructionData)
    
    # Закрытие программы, отключение видеопотока
    def closeEvent(self, event):
        self.capture.release()
    
    # Вкл/выкл отправку пакетов
    def SwichSendUPD(self):
        if self.btn_SwichSendUDP.text() == "Отключить передачу данных":
            button_text = "Включить передачу данных"
            self.sendUDP = False
        else:
            button_text = "Отключить передачу данных"
            self.sendUDP = True
        self.btn_SwichSendUDP.setText(button_text) 

    # Вкл/выкл видеопоток
    def SwichSendVideo(self):
        if self.btn_SwichSendVideo.text() == "Отключить камеру":
            button_text = "Включить камеру"
            button_color = 'background: rgb(0,150,50); color: rgb(255,255,255);'
            self.timer.stop()
            self.capture.release()
            self.frameVideo.hide()
            self.ButtonUIEnable(False)
        else:
            button_text = "Отключить камеру"
            button_color = 'background: rgb(180,0,50); color: rgb(255,255,255);'
            self.startVideo(self.cameraIndexStr)
            self.frameVideo.show()
            self.ButtonUIEnable(True)
        self.btn_SwichSendVideo.setText(button_text) 
        self.btn_SwichSendVideo.setStyleSheet(button_color)

    # Изменение состояний кнопок интерфейса в зависимости от включения камеры
    def ButtonUIEnable(self, state):
        self.btn_SwichSendUDP.setEnabled(state)
        self.btn_NormalizeFace.setEnabled(state)
        self.btn_leftCloseEye.setEnabled(state)
        self.btn_rightCloseEye.setEnabled(state)
        self.btn_browUp.setEnabled(state)
        self.btn_lipsOpen.setEnabled(state)
        self.btn_smile.setEnabled(state)
        self.btn_liftHead.setEnabled(state)
        self.btn_turnHead.setEnabled(state)
        self.btn_tiltHead.setEnabled(state)
        self.btn_FaceReconstruction.setEnabled(state)
        self.resize(350, 230)

    # Установка положений лица
    def NormalizeFace(self):
        # self.index_iteration = 1
        self.faceController.InitNormalOffset(self.points)
    def LeftCloseEye(self):
        self.faceController.SetEyeBlinkLeftOffset(self.points)
    def RightCloseEye(self):
        self.faceController.SetEyeBlinkRightOffset(self.points)
    def BrowUp(self):
        self.faceController.SetBrowUpOffset(self.points)
    def LipsOpen(self):
        self.faceController.SetBottomJawOffset(self.points)
    def Smile(self):
        self.faceController.SetSmileOffset(self.points)
    
    def LiftHead(self):
        self.faceController.SetRorateHeadX(self.points)
        # self.faceController.SetBrowUpOffset(self.points)
    def TurnHead(self):
        self.faceController.SetRorateHeadY(self.points)
    def TiltHead(self):
        self.faceController.SetRorateHeadZ(self.points)

    # Формирвоание данных о мимике
    def GetFaceBlendShape(self):
        # Детекция открытого рта
        Mouth_Open = self.faceController.GetBottomJawPosition(self.points)["Y"]
        mouthTight = 0
        if Mouth_Open < 0:
            mouthTight = abs(Mouth_Open)
            Mouth_Open = 0
        # Детекция улыбки влево
        Mouth_Smile_Simple_Left = self.faceController.GetMouthCornerLeftPosition(self.points)["X"]
        Mouth_Dimple_Left = 0
        if Mouth_Smile_Simple_Left < 0:
            Mouth_Dimple_Left = abs(Mouth_Smile_Simple_Left)
            Mouth_Smile_Simple_Left = 0
        # Детекция улыбки вправо
        Mouth_Smile_Simple_Right = self.faceController.GetMouthCornerRightPosition(self.points)["X"]
        Mouth_Dimple_Right = 0
        if Mouth_Smile_Simple_Right < 0:
            Mouth_Dimple_Right = abs(Mouth_Smile_Simple_Right)
            Mouth_Smile_Simple_Right = 0
        # Детекция закрытого левого глаза
        Eyes_Closed_Left = self.faceController.GetEyeBlinkLeftPosition(self.points)["Y"]
        if Eyes_Closed_Left < 0.75:
            Eyes_Closed_Left = 0
        else:
            Eyes_Closed_Left = 1
        # Детекция закрытого правого глаза
        Eyes_Closed_Right = self.faceController.GetEyeBlinkRightPosition(self.points)["Y"]
        if Eyes_Closed_Right < 0.75:
            Eyes_Closed_Right = 0
        else:
            Eyes_Closed_Right = 1
        # Детекция поднятой левой брови
        Brow_Inner_UP__Down_Left = self.faceController.GetBrowLeftPosition(self.points)["Y"]
        # Детекция поднятой правой брови
        Brow_Inner_UP__Down_Right = self.faceController.GetBrowRightPosition(self.points)["Y"]
        local_variable = locals()

        # Объект для формирования расчитанных данных
        emotionDataModel = FaceDataModel()
        emotionDataModel.values["type"] = "emotionData"
        # Получаем все переменные в данной функции и выбираем только те, которые имеют числовое значение, чтобы заполнить модель данных
        local_variable = locals()
        for val in local_variable:
            if isinstance(local_variable[val], (int, float)):
                emotionDataModel.values[val] = str(local_variable[val])
        # Получаем модель данных
        valuesEmotionFace = emotionDataModel.GetDictData()
        # Преобразование модели данных в JSON
        json_data = json.dumps(valuesEmotionFace, indent=4, separators=(",",":"))
        # Отправка преобразованных данных по UDP
        self.SendUDP(json_data, self.UDP_ip, self.UDP_port)
        return json_data
    
    # Формирование данных о поворотах головы 
    def GetRotationHead(self):
        # Наклон головы вперед/назад, вращения головы, наклоны головы в стороны
        Neck_UpDown = self.faceController.GetRorateHeadX(self.points) 
        Neck_Rotation = self.faceController.GetRorateHeadY(self.points)
        Neck_Incline = self.faceController.GetRorateHeadZ(self.points)
        local_variable = locals()
        rotationHeadDataModel = FaceDataModel()
        rotationHeadDataModel.values["type"] = "rotationHeadData"
        # local_variable = locals()
        for val in local_variable:
            if isinstance(local_variable[val], (int, float)):
                rotationHeadDataModel.values[val] = str(local_variable[val])
        valuesRotationData = rotationHeadDataModel.GetDictData()
        # Преобразование модели данных в JSON
        json_data = json.dumps(valuesRotationData, indent=4, separators=(",",":"))
        # Отправка преобразованных данных по UDP
        self.SendUDP(json_data, self.UDP_ip, self.UDP_port)
   
    # Формирование данных трехмерной реконструкции
    def GetFaceReconstructionData(self):
        dataPoints = {}
        dataPoints = self.points
        dataPoints["type"] = "faceReconstructionData"
        json_data = json.dumps(self.points, indent=4, separators=(",",":"))
        self.SendUDP(json_data, self.UDP_ip, self.UDP_port)

    # Запуск видеопотока (на основе таймера)
    def startVideo(self, camera_name):
        """
        :param camera_name: link of camera or usb camera
        :return:
        """
        if len(camera_name) == 1:
        	self.capture = cv2.VideoCapture(int(camera_name))
        else:
        	self.capture = cv2.VideoCapture(camera_name)
        self.timer = QTimer(self)          
        path = 'ImagesAttendance'
        if not os.path.exists(path):
            os.mkdir(path)
        images = []
        self.class_names = []
        self.encode_list = []
        self.TimeList1 = []
        self.TimeList2 = []
        attendance_list = os.listdir(path)
        self.timer.timeout.connect(self.update_frame_mediapipe)
        self.timer.start(10)
    
    # Обновление кадров видеопотока для MEDIAPIPE
    def update_frame_mediapipe(self):
        # For webcam input:
        drawing_spec = self.mpDrawing.DrawingSpec(thickness=1, circle_radius=1)
        with self.mpFaceMesh.FaceMesh(
            min_detection_confidence=0.5,
            max_num_faces=1,
            min_tracking_confidence=0.5) as face_mesh:
            while self.capture.isOpened():
                success, image = self.capture.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    break
                # Преобразование изображение в формат BGR 
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = face_mesh.process(image)

                # Draw the face mesh annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_face_landmarks:
                    # Перебор массива обнаруженных лиц (в настройка выставлено одно: max_num_faces=1)
                    for face_landmarks in results.multi_face_landmarks:
                        # Перебор ключевых точек
                        for indexPoint, point in enumerate(face_landmarks.landmark):
                            index_rescale = 1
                            x = point.x * index_rescale
                            y = point.y * index_rescale
                            z = point.z * index_rescale
                            self.points[indexPoint] = {"X": x, "Y": y, "Z": z} 
                        # Формирование данных мимики и поворотов головы
                        if self.sendUDP:
                            self.GetFaceBlendShape()
                            self.GetRotationHead()
                        self.mpDrawing.draw_landmarks(
                            image=image,
                            landmark_list=face_landmarks,
                            connections=self.mpFaceMesh.FACE_CONNECTIONS,
                            landmark_drawing_spec=drawing_spec,
                            connection_drawing_spec=drawing_spec)
                qformat = QImage.Format_Indexed8
                if len(image.shape) == 3:
                    if image.shape[2] == 4:
                        qformat = QImage.Format_RGBA8888
                    else:
                        qformat = QImage.Format_RGB888
                outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
                outImage = outImage.rgbSwapped()
                self.frameVideo.setPixmap(QPixmap.fromImage(outImage))
                self.frameVideo.setScaledContents(True) 
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        self.capture.release()

    # Отправка данных по UDP
    def SendUDP(self, data, UDP_IP, UDP_PORT):
        print(type(data))
        if self.sendUDP:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(data.encode("utf-8"), (UDP_IP, UDP_PORT))

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()  

if __name__ == "__main__":
    main()