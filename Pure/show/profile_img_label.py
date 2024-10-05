#  profile_img_label.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QBrush, QImage, QPainter, QPixmap, QColor
from PySide6.QtWidgets import QLabel


class ProfileImgLabel(QLabel):
    _image_path: str

    def __init__(self, square: int, image: str = None, parent=None):
        super().__init__(parent)
        super().setFixedSize(square, square)
        if image:
            self.set_image(image)
        else:
            self.setPixmap(_circle_pixmap(QColor(Qt.GlobalColor.lightGray), square, self.devicePixelRatio()))

    def set_image(self, path: str):
        self._image_path = path
        with open(self._image_path, 'rb') as f:
            self.setPixmap(
                _circle_masked_pixmap(
                    f.read(),
                    pixel=self.size().height(),
                    scale=self.devicePixelRatio()
                )
            )

    # OVERRIDE
    def setFixedSize(self, arg__1):
        super().setFixedSize(arg__1)
        self.set_image(self._image_path)


# 비트맵 이미지를 원형 마스크 픽셀맵으로 반환
# 원형 이미지를 캐시로 저장할 거라면 pillow 가 나은 선택이다. 로직은 비슷하다.
# https://stefan.sofa-rockers.org/2018/05/04/how-to-mask-an-image-with-a-smooth-circle-in-pyqt5/
def _circle_masked_pixmap(imgdata, imgtype='jpg', pixel=64, scale=1.0):
    # 바이너리 이미지를 QImage로 만들어 ARGB32 이미지 포멧으로 변환
    image = QImage.fromData(imgdata, imgtype)
    image.convertToFormat(QImage.Format.Format_ARGB32)
    # 이미지 정사각형 비율로 크롭
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) // 2,
        (image.height() - imgsize) // 2,
        imgsize,
        imgsize
    )
    image = image.copy(rect)
    # 사이즈가 동일한 정사각 투명 이미지 준비
    out_img = QImage(imgsize, imgsize, QImage.Format.Format_ARGB32)
    out_img.fill(Qt.GlobalColor.transparent)
    # 투명 정사각형에 원형으로 이미지로 렌더링
    brush = QBrush(image)
    painter = QPainter(out_img)
    painter.setBrush(brush)
    painter.setPen(Qt.PenStyle.NoPen)  # 아웃라인 필요없어
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.drawEllipse(0, 0, imgsize, imgsize)  # 원형 마스크
    painter.end()
    # 픽셀멥으로 변환하고 크기를 조정. 디바이스 픽셀비율 적용하여 반환
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(scale)
    pixel *= scale
    return pm.scaled(
        pixel, pixel,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )


def _circle_pixmap(color: QColor, pixel=64, scale=1.0):
    out_img = QImage(pixel, pixel, QImage.Format.Format_ARGB32)
    out_img.fill(Qt.GlobalColor.transparent)
    painter = QPainter(out_img)
    painter.setBrush(color)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.drawEllipse(0, 0, pixel, pixel)
    painter.end()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(scale)
    pixel *= scale
    return pm.scaled(
        pixel, pixel,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )

