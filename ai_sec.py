import sys, json, os, cv2
from PyQt5 import QtWidgets
import mediapipe as mp
from pystray import MenuItem as itm
from PIL import Image, ImageDraw
import pystray, face_recognition
from time import time

conf_file = 'settings.json'
face_img_file = 'image.png'

class SecApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

        if not self.load_config():
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to load settings.")
            sys.exit(1)

        self.hand_det = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
        self.tray = None
        self.attempt_cnt = 0
        self.t0 = time()
        self.authenticated = False  # تعیین وضعیت احراز هویت

        if self.recog_face:
            self.face_detection()
        else:
            self.finger_detection()

    def setup(self):
        self.setWindowTitle("Security App")
        self.resize(300, 200)

    def load_config(self):
        try:
            with open(conf_file, 'r') as f:
                sett = json.load(f)
                self.req_fingers = sett.get('finger_count')
                self.passcode = sett.get('password')
                self.recog_face = sett.get('use_face_recognition', False)
                return True
        except:
            print("No settings found.")
            return False

    def face_detection(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cam error.")
            return
        if not os.path.exists(face_img_file):
            QtWidgets.QMessageBox.warning(self, "Face Image Missing", "Save a face image in settings.")
            cap.release()
            return

        ref_img = face_recognition.load_image_file(face_img_file)
        ref_encoding = face_recognition.face_encodings(ref_img)[0]

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if time() - self.t0 > 7:
                cap.release()
                cv2.destroyAllWindows()
                self.ask_pass()
                return

            rgb_frame = frame[:, :, ::-1]
            locations = face_recognition.face_locations(rgb_frame)
            encodings = face_recognition.face_encodings(rgb_frame, locations)

            for enc in encodings:
                if True in face_recognition.compare_faces([ref_encoding], enc):
                    self.authenticated = True
                    cap.release()
                    cv2.destroyAllWindows()
                    self.hide()
                    self.show_tray()
                    return

            cv2.imshow("Face Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def finger_detection(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cam error.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if time() - self.t0 > 7:
                cap.release()
                cv2.destroyAllWindows()
                self.ask_pass()
                return

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hand_det.process(rgb_frame)
            total_fingers = 0

            if result.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                    label = handedness.classification[0].label
                    cnt = self.finger_count(hand_landmarks, label)
                    total_fingers += cnt

                    cv2.putText(frame, f"{label} Hand: {cnt} fingers", 
                                (10, 30 if label == "Right" else 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            if total_fingers == self.req_fingers:
                self.authenticated = True
                cap.release()
                cv2.destroyAllWindows()
                self.hide()
                self.show_tray()
                return

            cv2.imshow("Finger Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def finger_count(self, hnd_lm, lbl):
        tips = [8, 12, 16, 20]
        thumb = 4
        fingers = 0

        if (lbl == "Right" and hnd_lm.landmark[thumb].x < hnd_lm.landmark[thumb - 2].x) or \
           (lbl == "Left" and hnd_lm.landmark[thumb].x > hnd_lm.landmark[thumb - 2].x):
            fingers += 1

        for t in tips:
            if hnd_lm.landmark[t].y < hnd_lm.landmark[t - 2].y:
                fingers += 1

        return fingers

    def ask_pass(self):
        pw, ok = QtWidgets.QInputDialog.getText(self, "Password Required", "Enter password:", QtWidgets.QLineEdit.Password)
        if ok and pw == self.passcode:
            self.authenticated = True
            self.show_tray()
        else:
            self.attempt_cnt += 1
            if self.attempt_cnt < 3:
                self.ask_pass()
            else:
                os.system("shutdown /s /t 1")

    def show_tray(self):
        img = Image.new('RGB', (64, 64), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 64, 64], fill="blue")
        draw.text((10, 20), "App", fill="white")

        menu = (itm('Settings', self.show_sett), itm('Quit', self.exit_app))
        self.tray = pystray.Icon("SecApp", img, "Sec App", menu)
        self.tray.run()

    def show_sett(self, icon=None, itm=None):
        d = SettDialog(self)
        if d.exec_() == QtWidgets.QDialog.Accepted:
            self.req_fingers = d.finger_cnt.value()
            self.passcode = d.pass_input.text()
            self.recog_face = d.chkbox.isChecked()
            self.save_conf()
            if self.recog_face:
                self.save_face()

    def save_conf(self):
        sett = {'finger_count': self.req_fingers, 'password': self.passcode, 'use_face_recognition': self.recog_face}
        with open(conf_file, 'w') as f:
            json.dump(sett, f)
        print("Settings saved.")

    def save_face(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cam error.")
            return

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(face_img_file, frame)
            print("Face image saved.")
        cap.release()

    def exit_app(self, icon, itm):
        self.tray.stop()
        sys.exit(0)

    def closeEvent(self, event):
        if not self.authenticated:
            QtWidgets.QMessageBox.warning(self, "Security Alert", "Unauthorized closing detected. System will restart.")
            os.system("shutdown /r /t 1")  # ری‌استارت اجباری سیستم
        event.ignore()  # جلوگیری از بسته‌شدن پنجره

class SettDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        self.finger_cnt = QtWidgets.QSpinBox(self)
        self.finger_cnt.setRange(1, 10)
        self.pass_input = QtWidgets.QLineEdit(self)
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.chkbox = QtWidgets.QCheckBox("Use Face Recognition", self)

        save_btn = QtWidgets.QPushButton("Save", self)
        save_btn.clicked.connect(self.accept)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Number of fingers:"))
        layout.addWidget(self.finger_cnt)
        layout.addWidget(QtWidgets.QLabel("Password:"))
        layout.addWidget(self.pass_input)
        layout.addWidget(self.chkbox)
        layout.addWidget(save_btn)
        self.setLayout(layout)
        self.load_curr_conf()

    def load_curr_conf(self):
        try:
            with open(conf_file, 'r') as f:
                s = json.load(f)
                self.finger_cnt.setValue(s.get('finger_count', 5))
                self.pass_input.setText(s.get('password', ''))
                self.chkbox.setChecked(s.get('use_face_recognition', False))
        except:
            print("Using defaults.")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SecApp()
    w.show()
    sys.exit(app.exec_())
