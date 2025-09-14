# VS Code 团队开发环境配置

## 环境激活策略

### 1. 创建统一的conda环境
```bash
# 使用项目根目录的environment.yml创建环境
mamba env create -f environment.yml
# 或使用conda
conda env create -f environment.yml
```

### 2. VS Code配置说明

#### settings.json配置要点：
- `python.defaultInterpreterPath`: 使用环境名而非绝对路径
- `python.condaPath`: 设置为"mamba"或"conda"
- `python.venvPath`: 根据你的mamba/conda安装位置调整

#### launch.json调试配置：
- `python`: 使用`${command:python.interpreterPath}`让VS Code自动选择正确的解释器
- `env`: 设置必要的环境变量

#### tasks.json任务配置：
- 添加了`environment: activate conda`任务用于环境激活
- 所有Python相关任务都会使用激活的环境

### 3. 团队协作最佳实践

#### 配置文件管理：
- `.vscode/settings.example.json`: 团队共享的配置模板
- `.vscode/settings.json`: 个人配置（不要提交到git）
- `.vscode/launch.json`和`.vscode/tasks.json`: 团队共享

#### 推荐的git忽略配置：
```gitignore
# VS Code个人配置
.vscode/settings.json
```

### 4. 环境激活验证

#### 检查当前环境：
1. 打开VS Code终端，应该看到环境名在提示符中
2. 运行`python --version`确认Python版本
3. 运行`which python`确认Python路径

#### 调试时环境检查：
- 在调试控制台中运行`import sys; print(sys.executable)`
- 确认路径指向正确的conda环境

### 5. 常见问题解决

#### VS Code找不到Python解释器：
1. Ctrl+Shift+P → "Python: Select Interpreter"
2. 选择desktop_app_by_webview环境
3. 重启VS Code

#### 调试时环境不对：
1. 检查launch.json中的python配置
2. 确保environment.yml中的环境名正确
3. 重新创建conda环境

#### 任务执行失败：
1. 手动运行`environment: activate conda`任务
2. 检查terminal.integrated.env配置
3. 确认mamba/conda在PATH中

### 6. 平台兼容性

配置已针对Linux、macOS和Windows进行了优化：
- Linux/macOS: 使用~/mambaforge路径
- Windows: 使用%USERPROFILE%\\mambaforge路径
- 团队成员需要根据实际安装路径调整settings.json
