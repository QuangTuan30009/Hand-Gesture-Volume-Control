import cv2
import mediapipe as mp
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Khởi tạo MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Khởi tạo điều khiển âm lượng
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Lấy phạm vi âm lượng (min và max decibel)
min_vol, max_vol, _ = volume.GetVolumeRange()  # min_vol ≈ -65.25, max_vol ≈ 0.0

# Mở webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển sang RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Lấy vị trí ngón cái và ngón trỏ
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]

            # Chuyển đổi tọa độ từ tỷ lệ (0-1) sang pixel
            h, w, _ = frame.shape
            thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
            index_x, index_y = int(index.x * w), int(index.y * h)

            # Tính khoảng cách
            distance = math.sqrt((thumb.x - index.x)**2 + (thumb.y - index.y)**2)

            # Ánh xạ khoảng cách thành âm lượng (1 đến 100)
            vol_percentage = min(max(distance * 200, 1), 100)  # Nhân 200 để điều chỉnh độ nhạy
            vol_db = min_vol + (max_vol - min_vol) * (vol_percentage / 100)  # Chuyển thành decibel
            volume.SetMasterVolumeLevel(vol_db, None)

            # Vẽ đường nối giữa ngón cái và ngón trỏ
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 2)

            # Hiển thị khoảng cách và mức âm lượng
            cv2.putText(frame, f"Khoang cach: {distance:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Am luong: {int(vol_percentage)}%", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Vẽ điểm mốc tay
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Điều khiển âm lượng bằng cử chỉ', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()