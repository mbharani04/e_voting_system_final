import qrcode
from PIL import Image
import customtkinter as ctk
import os
import properties
import access
import time
import cv2
from tkinter import messagebox


class qrGeneratorService:
    def generate_qr(self,voter_id):
        print(self.voter_id)
        os.makedirs("qr_codes", exist_ok=True)
        file_path = f"qr_codes/{self.voter_id}.png"

        qr = qrcode.make(self.voter_id)
        qr.save(file_path)
        print(self.voter_id)
        connection,cursor = access.dbUtils.get_connection(self) #db connection
        cursor.execute(properties.update_qr_status, {"voter_id": self.voter_id}) #query connection
        connection.commit()
        return file_path 
        access.dbUtils.close_connection(self)

    def printQrService(self,voter_id,file_path):
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "QR Code not found. Generate QR first.")
            return 0

        try:
            # Opens system print dialog
            os.startfile(file_path, "print")
            # Step-by-step logic: Only scan after clicking OK
            #if messagebox.askokcancel("Print", "Printing started. Click OK to open scanner."):
            time.sleep(4)
            return 1
        except Exception as e:
            messagebox.showerror("Print Error", str(e))
            return 0

        
            
    
