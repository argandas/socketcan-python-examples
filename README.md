# socketcan-python-examples
Python CAN - Linux socketcan examples

CAN Interface setup
```bash
sudo ifconfig can0 down 
sudo ip link set can0 type can bitrate 500000
sudo ifconfig can0 up
```

Python CAN Library install 
```bash
python3 -m pip install python-can
```