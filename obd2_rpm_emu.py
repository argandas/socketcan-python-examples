import can
from datetime import datetime
import threading
import time

rpm = 0

RPM_PID = 0x0C
RSP_PAD = [0xAA] * 8
REQ_PAD = [0x55] * 8
REQ_ID = 0x7DF
RSP_ID = 0x7E8


def req_rpm() -> can.Message:
    req_data = REQ_PAD
    req_data[0] = 0x02  # DLC = 2
    req_data[1] = 0x01  # MOD = 1
    req_data[2] = RPM_PID  # Vehicle Speed (PID = 0x0D)
    return can.Message(
        arbitration_id=REQ_ID,
        data=req_data,
        is_extended_id=False,
        dlc=8,
        timestamp=datetime.timestamp(datetime.now()),
    )


def rsp_rpm(rpm_value: int) -> can.Message:
    rsp_data = RSP_PAD
    rsp_data[0] = 0x04  # DLC = 4
    rsp_data[1] = 0x41  # MOD = 1 + Positive Response = 0x40
    rsp_data[2] = RPM_PID  # Vehicle Speed (PID = 0x0D)
    rsp_data[3] = rpm_value & 0xFF
    rsp_data[4] = (rpm_value >> 8) & 0xFF
    return can.Message(
        arbitration_id=RSP_ID,
        data=rsp_data,
        is_extended_id=False,
        dlc=8,
        timestamp=datetime.timestamp(datetime.now()),
    )


def is_rpm_req(can_msg: can.Message) -> bool:
    ret = False
    if can_msg.arbitration_id == REQ_ID:
        if can_msg.dlc == 8:
            dlc = can_msg.data[0]
            mod = can_msg.data[1]
            pid = can_msg.data[2]
            if dlc == 0x02:
                if mod == 0x01:
                    if pid == RPM_PID:
                        ret = True
    return ret


def is_rpm_rsp(can_msg: can.Message) -> bool:
    ret = False
    if can_msg.arbitration_id == RSP_ID:
        if can_msg.dlc == 8:
            dlc = can_msg.data[0]
            mod = can_msg.data[1]
            pid = can_msg.data[2]
            if dlc == 0x04:
                if mod == 0x41:
                    if pid == RPM_PID:
                        ret = True
    return ret


def obd2_rpm_handler(bus: can.BusABC):
    # Receive request
    global rpm
    while True:
        try:
            can_msg = bus.recv()
            if can_msg is not None:
                if is_rpm_req(can_msg):
                    # Send response
                    bus.send(rsp_rpm(rpm))
        except can.CanError as e:
            print(e)


def main():

    global rpm

    bus = can.interface.Bus(bustype="socketcan", channel="can0", bitrate=250000)

    threading.Thread(target=obd2_rpm_handler, kwargs={"bus": bus}).start()

    while True:
        rpm_str = input("RPM = ")
        rpm = int(rpm_str)
        time.sleep(1)


if __name__ == "__main__":
    main()
