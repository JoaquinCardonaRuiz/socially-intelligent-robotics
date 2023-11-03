import queue
import cv2
from sic_framework.core.message_python2 import CompressedImageMessage
from sic_framework.devices import Nao

imgs = queue.Queue()


def on_image(image_message: CompressedImageMessage):
    # we could cv2.imshow here, but that does not work on Mac OSX
    imgs.put(image_message.image[..., ::-1])


nao = Nao(ip="192.168.0.0")
nao.top_camera.register_callback(on_image)

for i in range(10000):
    img = imgs.get()
    cv2.imshow('', img)
    cv2.waitKey(1)
