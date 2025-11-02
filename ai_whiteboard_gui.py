import sys
import cv2
import numpy as np
import mediapipe as mp
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, 
    QSlider, QColorDialog, QLabel, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap, QColor

# ---------------------
# Hand Tracking Setup
# ---------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# ---------------------
# PyQt Whiteboard App
# ---------------------
class Whiteboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Finger Whiteboard")
        self.setGeometry(100, 100, 1280, 720)

        # Drawing variables
        self.pen_color = (255, 0, 0)
        self.pen_width = 5
        self.drawing = False
        self.mode = "freehand"  # 'freehand' or 'shape'
        self.shape_type = None  # 'line', 'rect', 'circle'
        self.start_pos = None
        self.temp_canvas = None  # For showing shapes while dragging
        self.prev_x, self.prev_y = 0, 0

        # Canvas
        self.canvas = None

        # Webcam
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # PyQt Layout
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        # Buttons
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_canvas)
        btn_layout.addWidget(self.clear_btn)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_canvas)
        btn_layout.addWidget(self.save_btn)

        self.color_btn = QPushButton("Pick Color")
        self.color_btn.clicked.connect(self.pick_color)
        btn_layout.addWidget(self.color_btn)

        # Pen width slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(20)
        self.slider.setValue(self.pen_width)
        self.slider.valueChanged.connect(self.change_width)
        btn_layout.addWidget(QLabel("Pen Width"))
        btn_layout.addWidget(self.slider)

        # Shape buttons
        self.line_btn = QPushButton("Line")
        self.line_btn.clicked.connect(lambda: self.set_shape("line"))
        btn_layout.addWidget(self.line_btn)

        self.rect_btn = QPushButton("Rectangle")
        self.rect_btn.clicked.connect(lambda: self.set_shape("rect"))
        btn_layout.addWidget(self.rect_btn)

        self.circle_btn = QPushButton("Circle")
        self.circle_btn.clicked.connect(lambda: self.set_shape("circle"))
        btn_layout.addWidget(self.circle_btn)

        # Freehand button
        self.freehand_btn = QPushButton("Freehand")
        self.freehand_btn.clicked.connect(self.set_freehand)
        btn_layout.addWidget(self.freehand_btn)

        layout.addLayout(btn_layout)

        # Video label
        self.video_label = QLabel()
        self.video_label.setMouseTracking(True)
        self.video_label.mousePressEvent = self.mouse_press
        self.video_label.mouseMoveEvent = self.mouse_move
        self.video_label.mouseReleaseEvent = self.mouse_release
        layout.addWidget(self.video_label)

        self.setLayout(layout)

        # Timer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(15)  # ~66 FPS target

    # ---------------------
    # Button Functions
    # ---------------------
    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas = np.zeros_like(self.canvas)

    def save_canvas(self):
        if self.canvas is not None:
            cv2.imwrite("whiteboard.png", self.canvas)
            print("Canvas saved as whiteboard.png")

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pen_color = (color.blue(), color.green(), color.red())

    def change_width(self, value):
        self.pen_width = value

    def set_shape(self, shape):
        self.mode = "shape"
        self.shape_type = shape

    def set_freehand(self):
        self.mode = "freehand"
        self.shape_type = None

    # ---------------------
    # Mouse Events for Shapes
    # ---------------------
    def mouse_press(self, event):
        if self.mode == "shape":
            self.start_pos = event.pos()
            self.temp_canvas = self.canvas.copy()

    def mouse_move(self, event):
        if self.mode == "shape" and self.start_pos is not None:
            end_pos = event.pos()
            self.canvas = self.temp_canvas.copy()
            x1, y1 = self.start_pos.x(), self.start_pos.y()
            x2, y2 = end_pos.x(), end_pos.y()
            if self.shape_type == "line":
                cv2.line(self.canvas, (x1, y1), (x2, y2), self.pen_color, self.pen_width)
            elif self.shape_type == "rect":
                cv2.rectangle(self.canvas, (x1, y1), (x2, y2), self.pen_color, self.pen_width)
            elif self.shape_type == "circle":
                radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                cv2.circle(self.canvas, (x1, y1), radius, self.pen_color, self.pen_width)

    def mouse_release(self, event):
        if self.mode == "shape":
            self.start_pos = None
            self.temp_canvas = None

    # ---------------------
    # Frame Update
    # ---------------------
    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Resize frame for performance
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))
        h, w, c = frame.shape

        # Initialize canvas
        if self.canvas is None or self.canvas.shape[:2] != frame.shape[:2]:
            self.canvas = np.zeros_like(frame)

        # Hand Tracking for freehand mode
        if self.mode == "freehand":
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)
            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                x, y = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)
                if self.drawing:
                    if self.prev_x == 0 and self.prev_y == 0:
                        self.prev_x, self.prev_y = x, y
                    cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y), self.pen_color, self.pen_width)
                    self.prev_x, self.prev_y = x, y
                else:
                    self.prev_x, self.prev_y = 0, 0
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Merge canvas and webcam
        combined = cv2.addWeighted(frame, 0.5, self.canvas, 0.5, 0)

        # Convert to QImage
        img = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
        qt_img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

    # ---------------------
    # Key events
    # ---------------------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.drawing = not self.drawing
        elif event.key() == Qt.Key_C:
            self.clear_canvas()


# ---------------------
# Run App
# ---------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Whiteboard()
    window.show()
    sys.exit(app.exec_())
