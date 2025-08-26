import threading
import time
import socket
def iframe_thread(port):
  while True:
      time.sleep(0.5)
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      result = sock.connect_ex(('127.0.0.1', port))
      if result == 0:
        break
      sock.close()
  from google.colab import output
  output.serve_kernel_port_as_iframe(port, height=1024)
  print("to open it in a window you can open this link here:")
  output.serve_kernel_port_as_window(port)

threading.Thread(target=iframe_thread, daemon=True, args=(8188,)).start()

!python main.py --dont-print-server
