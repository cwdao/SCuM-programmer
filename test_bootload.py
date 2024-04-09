import serial
import random
import argparse
import signal
import sys
import time

# Serial connections
nRF_ser = None
uart_ser = None

nRF_port="COM6"
# it is my sync_calibration code
# binary_image="D:/Work/atomic/lighthouse_position/reference/scum-test-code/scm_v3c/applications/synclight_carlibration/Objects/synclight_calibration.bin"
# ble-tx
# binary_image="D:\Work/atomic/lighthouse_position/develop_sync_clock/dev/tryuan99_scum-test-code/scum-test-code/scm_v3c/applications/ble_tx/Objects/ble_tx.bin"
# 获得合适的BLE频率


# yoga pro 14s 上的地址
# C:/Users/cwdbo/work/TRY_LIGHTHOUSE/scum-test-code/scm_v3c/applications/ble_tx/Objects
binary_image="C:/Users/cwdbo/work/TRY_LIGHTHOUSE/scum-test-code/scm_v3c/applications/ble_tx/Objects/ble_tx.bin"
# binary_image="D:\Work/atomic/lighthouse_position/develop_sync_clock/dev/tryuan99_scum-test-code/scum-test-code/scm_v3c/applications/ble_freq_sweep/Objects/ble_freq_sweep.bin"

# binary_image="D:\Work/atomic/lighthouse_position/develop_sync_clock/dev/tryuan99_scum-test-code/scum-test-code/scm_v3c_BLE/code.bin"
# binary_image="D:/Work/atomic/lighthouse_position/reference/scum-test-code/scm_v3c/applications/hello_world/Objects/hello_world.bin"
# binary_image="C:/Users/fmaksimo/scum/austin_repo/scum-test-code/scm_v3c/applications/freq_sweep_rx_tx/Objects/freq_sweep_rx_tx.bin"
#binary_image="C:/Users/fmaksimo/scum/scum-test-code/scm_v3c/applications/ble_freq_sweep/Objects/ble_freq_sweep.bin"
#binary_image="C:/Users/fmaksimo/scum/scum-hornet/scm_v3c/applications/ble_freq_sweep/Objects/ble_freq_sweep.bin"
boot_mode='3wb'
pad_random_payload=False

# Open COM port to nRF
nRF_ser = serial.Serial(
    port=nRF_port,
    baudrate=250000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS)
    
# Open binary file from Keil
with open(binary_image, 'rb') as f:
    bindata = bytearray(f.read())
    
bindata2 = bytearray()
# Need to know how long the binary payload to pad to 64kB
code_length = len(bindata) - 1
pad_length = 65536 - code_length - 1

#print(code_length)

# Optional: pad out payload with random data if desired
# Otherwise pad out with zeros - uC must receive full 64kB
if(pad_random_payload):
    for i in range(pad_length):
        bindata.append(random.randint(0,255))
    code_length = len(bindata) - 1 - 8
else:
    for i in range(pad_length):
        bindata.append(0)
        
        
# Transfer payload to nRF
#nRF_ser.write(b'transfersram\n')
#print(nRF_ser.read_until())
# Send the binary data over uart
nRF_ser.write(bindata)
# and wait for response that writing is complete
print(nRF_ser.read_until())

# Execute 3-wire bus bootloader on nRF
#nRF_ser.write(b'boot3wb\n')

# Display 3WB confirmation message from nRF
print(nRF_ser.read_until())
