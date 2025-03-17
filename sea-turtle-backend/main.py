from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
import cv2
import numpy as np
from ultralytics import YOLO

app = FastAPI()

# 設置 CORS 設定
origins = [
    "http://localhost:5173",  # 允許來自這個來源的請求
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允許的來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法 (GET, POST 等)
    allow_headers=["*"],  # 允許所有請求標頭
)

# 設定裝置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用裝置: {device}")

# 加載 YOLO 模型
model_A = YOLO('C:/Users/user/Desktop/Sophia/yolov8/runs/detect/A_class/train/weights/best.pt', verbose=False).to(device)
model_B = YOLO('C:/Users/user/Desktop/Sophia/yolov8/runs/detect/B_class/train4/weights/best.pt', verbose=False).to(device)
model_C = YOLO('C:/Users/user/Desktop/Sophia/yolov8/runs/detect/C_class/train3/weights/best.pt', verbose=False).to(device)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # 讀取圖片
    image = Image.open(io.BytesIO(await file.read()))
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # 轉換顏色通道順序

    # 使用 YOLOv8 進行推理
    # 第一層分類 (A)
    pred_A = model_A(img, verbose=False)
    A_results = []
    if pred_A[0].boxes:
        for box in pred_A[0].boxes:
            cls = int(box.cls.cpu().numpy())  # 取得類別索引
            cls_name = ['Green_sea_turtle', 'Hawksbill_turtle'][cls]
            A_results.append(f"A 分類結果: {cls_name}")

    # 第二層分類 (B)
    pred_B = model_B(img, verbose=False)
    B_results = []
    if pred_B[0].boxes:
        for box in pred_B[0].boxes:
            cls_B = int(box.cls.cpu().numpy())
            cls_name_B = ['3_scales', '4_scales', '5_scales'][cls_B]
            B_results.append(f"B 分類結果: {cls_name_B}")

    # 第三層分類 (C)
    pred_C = model_C(img, verbose=False)
    C_results = []
    if pred_C[0].boxes:
        for box in pred_C[0].boxes:
            cls_C = int(box.cls.cpu().numpy())
            cls_name_C = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6'][cls_C]
            C_results.append(f"C 分類結果: {cls_name_C}")

    # 返回預測結果
    return JSONResponse({
        "model_A_results": A_results,
        "model_B_results": B_results,
        "model_C_results": C_results,
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
