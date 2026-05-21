# TODOList列表工具
TODOList列表工具，基于Python3.9和PyQt制作的可视化窗口列表工具。
A visual window list tool based on Python 3.9 and PyQt for creating TODO lists.

工具下载：https://github.com/TaChangFeng/TODOList/releases/tag/v1.0

# 📌 TODOList v1.0.0 — 更新日志（Release Notes）

## 🎉 版本说明
TODOList v1.0.0 是该项目的首个正式可执行版本，支持 Windows 平台独立运行，无需安装 Python 环境。  
本版本包含完整的任务管理、提醒系统、界面交互与数据持久化功能。

---

## ✨ 新增功能（New Features）

### 🟦 主界面（menu.py）
- 背景图支持（pic2.jpg）  
- “开始使用 / 项目说明 / 退出程序” 三大入口  

### 🟦 任务管理系统（main.py）
- 添加任务  
- 修改任务  
- 删除任务  
- 搜索任务  
- 按状态筛选（TODO / 正在进行 / 已完成 / 删除）  
- 任务说明编辑区  
- 系统提示区  

### 🟦 任务提醒系统（timewindow）
- 支持设置任务开始与结束提醒时间  
- 到点自动提醒  
- 支持“结束”或“推迟”操作  
- 推迟可自定义分钟数  
- 提醒信息同步写入系统提示区  

### 🟦 音频提醒（bgm.mp3）
- 使用 QMediaPlayer 播放提醒音  
- 支持多次触发  

### 🟦 数据持久化（datafile.txt）
- 自动保存任务列表  
- 程序重启后自动加载  
- 使用 pickle 与文本双格式  

### 🟦 使用说明（Text2.txt / Text3.txt）
- 主界面项目说明  
- 主窗口使用说明  
- 支持弹窗展示  

---

## 🛠 改进内容（Improvements）

### ✔ 全面支持 PyInstaller 打包
- 所有静态文件改为 `resource_path()` 读取  
- 解决 EXE 环境下路径失效问题  
- 支持单文件打包（-F）  
- 支持无控制台模式（-w）  

### ✔ 静态资源统一管理
以下文件已正确加入打包资源：

| 文件名 | 用途 |
|--------|------|
| pic2.jpg | 背景图 |
| bgm.mp3 | 提醒音 |
| mainwindowUI.ui | UI 文件 |
| datafile.txt | 数据文件 |
| Text2.txt | 主界面说明 |
| Text3.txt | 使用说明 |


---

## 🚀 运行环境（Runtime）

- Windows 10 / 11  
- 无需 Python 环境  
- 双击即可运行  

---

