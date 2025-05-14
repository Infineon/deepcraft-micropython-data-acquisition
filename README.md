# DEEPCRAFT™ Studio Data Acquisition using MicroPython

This repository offers a comprehensive framework for streaming sensor data, such as audio from PDM microphones, over WiFi using MicroPython. The captured data can be seamlessly integrated into [DEEPCRAFT™ Studio](https://www.imagimob.com/studio) for further processing, labeling, and model training.

## Supported Boards

- CY8CKIT-062S2-AI

## Pre-requisites
1. A PSOC™ 6-based device with MicroPython firmware installed. Refer to our [installation guide](https://ifx-micropython.readthedocs.io/en/latest/psoc6/installation.html) for detailed instructions.

2. Clone and set up the Capture Server repository by following the instructions provided in the [Capture Server documentation](https://bitbucket.org/imagimob/captureserver/src/master/).

3. Clone this repository:
    ```bash
    git clone https://github.com/Infineon/deepcraft-micropython-data-acquisition.git
    ```
4. Install [DEEPCRAFT™ Studio](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.deepcraftstudio) 

## Usage
1. Open the cloned repository in a MicroPython-supported IDE, such as [Thonny](https://thonny.org/), and update the `config.py` file with your WiFi credentials:
    
    ```bash
    SSID = "your wifi name"
    PASSWORD = "your wifi password"
    ```
2. Transfer all source files to the device by right-clicking on the project folder and selecting "Upload to /".

    ![Alt text](docs/images/transfer_to_device.png)

    After completing the upload, all the source files will be visible in the filesystem of your MicroPython edge device.

    ![Alt text](docs/images/lib_on_device.png)

2. Open a command prompt, navigate to the root directory of the cloned Capture Server repository, and then change to the `examples/generic` folder:
    
    ```bash
    cd examples/generic
    ```

3. Execute the following command, ensuring you replace the placeholders with the appropriate values for your setup:
    
    ```bash
    python generic_local_capture_interface.py --output-dir "Your output directory" --protocol TCP --ip-address "Your board's IP address" --port 5000  --data-format ".data or .wav" --data-type h --samples-per-packet 512 --features 1 --sample-rate 16000 --video-disabled.
    ```
    For explanation on each of the parameters, please check the [Capture Server documentation](https://bitbucket.org/imagimob/captureserver/src/master/).

    The recorded data will be stored in the output directory mentioned above.

4. Launch DEEPCRAFT™ Studio and create a new project or open an existing one. Go to the DATA tab, click on the *Add Data* button, and choose the output directory containing the captured `.wav` or `.data` files along with their corresponding label files.

    ![Alt text](docs/images/training_add_data.png)

5. After selecting the output directory, DEEPCRAFT™ Studio will automatically import the audio/data files and their corresponding label files into a new data session.

    ![Alt text](docs/images/training_data_view.png)

6. After creating the data session, your dataset will be accessible within DEEPCRAFT™ Studio, ready for preprocessing, labeling, and training machine learning models. 🚀

    ![Alt text](docs/images/training_data_session.png)

## Add your own Sensor
Want to stream data from a different sensor? The integration is straight forward — just implement a few standard methods in your sensor driver to work seamlessly with the capture script.

### Sensor Driver Interface
Every sensor must have its own sensor driver file (e.g. `pdm_pcm.py`) which must define the following methods: 

| Method                 | Description                                                                 | Input Args                  | Return Type                 |
|------------------------|-----------------------------------------------------------------------------|-----------------------------|-----------------------------|
| `__init__()`           | Set the default parameters for the sensor.                                  | `self`                      | `None`                      |
| `init()`               | Initialize the sensor hardware (e.g. I2C or SPI setup).                     | `self`                      | `None`                      |
| `get_buffer()`         | Return the internal buffer used to store captured sensor samples.           | `self`                      | `List[int]` / `List[float]` |
| `get_format()`         | Specify how data should be packed for the transmission.                     | `self`                      | `Tuple[str, str]`           |
| `read_samples(buffer)` | Capture data into the provided buffer in-place.                             | `self`, `buffer: List`      | `None`                      |
| `deinit()`             | Power down the sensor and release any used resources.                       | `self`                      | `None`                      |


With the interface defined, just import your new sensor in the `data_acquisition.py` script and define your sensor config in the `main` block. 
1. For PDM microphones, we configure it as:

```python
config = {
    "clk_pin": "P10_4",
    "data_pin": "P10_5",
    "sample_rate": 16000,
    "gain": 20,
    "buffer_size": 512,
    }
```

## Contributing Guide
Please do not hesitate to share your sensor integration with the community! Open a [Pull Request](https://github.com/Infineon/deepcraft-micropython-data-acquisition/pulls) with your `sensors/sensor_name.py` and an example configuration in the `README.md`. 🙌