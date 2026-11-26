# 市場面板（GitHub Pages / 手機 PWA）

## 發布方式
1. 在 GitHub 建立一個新的 repository（例如 `market-panel`）。
2. 將本資料夾內的所有檔案與 `icons` 資料夾一起上傳到 repository 根目錄。
3. 進入 repository 的 **Settings → Pages**。
4. 在 **Build and deployment** 選 `Deploy from a branch`，Branch 選 `main`、資料夾選 `/ (root)`，按 Save。
5. 等待 GitHub Pages 發布完成，使用 GitHub 顯示的網址開啟。

## 手機加入主畫面
- iPhone：用 Safari 開啟網站 → 分享 →「加入主畫面」。
- Android：用 Chrome 開啟網站 → 右上角選單 →「安裝應用程式」或「加入主畫面」。

## 功能與離線說明
- 原有報價群組、4 個迷你圖、台北時間、紅漲綠跌、深淺色、重新載入及設定保存均保留。
- 手機版調整為單欄圖表與較大的觸控按鈕。
- PWA 會快取頁面外殼，網路中斷時可開啟頁面框架；TradingView 報價/圖表本身仍需網路，離線時不會更新。
- 本專案不需要自建 API 或後端；GitHub Pages 免費靜態託管即可。
