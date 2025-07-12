import tkinter as tk
from tkinter import ttk

import serial
import time
import queue
import threading
from serial.tools import list_ports
# Find msp432 launchpad port
def find_launchpad_port():
    TI_VID = 0x0451
    XDS110_PID = 0xbef3 # XDS110PID
    for port in list_ports.comports():
        if port.vid == TI_VID and port.pid == XDS110_PID:
            return port.device
    return None


separator = '\n'
class UartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Panel")

        # Connection status frame
        self.connection_frame = ttk.LabelFrame(root, text="Connection Status",padding = 10)
        self.connection_frame.grid(row=0,column=0,padx=10,pady=10,sticky="ew")

        self.connection_status = ttk.Label(self.connection_frame,text="Disconnected", foreground="red")

        self.connection_status.pack()

        # Message display frame
        self.message_frame = ttk.LabelFrame(root,text='Messages',padding=10)
        self.message_frame.grid(row =1, column = 0, padx=10,pady=10,sticky="ew")

        self.message_display = ttk.Label(self.message_frame,text="No messages",wraplength=300)
        self.message_display.pack()

        #Button grid frame
        self.button_frame = ttk.LabelFrame(root,text="Controls",padding=10)
        self.button_frame.grid(row=2,column=0,padx=10,pady=10)
        # Create buttons in a grid layout
        buttons = [
            ("Up", self.on_up, 0, 1),
            ("Left", self.on_left, 1, 0),
            ("Right", self.on_right, 1, 2),
            ("Down", self.on_down, 2, 1),
            ("Button A", self.on_button_a, 1, 3),
            ("Button B", self.on_button_b, 2, 3),
            ("Joystick Select", self.on_joystick_select, 1, 1)
        ]

        for label,command,row,col in buttons:
            button = ttk.Button(self.button_frame,text=label,command=command)
            button.grid(row=row,column=col,padx=5,pady=5,ipadx=10,ipady=5)

        #init connection status
        self.running = True

        self.writing_queue = queue.Queue()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.init_connection()

    def on_up(self):
        """write up to uart"""
        self.writing_queue.put("CONTROLLER:UP")
    def on_down(self):
        """write down to uart"""
        self.writing_queue.put("CONTROLLER:DOWN")
    def on_left(self):
        """write left to uart"""
        self.writing_queue.put("CONTROLLER:LEFT")
    def on_right(self):
        """write right to uart"""
        self.writing_queue.put("CONTROLLER:RIGHT")
    def on_button_a(self):
        """write button a to uart"""
        self.writing_queue.put("CONTROLLER:BUTTON_A")

    def on_button_b(self):
        """write button b to uart"""
        self.writing_queue.put("CONTROLLER:BUTTON_B")
    def on_joystick_select(self):
        """write select to uart"""
        self.writing_queue.put("CONTROLLER:SELECT")
    def display_message(self,message):
        def update():
                self.message_display.config(text=message)
        self.root.after(0, update)


#########################################################################
    def init_connection(self):
        self.port = find_launchpad_port()
        # self.port = '/dev/tty.usbmodem101'
        if not self.port:
            self.connection_status.config(text="MSP432 Launchpad not found!")
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1
            )
            self.connection_status.config(text=f"Connected to {self.ser.name}")
            self.ser.reset_input_buffer()
            time.sleep(0.1)



            self.reader = threading.Thread(target=self.read_from_port)
            self.reader.start()

            self.writer = threading.Thread(target=self.write_to_port)
            self.writer.start()

        except serial.SerialException as e:
            self.display_message(f"serial error: {e}")
#########################################################################

    def read_from_port(self):
        buffer = bytearray()
        while self.running:

            try:
                if self.ser.in_waiting >0:
                    data=self.ser.read(self.ser.in_waiting)
                    buffer.extend(data)
                    #self.display_message("current " +buffer.decode('ascii'))
                    if b'\0' in buffer:
                        message, _, remaining = buffer.partition(b'\0')

                        if message:
                            self.display_message(message.decode('ascii'))
                        buffer = remaining
            except :
                #self.display_message("error has occured while reading")
                continue
            time.sleep(0.01)
    def write_to_port(self):
        global separator
        while self.running:
            try:
                next = self.writing_queue.get(timeout=0.1)

                next = next + separator

                self.ser.write(next.encode('ascii'))
            except:
                #self.display_message("error has occured while writing")
                continue
    def on_close(self):
        self.running= False
        if(hasattr(self,'reader')):
            self.reader.join()
        if(hasattr(self,'writer')):
            self.writer.join()
        if (hasattr(self,'ser') and self.ser.is_open):
            self.ser.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UartApp(root)
    root.mainloop()
