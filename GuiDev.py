#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName    :GuiDev.py
# @Time        :2024/8/29 下午9:04
# @Author      :Xinrong.Li23@xjtlu.edu.cn
# email2 lixinrong4002@gmail.com

# 写了两天写吐了不想再看到一眼这个大屎山让我走吧让我走吧让我走吧让我走吧求你了求你了求你了

# TODO: STREAM SUPPORT BY CV
# TODO: LOGGING TO DO
# TODO: CONTEXT ACTIONS
# TODO: HELP PAGE
# TODO: MENU PAGES: about, help, github page

import os
import json
from typing import Dict, Any
import cv2

from ultralytics import YOLO

from PySide6.QtWidgets import (QMainWindow, QWidget, QApplication,
                               QMessageBox, QFileDialog,
                               QLabel, QSlider, QPushButton,
                               QHeaderView, QAbstractItemView)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QImage, QIcon
from PySide6.QtCore import Qt, Signal, Slot, QThread, QObject, QTimer
from ui_GUI import Ui_MainWindow


def pa(path: str) -> str:
    return path.replace('\\', '/')


class ConfigManager(QWidget):
    def __init__(self):
        """
        initialize and read the config file
        """

        super().__init__()

        self.configFileFolder = 'config'
        self.configFilePath = pa(os.path.join(self.configFileFolder, 'config.json'))

        self.sourcePathList = []
        # outputPath 是在系统中的绝对路径
        self.outputPath = pa(os.path.join(os.getcwd(), 'output'))
        self.alertAfterComplete = True

        self.ModelPath = pa(os.path.join(os.getcwd(), 'model/yolo8n.pt'))
        self.confidence = '0.5'

        # check if the config file and folder exist
        if not os.path.exists(self.configFilePath):
            self.createDefaultConfig()
        else:
            self.readConfigFile()

    def _modelPathValidator(self, modelPath: str) -> str:
        if os.path.exists(modelPath):
            if modelPath.endswith('.pt'):
                return modelPath
            else:
                QMessageBox.warning(self, 'Warning', 'The model should be a .pt file')
                return "model/yolo8n.pt"
        else:
            QMessageBox.warning(self, 'Warning', 'The model path is not valid!')
            return "model/yolo8n.pt"

    def _outputPathValidator(self, outputPath: str) -> str:
        if os.path.exists(outputPath):
            return outputPath
        else:
            QMessageBox.warning(self, 'Warning', 'The output path is not valid\n auto create it now')
            os.mkdir(outputPath)
            return outputPath

    def confidenceValidator(self, confidence: str) -> float:
        try:
            confidence = float(confidence)
            if 0 < confidence <= 1:
                return confidence
            else:
                QMessageBox.warning(self, 'Warning', 'The confidence should be a number between 0 and 1, set confidence = 0.5 now')
                return 0.5
        except TypeError:
            QMessageBox.warning(self, 'Warning', 'The confidence should be a number, set confidence = 0.5 now')
            return 0.5

    def readConfigFile(self) -> None:
        """read config file (json)
        and give out data"""
        with open(self.configFilePath) as f:
            config = json.load(f)

            # common settings
            self.outputPath = self._outputPathValidator(config['common']['OutputPath']) if config['common']['OutputPath'] != "" else self.outputPath
            self.alertAfterComplete = config['common']['alertAfterComplete']

            # model settings
            self.ModelPath = self._modelPathValidator(config['Model']['ModelPath']) if config['Model']['ModelPath'] != "" else self.ModelPath
            self.confidence = self.confidenceValidator(config['Model']['confidence']) if config['Model']['confidence'] != "" else self.confidence

        # Done: analyse the data: for example: does the ckpt exist?

    def updateConfigFile(self, **kwargs) -> None:
        # validation and update first
        self.outputPath = self._outputPathValidator(kwargs.get('OutputPath', self.outputPath))
        self.alertAfterComplete = kwargs.get('alertAfterComplete', self.alertAfterComplete)
        self.confidence = self.confidenceValidator(kwargs.get('confidence', self.confidence))
        self.ModelPath = self._modelPathValidator(kwargs.get('ModelPath', self.ModelPath))

        with open(self.configFilePath, 'w') as f:
            config = {
                "common": {
                    "OutputPath": self.outputPath,
                    "alertAfterComplete": self.alertAfterComplete
                },
                "Model": {
                    "ModelPath": self.ModelPath,
                    "confidence": self.confidence
                }
            }
            json.dump(config, f, indent=4)

        # self.readConfigFile()  # update information in the class' attributes  # no need now

    def createDefaultConfig(self) -> None:
        """Create the folder 'config' and put default config file in it."""
        if not os.path.exists(self.configFileFolder):
            os.mkdir(self.configFileFolder)

        new_config: Dict[str, Dict[str, Any]] = {
            "common": {
                "OutputPath": "",
                "alertAfterComplete": True
            },
            "Model": {
                "ModelPath": "",
                "confidence": ""
            }
        }

        with open(self.configFilePath, 'w') as f:
            json.dump(new_config, f, indent=4)
            print("Default config file created at", self.configFilePath)


class YOLODetector:
    def __init__(self, **kwargs):
        self.model = kwargs['ModelPath']
        self.sources: list = kwargs['sourcesPath']
        self.name = 'predict'
        self.project: str = kwargs['OutputPath']
        self.conf: float = kwargs['confidence']

        self.save = True
        self.show = False

    def inference(self):
        model = YOLO(self.model)
        results = model.predict(source=self.sources,
                                save=self.save,
                                project=self.project,
                                name=self.name,
                                show=self.show,
                                conf=self.conf,
                                exist_ok=True)

    def returnOutputPath(self) -> str:
        return pa(os.path.join(self.project, self.name))

    def returnOutputFilePath(self) -> list[str]:
        filePaths = []
        for file in self.sources:
            fileName = file.split('/')[-1].replace('.mp4', '.avi')
            filePaths.append(pa(os.path.join(self.project, self.name, fileName)))
        return filePaths


class YOLOWorker(QObject):
    finished = Signal()

    def __init__(self, yolo_func):
        super().__init__()
        self.yolo_func = yolo_func

    def run(self):
        self.yolo_func()
        self.finished.emit()


class SourceListTable(QStandardItemModel):
    sourceSingleChanged = Signal(dict, int)

    def __init__(self):
        super().__init__()
        # set Headers
        self.setHorizontalHeaderLabels(['Need', 'Path', 'Status'])

        self.itemChanged.connect(self.onItemChanged)

    def onItemChanged(self, item: QStandardItem):
        if item.isCheckable():
            source = item.data(Qt.ItemDataRole.UserRole)
            if source:
                source['checked'] = (item.checkState() == Qt.CheckState.Checked)
                index = item.index().row()
                self.sourceSingleChanged.emit(source, index)
                print(f'Source updated: {source} at index {index}')

    def updateSourceList(self, sources: list):
        self.setRowCount(0)  # clear all
        for row, source in enumerate(sources):
            needItem = QStandardItem()
            needItem.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            needItem.setData(Qt.CheckState.Checked if source['checked'] else Qt.CheckState.Unchecked,
                             role=Qt.ItemDataRole.CheckStateRole)
            needItem.setData(source, Qt.ItemDataRole.UserRole)
            needItem.setText("")

            pathItem = QStandardItem(source["path"])
            statusItem = QStandardItem(source['status'])

            self.setItem(row, 0, needItem)
            self.setItem(row, 1, pathItem)
            self.setItem(row, 2, statusItem)


class VideoPlayer(QObject):
    def __init__(self, slider: QSlider, playButton: QPushButton):
        super().__init__()
        self.slider = slider
        self.playButton = playButton
        self.timer = QTimer(self)
        self.isPlaying = False
        self.caps = []  # 用于存储多个视频捕获对象
        self.labels = []  # 用于存储多个QLabel对象
        self.timer.timeout.connect(self.nextFrame)  # 确保定时器只连接一次

        self.playButton.clicked.connect(self.playPauseVideo)

    def addVideo(self, videoPath: str, label: QLabel):
        cap = cv2.VideoCapture(videoPath)
        if not cap.isOpened():
            print(f"Failed to open video: {videoPath}")
            return
        self.caps.append(cap)
        self.labels.append(label)

        # 设置滑块的最大值为第一个视频的帧数（假设所有视频帧数相同）
        if len(self.caps) == 1:
            self.slider.setMinimum(0)
            self.slider.setMaximum(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1)
            self.slider.valueChanged.connect(self.updateFrames)

        # 加载视频的第一帧到对应的 QLabel
        self.updateFrame(label, cap, self.slider.value())

    def updateFrames(self):
        position = self.slider.value()
        for cap, label in zip(self.caps, self.labels):
            self.updateFrame(label, cap, position)

    def updateFrame(self, label: QLabel, cap: cv2.VideoCapture, position: int):
        cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            label.setPixmap(pixmap.scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def playPauseVideo(self):
        if not self.caps or not all(cap.isOpened() for cap in self.caps):
            return

        if self.isPlaying:
            self.timer.stop()
            self.isPlaying = False
            self.playButton.setText('Play')
            self.playButton.setIcon(QIcon(':/icons/play.svg'))
        else:
            self.timer.start(30)  # refresh 30 ms per frame
            self.isPlaying = True
            self.playButton.setText('Pause')
            self.playButton.setIcon(QIcon(':/icons/pause.svg'))

    def nextFrame(self):
        current_position = self.slider.value()
        if current_position < self.slider.maximum():
            self.slider.setValue(current_position + 1)
        else:
            self.timer.stop()
            self.isPlaying = False
            self.playButton.setText("Play")
            self.playButton.setIcon(QIcon(':/icons/play.svg'))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        initialize first
        connect to ui
        bind the buttons
        then read the config
        """
        super().__init__()
        self.setupUi(self)

        self.configManager = ConfigManager()

        self.isSingleFile = bool(self.comboBox.currentIndex)
        # PLAN: improve robustness, what the index is more than 1 in the future update? -- NO PLAN NOW

        self.sourceList = []
        self.model = SourceListTable()

        # video Player config
        self.VideoPlayer = VideoPlayer(self.horizontalSlider, self.playButton)
        self.isPlaying = False

        """
        sourceList will contain all the Source in the List in the format like
        [
            {
                "checked": true,
                "status": 0,
                "path": "path/to/first/file1"
            },
            {
                "checked": true,
                "status": 0,
                "path": "path/to/first/file2"
            }
        ]
        """

        self.thread = None
        self.worker = None

        self.bindModelConfig()
        self.bindCommonConfig()
        self.bindDisplayTab()

        # signal binding
        self.model.sourceSingleChanged.connect(self.sourceSingleChangedSignalReceiver)

    def bindDisplayTab(self):
        # the source display and outputDisplay should be updated when a line in sourceList is selected
        self.listTableView.setModel(self.model)
        self.listTableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        header = self.listTableView.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.listTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # self.model.updateSourceList([  # test
        #     {'checked': True, 'path': '/path/to/file1dsfsdfsdsf', 'status': 'Completed'},
        #     {'checked': False, 'path': '/path/to/file2', 'status': 'Pending'},
        #     {'checked': True, 'path': '/path/to/file3', 'status': 'Failed'}
        # ])
        self.listTableView.doubleClicked.connect(self.isPathItemClicked)

        self.detectStartButton.clicked.connect(self.detectStartButtonClicked)

    def yolo(self) -> None:
        sourcePathList: list[str] = []
        updateList: list[dict] = []

        for item in self.sourceList:
            if item['checked']:
                updateList.append(item)
                sourcePathList.append(item['path'])
                item['status'] = 'Detecting'

        self.model.updateSourceList(self.sourceList)

        if sourcePathList:
            for path in sourcePathList:
                if self._isPathVideo(path):
                    self.yoloProcessVideo(path)
                else:
                    self.yoloProcessImage(path)

            self.model.updateSourceList(self.sourceList)

    def yoloProcessImage(self, image_path: str) -> None:
        Detector = YOLO(self.configManager.ModelPath)
        results = Detector.predict(source=image_path,
                                   save=True,
                                   project=self.configManager.outputPath,
                                   conf=self.configManager.confidence)

    def yoloProcessVideo(self, video_path: str) -> None:
        Detector = YOLO(self.configManager.ModelPath)
        results = Detector.predict(source=video_path,
                                   save=True,
                                   project=self.configManager.outputPath,
                                   conf=self.configManager.confidence)

    def detectStartButtonClicked(self) -> None:
        self.detectStartButton.setEnabled(False)

        # config
        self.thread = QThread()
        self.worker = YOLOWorker(self.yolo)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # signal connections to the UI
        self.thread.started.connect(lambda: self.detectStartButton.setEnabled(False))
        self.thread.finished.connect(lambda: self.detectStartButton.setEnabled(True))

        # work
        self.thread.start()

    @Slot(dict)
    def sourceSingleChangedSignalReceiver(self, updatedSourceSingle: dict, index: int) -> None:
        self.sourceList[index] = updatedSourceSingle
        # self.model.updateSourceList(self.sourceList)

    def isOutputPathExist(self, originalPath: str) -> (bool, str):
        fileName = originalPath.split('/')[-1].replace('.mp4', '.avi')
        outputPath = pa(os.path.join(self.configManager.outputPath, 'predict', fileName))
        return os.path.exists(outputPath), outputPath

    def isPathItemClicked(self, index: QStandardItem):
        print(f"clicked on {index.row()}, {index.column()}")
        if index.column() == 1:
            path = self.model.item(index.row(), index.column()).text()
            self.updateSourceLabelDisplay(path)

            isOutputExist = self.isOutputPathExist(path)
            if isOutputExist[0]:
                self.updateOutputLabelDisplay(isOutputExist[1])
                print(f"output path {isOutputExist[1]} does exist")
            else:
                print(f"output path {isOutputExist[1]} does NOT exist")
                # clear the label display to blank
                self.updateOutputLabelDisplay('')
            # DONE: VIDEO DISPLAY


    @staticmethod
    def _isPathVideo(path: str) -> bool:
        return path.endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.mpeg'))

    def updateSourceLabelDisplay(self, path: str):
        isVideo = self._isPathVideo(path)
        if isVideo:
            self.VideoPlayer.addVideo(path, self.sourceDisplayLabel)  # 绑定 sourceDisplayLabel 到控制条
        else:  # it is a picture
            print('pixmap source display part')
            print(path)
            pixmap = QPixmap(path)  # 直接从路径加载图片
            if not pixmap.isNull():  # 检查图片是否加载成功
                self.sourceDisplayLabel.setPixmap(
                    pixmap.scaled(self.sourceDisplayLabel.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation))
            else:
                print("Failed to load the image.")

    def updateOutputLabelDisplay(self, path: str):
        if path:
            isVideo = self._isPathVideo(path)
            if isVideo:
                self.VideoPlayer.addVideo(path, self.outputDisplayLabel)
            else:
                pixmap = QPixmap(path)  # 直接从路径加载图片
                if not pixmap.isNull():  # 检查图片是否加载成功
                    self.outputDisplayLabel.setPixmap(
                        pixmap.scaled(self.outputDisplayLabel.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation))
                else:
                    print("Failed to load the image.")
            return pa(path), isVideo
        else:
            self.outputDisplayLabel.setText('No Output')

    def bindModelConfig(self) -> None:
        # DONE!
        self.selectModelButton.clicked.connect(self.selectModeButtonClicked)
        self.modelPathLineEdit.setText(self.configManager.ModelPath)
        self.confidenceLineEdit.textEdited.connect(self.confidenceLineEditChanged)
        self.confidenceLineEdit.setText(str(self.configManager.confidence))

    def confidenceLineEditChanged(self) -> None:
        newConfidence = self.confidenceLineEdit.text()
        self.configManager.updateConfigFile(confidence=newConfidence)
        self.confidenceLineEdit.setText(newConfidence)

    def selectModeButtonClicked(self) -> None:
        modelpath = QFileDialog.getOpenFileName(
            self,
            'Select pt model',
            '',
            '*.pt'
        )[0]
        self.configManager.updateConfigFile(ModelPath=modelpath) if modelpath else None
        self.modelPathLineEdit.setText(self.configManager.ModelPath) if modelpath else None

    def bindCommonConfig(self) -> None:
        self.inputFileSelectButton.clicked.connect(self.inputSelectButtonClicked)
        self.comboBox.currentTextChanged.connect(self.setIsSingleFile)

        self.outputPathSelectPathButton.clicked.connect(self.selectOutputPath)
        self.outputLineEdit.setText(self.configManager.outputPath)

        self.alertAfterCompleteCheckBox.setChecked(self.configManager.alertAfterComplete)
        self.alertAfterCompleteCheckBox.checkStateChanged.connect(self.changeAlertMode)

    def selectOutputPath(self):
        outputPath = QFileDialog.getExistingDirectory(
            self,
            'Select output path',
            ''
        )
        self.configManager.updateConfigFile(OutputPath=outputPath) if outputPath else None
        self.outputLineEdit.setText(outputPath) if outputPath else None

    def changeAlertMode(self):
        alertMode = self.alertAfterCompleteCheckBox.isChecked()
        self.configManager.updateConfigFile(alertAfterComplete=alertMode)
        print(f"alert mode changed to {alertMode}")

    def putFileToSourceList(self, files: list):
        for filePath in files:
            newSource = {
                "checked": True,
                "status": 'pending',
                "path": pa(filePath)
            }
            self.sourceList.append(newSource)
        self.model.updateSourceList(self.sourceList)

    def putDirToSourceList(self, Dir: str):
        # 输入的应该是一个dir的path: str，接着检查这个dir下面（只有一层）中有没有指定格式的文件，如果有，则加入一个列表中
        _list = []
        for file in os.listdir(Dir):
            if file.endswith(('.jpg', '.bmp', '.png', '.mp4', '.avi', '.mov', '.mkv', 'flv', '.mpeg')):
                _list.append(file)
        self.putFileToSourceList(_list)

    def inputSelectButtonClicked(self):
        if self.isSingleFile:  # if index of comboBox is 0 (false)
            files = QFileDialog.getOpenFileNames(
                self,
                'choose file (video/picture)',
                '',
                'image(*.jpg *.bmp *.png) ;;video(*.mp4 *.avi *.mov *.mkv *.flv *.mpeg)'
            )[0]
            self.putFileToSourceList(files) if files else None

        else:  # if index of comboBox is 1 (true)
            directory = QFileDialog.getExistingDirectory(
                None,
                "Select Directory",
                "/",
                QFileDialog.Option.ShowDirsOnly
            )
            self.putDirToSourceList(directory) if directory else None

    def setIsSingleFile(self):
        self.isSingleFile = not bool(self.comboBox.currentIndex())
        print(f'single file mode: {self.isSingleFile}')


if __name__ == '__main__':
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
