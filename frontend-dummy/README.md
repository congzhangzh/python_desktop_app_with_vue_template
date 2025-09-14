# Frontend Dummy - Backend Test Interface

简单的HTML页面，用于测试后端抽象层，不依赖Vue构建系统。

## 用途

- 🔧 测试不同后端类型的集成 (webview_python, webui, qt4)
- 🐛 调试前端后端通信问题
- 📋 验证backend-abstraction.js的功能
- 🚀 独立于正式前端进行快速测试

## 文件

```
frontend-dummy/
├── index.html              # 测试页面
├── backend-abstraction.js  # 后端抽象层
├── .env                    # 环境配置
└── README.md              # 说明文档
```

## 使用方法

### 1. 直接用Python后端服务

```bash
# 启动不同的后端
python main.py webview_python  # 会加载 frontend-dummy/index.html
python main.py webui          # 会加载 frontend-dummy/index.html  
python main.py qt4            # 会加载 frontend-dummy/index.html
```

### 2. 手动打开HTML (Mock模式)

```bash
# 修改 backend-abstraction.js 中的环境变量
const FE_BE_CONCEPT_MOCK = true

# 然后在浏览器中打开
open frontend-dummy/index.html
```

## 环境变量

- `FE_BE_CONCEPT_DEBUG=true` - 显示详细的后端检测日志
- `FE_BE_CONCEPT_MOCK=true` - 强制使用Mock后端

## 测试功能

- 📋 **Get System Info** - 测试系统信息获取
- 💬 **Send Message** - 测试消息发送
- 📊 **Get Backend Data** - 测试数据获取
- 🗑️ **Clear** - 清空测试结果

## 后端检测

页面会自动检测可用的后端类型：

1. `window.pywebview.api` → WebViewPython
2. `window.webui` → WebUI  
3. `window.qt` → Qt4
4. 否则 → Mock (开发模式)

## 与正式前端的区别

| 项目 | 正式前端 (`frontend/`) | 测试前端 (`frontend-dummy/`) |
|------|----------------------|----------------------------|
| 技术栈 | Vue + Vite + TypeScript | 原生HTML + ES6 modules |
| 用途 | 生产级前端应用 | 后端集成测试 |
| 复杂度 | 完整的前端框架 | 简单的测试页面 |
| 构建 | npm run build | 无需构建 |
