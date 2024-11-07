import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import curses

# Configuration
serial_port = '/dev/ttyUSB0'  # Update this to your actual serial port
baud_rate = 9600
timeout = 1  # Timeout for serial communication

# Initialize serial communication
ser = serial.Serial(serial_port, baud_rate, timeout=timeout)

def send_duty_cycles(duty_cycle1, duty_cycle3):
    # Send duty cycle values to the Beetle
    message = f"{duty_cycle1},{duty_cycle3}\n"
    ser.write(message.encode())

def read_rpm_values():
    # Read RPM values from the Beetle
    if ser.in_waiting > 0:
        line = ser.readline().decode().strip()
        if line:
            rpm_values = line.split(',')
            if len(rpm_values) == 6:
                rpm1, rpm1_avg, rpm2, rpm2_avg, rpm3, rpm3_avg = map(int, rpm_values)
                return rpm1, rpm1_avg, rpm2, rpm2_avg, rpm3, rpm3_avg
    return None

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Initialize plot data
    x = np.arange(0, 100, 1)
    y1 = np.zeros(100)
    y2 = np.zeros(100)
    y3 = np.zeros(100)

    try:
        while True:
            # Example: Send duty cycle values
            duty_cycle1 = int(input("Enter duty cycle for Pump 1/2 (0-255): "))
            duty_cycle3 = int(input("Enter duty cycle for NMR Pump (0-255): "))
            send_duty_cycles(duty_cycle1, duty_cycle3)

            # Wait for a moment to receive data
            time.sleep(1)

            # Read and print RPM values
            rpm_values = read_rpm_values()
            if rpm_values:
                rpm1, rpm1_avg, rpm2, rpm2_avg, rpm3, rpm3_avg = rpm_values
                print(f"Pump 1 RPM: {rpm1}, Avg: {rpm1_avg}")
                print(f"Pump 2 RPM: {rpm2}, Avg: {rpm2_avg}")
                print(f"NMR Pump RPM: {rpm3}, Avg: {rpm3_avg}")

                # Update plot data
                y1 = np.roll(y1, -1)
                y2 = np.roll(y2, -1)
                y3 = np.roll(y3, -1)
                y1[-1] = rpm1
                y2[-1] = rpm2
                y3[-1] = rpm3

                # Clear and redraw plot
                stdscr.clear()
                stdscr.addstr(0, 0, "Pump 1 RPM: " + str(rpm1))
                stdscr.addstr(1, 0, "Pump 2 RPM: " + str(rpm2))
                #stdscr.addstr(2, 0, "NMR Pump RPM: " + str(rpm3))

                for i in range(100):
                    stdscr.addstr(4 + int(y1[i] / 10), i, '*')
                    stdscr.addstr(4 + int(y2[i] / 10), i, '+')
                    #stdscr.addstr(4 + int(y3[i] / 10), i, 'o')

                stdscr.refresh()

    except KeyboardInterrupt:
        print("Communication interrupted.")

    finally:
        ser.close()

# Run the curses application
curses.wrapper(main)