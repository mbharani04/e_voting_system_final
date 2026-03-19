import cv2
import tkinter.messagebox as messagebox
import access
import properties
import serial
import serial.tools.list_ports
import time



class ScanQr:
    def start_scanner(self,voter_id):

            generated_id = voter_id

            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0 = default camera
            detector = cv2.QRCodeDetector()

            if not cap.isOpened():
                messagebox.showerror("Error", "Cannot open camera")
                return

            try:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    data, bbox, _ = detector.detectAndDecode(frame)
                    if data:
                        scanned_data = data.strip().upper()
                        print("Scanned:", scanned_data)
                        if scanned_data == generated_id:
                            try:
                                connection, cursor = access.dbUtils.get_connection(self)
                                cursor.execute(properties.update_scanner_on, {"voter_id": scanned_data})
                                connection.commit()

                                # Send signal to Arduino side when scan is successful
                                try:
                                    arduino_port = ScanQr.find_arduino_port(self)

                                    if arduino_port is None:
                                        print("Arduino not found!")
                                    else:
                                        print(f"Arduino found on {arduino_port}")
                                        ser = serial.Serial(arduino_port, 9600, timeout=1)
                                        time.sleep(2)  # Wait for Arduino to reset
                                        ser.write(b"{}".format(properties.arduino_data))                           

                                        print("Arduino signal sent: x")
                                except Exception as arduino_err:
                                    print("Arduino signal failed:", arduino_err)
                                    return arduino_err
                            except Exception as e:
                                print("Scanner DB update error:", e)
                                return e
                            finally:
                                access.dbUtils.close_connection(self)

                            messagebox.showinfo("Success", "QR Matched! Scanner updated and signal sent")
                            return 1

                    cv2.imshow("Scanner - Press Q to Quit", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            finally:
                cap.release()
                cv2.destroyAllWindows()


    def find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # Check for Arduino in description (works in most cases)
            if "Arduino" in port.description or "CH340" in port.description or "USB Serial" in port.description:
                return port.device
        return None