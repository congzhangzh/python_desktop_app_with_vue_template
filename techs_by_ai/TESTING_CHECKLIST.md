# 脚手架验证清单

## 1. 基础功能测试

### 1.1 Python 应用独立运行
```bash
# 激活环境
mamba activate desktop_app_by_webview

# 直接运行（无前端）
python main.py
```
**验证点**：
- [ ] 应用启动无报错
- [ ] 显示错误提示："Neither development server nor built frontend found"
- [ ] 窗口正常显示

### 1.2 前端构建验证
```bash
cd frontend
npm install
npm run build
```
**验证点**：
- [ ] `frontend/dist/index.html` 文件存在
- [ ] `frontend/dist/` 包含完整的静态资源
- [ ] 构建无 TypeScript 错误
- [ ] 构建无 ESLint 错误

### 1.3 生产模式测试
```bash
# 前端已构建后
python main.py
```
**验证点**：
- [ ] 自动启动本地 HTTP 服务器
- [ ] WebView 正确加载前端页面
- [ ] 控制台显示："Started local HTTP server for built frontend"

## 2. 开发模式测试

### 2.1 手动开发模式
```bash
# 终端1：启动前端开发服务器
cd frontend && npm run dev

# 终端2：启动 Python 应用
python main.py
```
**验证点**：
- [ ] 前端开发服务器在 `localhost:5173` 启动
- [ ] Python 检测到开发服务器
- [ ] 控制台显示："Using development server"
- [ ] WebView 显示前端页面
- [ ] 前端热重载功能正常

### 2.2 VS Code 调试模式
```bash
# 在 VS Code 中按 F5，选择 "🚀 Dev Mode (Frontend + Python)"
```
**验证点**：
- [ ] `preLaunchTask` 正确启动前端开发服务器
- [ ] Python 调试器在前端服务就绪后启动
- [ ] 断点调试功能正常
- [ ] 可以同时调试前后端代码

## 3. 环境检测逻辑验证

### 3.1 开发服务器检测
```python
# 在 main.py 中测试
url = "http://localhost:5173"
available = self.is_dev_server_available(url)
print(f"Dev server available: {available}")
```
**验证点**：
- [ ] 前端服务运行时返回 True
- [ ] 前端服务未运行时返回 False
- [ ] 网络超时处理正确

### 3.2 路径检测逻辑
```python
# 测试 get_dist_path() 方法
dist_path = self.get_dist_path()
print(f"Found dist path: {dist_path}")
```
**验证点**：
- [ ] 正确找到 `frontend/dist` 路径
- [ ] 路径不存在时返回 None
- [ ] 跨平台路径处理正确

## 4. 生产构建测试

### 4.1 完整构建流程
```bash
# Linux/macOS
./scripts/build.sh

# Windows
.\scripts\build.cmd
```
**验证点**：
- [ ] 前端构建成功
- [ ] PyInstaller 打包成功
- [ ] 生成 `dist/DesktopApp/` 目录
- [ ] 可执行文件存在且可运行

### 4.2 打包后应用测试
```bash
# 运行打包后的应用
./dist/DesktopApp/DesktopApp  # Linux/macOS
.\dist\DesktopApp\DesktopApp.exe  # Windows
```
**验证点**：
- [ ] 应用正常启动
- [ ] 前端资源正确嵌入
- [ ] 本地 HTTP 服务器正常工作
- [ ] WebView 显示完整页面

## 5. Windows 兼容性测试

### 5.1 环境设置
```cmd
# Windows 命令提示符或 PowerShell
mamba create -n desktop_app_by_webview python=3.11
mamba activate desktop_app_by_webview
mamba install pyside6
pip install -r requirements.txt
```

### 5.2 路径处理测试
**验证点**：
- [ ] Windows 路径分隔符处理正确
- [ ] 长路径支持
- [ ] 中文路径兼容性

### 5.3 VS Code Windows 配置
**验证点**：
- [ ] `.vscode/tasks.json` 中的 Windows 命令正确
- [ ] PowerShell 和 cmd 兼容性
- [ ] 调试配置在 Windows 下正常工作

## 6. 错误处理测试

### 6.1 依赖缺失测试
```bash
# 测试 PySide6 未安装情况
pip uninstall PySide6
python main.py
```
**验证点**：
- [ ] 显示友好的错误信息
- [ ] 提示安装命令

### 6.2 端口占用测试
```bash
# 占用 8765 端口后启动应用
python -c "import socket; s=socket.socket(); s.bind(('localhost', 8765)); input()"
```
**验证点**：
- [ ] 自动寻找可用端口
- [ ] 端口冲突处理正确

### 6.3 前端构建失败测试
```bash
# 删除 frontend/dist 后运行
rm -rf frontend/dist
python main.py
```
**验证点**：
- [ ] 显示适当错误信息
- [ ] 应用不崩溃

## 7. 性能和用户体验测试

### 7.1 启动速度
**验证点**：
- [ ] 冷启动时间 < 5 秒
- [ ] 热启动时间 < 2 秒
- [ ] 前端页面加载流畅

### 7.2 内存使用
**验证点**：
- [ ] 空闲状态内存使用合理
- [ ] 无明显内存泄漏

## 测试记录

### 完成情况
- [ ] 基础功能测试
- [ ] 开发模式测试
- [ ] 环境检测验证
- [ ] 生产构建测试
- [ ] Windows 兼容性测试
- [ ] 错误处理测试
- [ ] 性能测试

### 发现的问题
（记录测试中发现的问题和解决方案）

### 优化建议
（记录可以改进的地方）