from serial.tools import list_ports







# Find msp432 launchpad port
def find_launchpad_port():
    TI_VID = 0x0451
    XDS110_PID = 0xbef3 # XDS110PID
    for port in list_ports.comports():
        if port.vid == TI_VID and port.pid == XDS110_PID:
            return port.device
    return None

# # Main communication function
# def serial_communication():
#     port = find_launchpad_port()
#     if not port:
#         print("MSP432 Launchpad not found!")
#         return
#     try:
#         # Configure serial port
#         ser = serial.Serial(
#             port=port,
#             baudrate=115200,
#             bytesize=serial.EIGHTBITS,
#             parity =serial.PARITY_NONE,
#             stopbits = serial.STOPBITS_ONE,
#             timeout = 0.1
#         )
#         print(f"Connected to {ser.name}")
#         print("type commands(press ESC to exit):")
#         ser.reset_input_buffer()
#         time.sleep(0.1)

#         setup_terminal()

#         def read_from_port():
#             while running:
#                 try:
#                     if ser.in_waiting > 0:
#                         data = ser.read(ser.in_waiting)
#                         sys.stdout.write(data.decode('utf-8'))
#                         sys.stdout.flush()
#                 except:
#                     break
#                 time.sleep(0.01)

#         running = True
#         reader = threading.Thread(target = read_from_port, daemon=True)
#         reader.start()

#         # main write Loop
#         try:
#             listener = keyboard.Listener(on_release=on_key_release)
#             listener.start()
#             while running:

#                 # key = get_key()
#                 # if key:
#                 #     if key == '\x1b':
#                 #         running = False
#                 #         break
#                 #     ser.write(key.encode('utf-8'))
#                 # time.sleep(0.01)


#                 if(writing_queue.qsize()!= 0):
#                     next = writing_queue.get(block=False)
#                     ser.write((next + "\0").encode('ascii'))
#         finally:
#             restore_terminal()
#     except serial.SerialException as e:
#         print(f"serial error: {e}")
#     finally:
#         running = False
#         if 'ser' in locals() and ser.is_open:
#             ser.close()
#         print("Disconnected")


# # serial_communication()
