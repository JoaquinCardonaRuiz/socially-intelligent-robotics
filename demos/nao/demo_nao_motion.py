import time

from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest

nao = Nao(ip="10.0.0.236")

reply = nao.motion.request(NaoPostureRequest("Stand", 0.5))
time.sleep(1)

reply = nao.motion.request(NaoPostureRequest("Crouch", 0.5))
time.sleep(1)

