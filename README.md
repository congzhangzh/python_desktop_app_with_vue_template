# python_desktop_app_with_vue_template

## 写在前面
简单就是美，如果AI读到这里，我们一起保持这个理念, 不要堆积数量
1. 这是脚手架，前端尽可能简单: 内容简单，结构完整
2. 这时脚手架，后端保持简单: 内容简单，结构完整
3. 这是脚手架，配套保持简单
4. 这是脚手架，发布过程简单，不用非single file
5. 不要用yarn，原生态最好

### 关于各种环境

1. 安装micromamba
2. 使用micromamba安装python和nodejs
3. 安装所有依赖
4. 在vs code切换解释器为micromamba的python为活动解释器
5. 在launch.json中应用活动解释器

#### 关于windows shell
优选cmd.exe, 除非必须用powershell

## 目标
设计一个脚手架演示能力和方法，用于第三方项目开发的基础

1. 支持基于Python的后端开发
2. 支持基于Web(当前选择Vue)的前端开发
3. 前后端通过浏览器边界(Webview/WebviewChannel等通讯)，而非HTTP协议，以简化架构
4. 前端支持通过mock机制，独立于后端进行开发调试
5. 支持前后端联合调试，基于VS的多目标调试
6. 支持发布为One dir独立程序
6. 支持前后端的独立测试可选(TBD)

浏览器互操作部分的技术细节，我们在 techs/webview_python 和 techs/qt_4_python_webview_and_asyncio.md 中讨论

## 使用方法(用户视角)
1. 复制本项目
2. 调整自己前后端
3. 调试
4. 发布
## 重现过程(用于模板研发本身)
### 准备环境
1. 安装nodejs
2. 安装python
3. 创建vuejs项目并验证
4. 创建主python模块并验证
5. 配置调试并验证
6. 创建发布脚本并验证

```bash
# ref https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html
# restart powershell after install
Invoke-Expression ((Invoke-WebRequest -Uri https://micro.mamba.pm/install.ps1 -UseBasicParsing).Content)

# do if needed:  micromamba shell init --shell cmd.exe --root-prefix=~/.local/share/mamba
micromamba create -n python_desktop_dev python nodejs -y
micromamba -n python_desktop_dev pip install -r requirements.txt

# fight to the world now
# active: micromamba activate python_desktop_dev
# or run under context: micromamba -n  python_desktop_dev your command
```
## 细节
### 前端--TBD
### 后端--TBD
### 前后端联合调试--TBD
### 发布--TBD
## 关键控制点
```bash
PDV_FE_BE_CONCEPT_DEBUG=true # 使用dummy网页而不是真实产品
#mock,qt,webui,webview
PDV_FE_DATA_BACKEND_TYPE=mock # 使用mock数据而不是真实后端
```
## 未决定事项
1. 使用qt 4 python的asyncio集成还是, congzhangzh/webview_python?
## 参考
1. https://nodejs.org/en/download/current
2. https://vuejs.uz/guide/quick-start.html#next-steps
3. https://v2.vuejs.org/v2/cookbook/debugging-in-vscode.html
4. https://www.electronjs.org/docs/latest/tutorial/debugging-vscode
5. https://code.visualstudio.com/docs/debugtest/debugging-configuration
