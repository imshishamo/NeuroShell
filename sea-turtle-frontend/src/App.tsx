import { useState } from 'react'
import './App.css'

// 定義預測結果的類型
interface PredictionResults {
  model_A_results: string[];
  model_B_results: string[];
  model_C_results: string[];
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [filePath, setFilePath] = useState<string>("")
  const [imageUrl, setImageUrl] = useState<string>("")
  const [prediction, setPrediction] = useState<PredictionResults | null>(null)  // 用來儲存預測結果

  // 處理檔案選擇
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files ? e.target.files[0] : null
    if (selectedFile) {
      setFile(selectedFile)
      setFilePath(selectedFile.name)

      // 顯示圖片預覽
      const objectUrl = URL.createObjectURL(selectedFile)
      setImageUrl(objectUrl)
    }
  }

  // 提交圖片並獲得預測結果
  const handleSubmit = async () => {
    if (!file) {
      alert("請選擇一個檔案！")
      return
    }

    const formData = new FormData()
    formData.append("file", file)

    // 發送圖片到後端進行預測
    const response = await fetch("http://localhost:8000/predict/", {
      method: "POST",
      body: formData,
    })

    const data = await response.json()

    // 印出收到的 JSON response
    console.log("Received data from backend:", data)

    // 顯示預測結果
    setPrediction(data)
  }

  return (
    <div>
      <h1>Turtle Image Identification</h1>

      <div className="container">
        {/* 左側部分：圖片上傳、預覽、按鈕 */}
        <div className="left">
          {/* 檔案選擇 */}
          <input type="file" onChange={handleFileChange} />

          {/* 顯示選擇的檔案名稱 */}
          {filePath && <p>選擇的檔案: {filePath}</p>}

          {/* 顯示圖片預覽 */}
          {imageUrl && (
            <div>
              <h2>圖片預覽 Preview:</h2>
              <img src={imageUrl} alt="Preview" width={300} />
            </div>
          )}

          {/* 提交並獲得預測結果 */}
          <button onClick={handleSubmit}>Upload and Predict</button>
        </div>

        {/* 右側部分：預測結果 */}
        <div className="right">
          {/* 顯示預測結果 */}
          {prediction && (
            <div>
              <h2> 預測結果 Result</h2>
              <h3> A_Species:</h3>
              <ul>
                {prediction.model_A_results.map((result, index) => (
                  <li key={index}>{result}</li>
                ))}
              </ul>
              <h3> B_Scute number under eye:</h3>
              <ul>
                {prediction.model_B_results.map((result, index) => (
                  <li key={index}>{result}</li>
                ))}
              </ul>
              <h3> C_Facial scute pattern:</h3>
              <ul>
                {prediction.model_C_results.map((result, index) => (
                  <li key={index}>{result}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
