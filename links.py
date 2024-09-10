import tkinter as tk
from tkinter import ttk, messagebox
import serial.tools.list_ports
import serial
import time

# Function to list available COM ports
def list_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Function to connect to the selected COM port and send command
def send_command(command):
    try:
        selected_port = com_port_var.get()
        if selected_port:
            ser = serial.Serial(
                port=selected_port, 
                baudrate=115200, 
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            
            if ser.is_open:
                print(f"Connected to {ser.port}")
                ser.write(command.encode())
                time.sleep(0.5)
                response = ser.read(ser.in_waiting)
                if response:
                    print("Response from arm:", response.decode())
                else:
                    print("No response received.")
                ser.close()
            else:
                raise serial.SerialException(f"Could not open {selected_port}.")
        else:
            raise ValueError("No port selected.")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect or send command: {e}")

# Command to send current set position
def send_current_position():
    current_position_command = "arm.set_position((0,-163,142),5000)\r\n"
    send_command(current_position_command)

# Command to send new position (163,0,142)
def send_new_position():
    new_position_command = "arm.set_position((163,0,142),5000)\r\n"
    send_command(new_position_command)

# Initialize GUI window
root = tk.Tk()
root.title("COM Port Selector and Commands")

# Dropdown to select COM port
com_port_var = tk.StringVar()
com_ports = list_ports()
com_port_dropdown = ttk.Combobox(root, textvariable=com_port_var, values=com_ports)
com_port_dropdown.set("Select COM Port")
com_port_dropdown.pack(pady=10)

# Button to send current set position command
current_position_button = tk.Button(root, text="Send Current Set Position", command=send_current_position)
current_position_button.pack(pady=10)

# Button to send new position command
new_position_button = tk.Button(root, text="Send New Position", command=send_new_position)
new_position_button.pack(pady=10)

# Run the GUI event loop
root.mainloop()

