# import os
# import qrcode
# import cv2
# import access
# import properties
# from tkinter import messagebox

# def start_scanner(expected_id):
#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     detector = cv2.QRCodeDetector()

#     if not cap.isOpened():
#         messagebox.showerror("Error", "Cannot open camera")
#         return

#     connection, cursor = access.dbUtils.get_connection(None)
#     if connection is None or cursor is None:
#         messagebox.showwarning("Warning", "DB connection unavailable. Scan still works but scanned_on won't be updated.")

#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             data, bbox, _ = detector.detectAndDecode(frame)

#             if data:
#                 scanned = data.strip().upper()
#                 print("Scanned:", scanned)

#                 if scanned == expected_id:
#                     messagebox.showinfo("Success", "QR Matched")
#                     if connection and cursor:
#                         try:
#                             cursor.execute(properties.update_scanner_on, {"voter_id": expected_id})
#                             connection.commit()
#                         except Exception as e:
#                             print("DB update failed:", e)
#                             messagebox.showwarning("Warning", "QR matched but scanned_on update failed.")
#                     break

#             cv2.imshow("Scanner (Press Q to exit)", frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#     finally:
#         cap.release()
#         cv2.destroyAllWindows()
#         if connection and cursor:
#             cursor.close()
#             connection.close()