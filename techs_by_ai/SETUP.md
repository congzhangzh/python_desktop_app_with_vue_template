# 项目设置指南

## 环境准备

### 0. Install Mamba?
TBD

### 1. 创建 Mamba 环境
```bash
# 创建环境
mamba create -n desktop_app_by_webview python=3.11

# 激活环境
mamba activate desktop_app_by_webview

# 安装 PySide6
mamba install pyside6

# 安装其他 Python 依赖
pip install -r requirements.txt
```

### 2. 前端依赖安装
```bash
cd frontend
npm install
cd ..
```

## 开发模式

### VS Code 调试（推荐）
1. 打开项目根目录
2. 确保已激活 `desktop_app_by_webview` 环境
3. 按 F5 选择 "🚀 Dev Mode (Frontend + Python)"
4. 自动启动前端开发服务器 + Python 应用

### 手动启动
```bash
# 终端1：启动前端开发服务器
cd frontend
npm run dev

# 终端2：启动 Python 应用
mamba activate desktop_app_by_webview
python main.py
```

## 生产构建

### 使用构建脚本
```bash
# Linux/macOS
./scripts/build.sh

# Windows
.\scripts\build.cmd
```

### 手动构建
```bash
# 1. 构建前端
cd frontend
npm run build
cd ..

# 2. 打包 Python 应用
pyinstaller --name=DesktopApp \
    --windowed \
    --onedir \
    --add-data "frontend/dist:frontend/dist" \
    main.py
```

## 调试模式说明

### 环境检测机制
- **开发模式**：检测 `http://localhost:5173` 是否可用
  - 可用：加载开发服务器（热重载）
  - 不可用：回退到本地 dist 文件

- **生产模式**：直接加载 `frontend/dist/index.html`

### VS Code 配置
- **🚀 Dev Mode**: 自动启动前端 dev server + Python
- **🏗️ Production Mode**: 先构建前端，再启动 Python
- **🐍 Python Only**: 仅启动 Python（用于调试后端逻辑）

## 故障排除

### 常见问题
1. **PySide6 导入失败**
   ```bash
   mamba activate desktop_app_by_webview
   mamba install pyside6
   ```

2. **前端构建失败**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **WebView 空白页面**
   - 检查前端是否构建成功（`frontend/dist/index.html` 存在）
   - 检查开发服务器是否启动（`localhost:5173`）

### 环境变量
- `DEV_MODE=1`: 强制开发模式
- `PROD_MODE=1`: 强制生产模式

## 项目结构
```
/
├── main.py                 # Qt 主程序
├── requirements.txt        # Python 依赖
├── frontend/              # Vue 前端
│   ├── dist/             # 构建产物
│   └── src/              # 源码
├── scripts/              # 构建脚本
├── .vscode/              # VS Code 配置
└── dist/                 # 最终打包产物
```
