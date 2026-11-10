# 露營平配

露營裝備配置工具：營位與帳篷內的 2D／3D 配置，包含真實尺寸的 3D 模型。

- 網站：用 GitHub Pages 發布，直接打開 `index.html` 即可。
- `data/seed.json`：預設的裝備與配置圖（第一次開啟時載入）。
- `models/`：裝備的 3D 模型（.glb）。
- `vendor/`：Three.js r147。

修改會即時存到雲端（Firebase，集合名稱 campplan_*），有網址的人都能編輯；手機沒訊號時會先存在這台裝置，連上網路後自動上傳。網址加上 `?view=<配置圖 id>` 是只能觀看的分享連結。

`index.html` 是網站的主要原始檔，直接修改它即可。
