import can
from datetime import datetime
import time

VEH_SPD_PID = 0x0D
RSP_PAD = [0xAA] * 8
REQ_PAD = [0x55] * 8
REQ_ID = 0x7DF
RSP_ID = 0x7E8

VEH_SPD_INC = 10


def handle_veh_spd(veh_spd: int) -> None:
    print(f"Vehicle Speed = {veh_spd} [kph]")


def handle_rsp_timeout():
    print(f"Vehicle Speed = TIMEOUT")
    pass


def req_vehicle_speed() -> can.Message:
    req_data = REQ_PAD
    req_data[0] = 0x02  # DLC = 2
    req_data[1] = 0x01  # MOD = 1
    req_data[2] = VEH_SPD_PID  # Vehicle Speed (PID = 0x0D)
    return can.Message(
        arbitration_id=REQ_ID,
        data=req_data,
        is_extended_id=False,
        dlc=8,
        timestamp=datetime.timestamp(datetime.now()),
    )


def rsp_vehicle_speed(vehicle_speed) -> can.Message:
    rsp_data = RSP_PAD
    rsp_data[0] = 0x03  # DLC = 3
    rsp_data[1] = 0x41  # MOD = 1 + Positive Response = 0x40
    rsp_data[2] = VEH_SPD_PID  # Vehicle Speed (PID = 0x0D)
    rsp_data[3] = vehicle_speed  # Vehicle Speed (0-255 kph)
    return can.Message(
        arbitration_id=RSP_ID,
        data=rsp_data,
        is_extended_id=False,
        dlc=8,
        timestamp=datetime.timestamp(datetime.now()),
    )


def is_veh_speed_req(can_msg: can.Message) -> bool:
    ret = False
    if can_msg.arbitration_id == REQ_ID:
        if can_msg.dlc == 8:
            dlc = can_msg.data[0]
            mod = can_msg.data[1]
            pid = can_msg.data[2]
            if dlc == 0x02:
                if mod == 0x01:
                    if pid == VEH_SPD_PID:
                        ret = True
    return ret


def is_veh_speed_rsp(can_msg: can.Message) -> bool:
    ret = False
    if can_msg.arbitration_id == RSP_ID:
        if can_msg.dlc == 8:
            dlc = can_msg.data[0]
            mod = can_msg.data[1]
            pid = can_msg.data[2]
            ret = False
            if dlc == 0x03:
                if mod == 0x41:
                    if pid == VEH_SPD_PID:
                        ret = True
    return ret


def main():

    bus = can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=250000)

    while True:
        try:
            # Send Request
            bus.send(req_vehicle_speed())

            # Wait for response
            can_rsp = bus.recv(timeout=1)
            if can_rsp is None:
                handle_rsp_timeout()
            else:
                if is_veh_speed_rsp(can_rsp):
                    veh_spd = can_rsp.data[3] # Vehicle Speed (0-255 kph)
                    handle_veh_spd(veh_spd)
            time.sleep(1)

        except can.CanError as e:
            print(e)

if __name__ == "__main__":
    main()
