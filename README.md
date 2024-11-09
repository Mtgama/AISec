# SecApp - PyQt5 Security Application

SecApp is a security application built with PyQt5 that enhances system security through facial or hand gesture recognition, as well as password verification. It runs on Windows and ensures user authentication at system startup by checking for a specific predefined gesture, number of fingers, or face recognition. If authentication fails after several attempts, the system shuts down or restarts automatically.

![SecApp Icon](https://s3.uupload.ir/files/matgama/ai/cyber-security.png)


## Features

- **Face Recognition**: Authenticates the user by detecting a specific face image.
- **Finger Detection**: Verifies the user by counting the number of displayed fingers.
- **Password Verification**: Prompts the user for a password if biometric authentication fails.
- **System Restart on Unauthorized Closure**: Prevents unauthorized shutdowns by forcing a system restart if the application is closed before successful authentication.
- **Customizable Settings**: Allows users to define security settings, such as required finger count, password, and whether to enable face recognition.

## Requirements

- Python 3.x
- Libraries:
  - PyQt5
  - OpenCV
  - MediaPipe
  - pystray
  - PIL
  - face_recognition

You can install all dependencies using the following command:

```bash
pip install pyqt5 opencv-python mediapipe pystray pillow face_recognition

```


# SecApp - برنامه امنیتی با PyQt5

**SecApp** یک برنامه امنیتی است که با استفاده از PyQt5 ساخته شده و امنیت سیستم را از طریق تشخیص چهره یا شناسایی انگشتان دست، همچنین تایید پسورد، تقویت می‌کند. این برنامه روی ویندوز اجرا می‌شود و از شما می‌خواهد در شروع سیستم، از طریق یک ژست مشخص، تعداد انگشتان یا شناسایی چهره، تایید هویت انجام دهید. در صورت عدم تایید بعد از چندین تلاش، سیستم به طور خودکار خاموش یا ریستارت می‌شود.

## ویژگی‌ها

- **تشخیص چهره**: احراز هویت کاربر با شناسایی یک تصویر چهره مشخص.
- **شناسایی انگشتان**: تایید هویت کاربر با شناسایی تعداد انگشتان دست.
- **تایید پسورد**: در صورت عدم شناسایی انگشت یا چهره، از کاربر پسورد خواسته می‌شود.
- **ریستارت سیستم در صورت بستن غیرمجاز**: اگر کاربر برنامه را قبل از تایید هویت ببندد، سیستم به طور خودکار ریستارت می‌شود.
- **تنظیمات قابل تنظیم**: کاربران می‌توانند تنظیمات امنیتی مانند تعداد انگشتان مورد نیاز، پسورد و فعال یا غیرفعال کردن تشخیص چهره را تعیین کنند.

## پیش‌نیازها

- Python 3.x
- کتابخانه‌ها:
  - PyQt5
  - OpenCV
  - MediaPipe
  - pystray
  - PIL
  - face_recognition

برای نصب تمامی وابستگی‌ها از دستور زیر استفاده کنید:

```bash
pip install pyqt5 opencv-python mediapipe pystray pillow face_recognition
