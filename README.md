# DEEPCRAFT™ Micropython Data Acquisition

This repository provides a framework to stream sensor data like audio from PDM microphones over WiFi using MicroPython.

## Tested Boards:

- CY8CKIT-062S2-AI

## Pre-requisites
1. PSoC6 based device flashed with MicroPython firmware. Check the [mpy-psoc6.py utility](https://ifx-micropython.readthedocs.io/en/latest/psoc6/installation.html) to do so.

2. Clone the captureserver repo:
    
    git clone https://bitbucket.org/imagimob/captureserver/src/master/ 
    
and follow the instruction to setup.


## 2. Sensor data acquisition
1. In TCP-mpy.py script add your Wifi name and password  to use your wifi to transfer the data:
    ```bash
    SSID = "your wifi name"
    PASSWORD = "your wifi password"
    ```
2. In capture server cloned repo  move to generic folder using 
    ```bash
    cd examples/generic
    ```
3. Specific commands for each demo ,TCP :
    ```bash
    python generic_local_capture_interface.py --output-dir "mention the output dir" --protocol TCP --ip-address 192.168.0.108 --port 5000  --data-format .wav --data-type h --samples-per-packet 512 --features 1 --sample-rate 16000 --video-disabled.
    ```
The data will be stored in the output directory mentioned .

## 3. Importing to studio:

1. Now open the Deepcraft Studio .Create a new project / open a project.And click the add data button inside the DATA tab  and choose the output directory in which you saved the files .

    ![Alt text](docs/demo_images/tcpaddata1.png)

2. you should see an audio and label file session automatically selected.

    ![Alt text](docs/demo_images/tcpaddata2.png)

3. After successful adding you can see the data session created inside the studio.Now you can get your data inside the studio and start training the model.

    ![Alt text](docs/demo_images/tcpdata3.png)
