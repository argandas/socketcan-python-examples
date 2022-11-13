# Install Linux CAN utils
```bash
sudo apt install can-utils
```

# Install Python CAN library
```bash
pip install python-can
```

# Setup Virtual CAN interface
```bash
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

# CAN Utils examples

## Dump all CAN traffic
```bash
candump vcan0
```

# Generate random CAN messages
```bash
cangen vcan0 -v
```
# Generate random CAN messages (DLC = 8)
```bash
cangen vcan0 -v -L 8
```

## OBD2 Vehicle Speed request every second
```bash
cangen vcan0 -g 1000 -I 7DF -L 8 -D 02010D5555555555 -v
```