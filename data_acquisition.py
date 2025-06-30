# main.py
import struct
import network_utils
from network_utils import connect_wifi
from tcp_server import create_server_socket
from sensors.pdm_pcm import PDM_PCM  # swap this out for any other sensor
import time

SYNC_DELAY = 0.1

def main(sensor):
    ip = connect_wifi()
    server_socket = create_server_socket(ip)

    sensor.init()
    rx_buf = sensor.get_buffer()
    endianness, fmt_str = sensor.get_format()
    full_format = f"{endianness}{len(rx_buf)}{fmt_str}"

    print("Waiting for capture-server to connect...")
    conn, addr = server_socket.accept()
    print(f"capture-server connected from {addr}")

    try:
        while True:
            sensor.read_samples(rx_buf)
            packet = struct.pack(full_format, *rx_buf)
            conn.sendall(packet)
            time.sleep(SYNC_DELAY)
    except OSError as e:
        print("Connection error:", e)
    finally:
        conn.close()
        server_socket.close()
        sensor.deinit()
        print("\nStreaming stopped.")

if __name__ == "__main__":
    config = {
        "clk_pin": "P10_4",
        "data_pin": "P10_5",
        "sample_rate": 16000,
        "gain": 20,
        "buffer_size": 512,
    }

    sensor = PDM_PCM(config=config)
    main(sensor)