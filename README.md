# IMYAI文本处理工具箱

![IMYAI文本处理工具箱](https://socialify.git.ci/zkeq/ai-markdown-text-toolkit/image?description=1&font=Rokkitt&language=1&name=1&owner=1&pattern=Brick%20Wall&theme=Dark)

> 这是一个基于FastAPI和前端JS开发的在线文本处理工具,提供了丰富的文本处理功能。

## 主要功能

- Markdown文本转普通文本
- AI智能优化文本
- 文本字数统计(包含汉字、字母、数字、标点符号等)
- 中英文标点符号转换
- 文本格式化(添加/删除空行、缩进等)
- 汉字转拼音(多种拼音风格)
- 文本查找替换
- 支持自动跟随系统深色/浅色主题切换

## 技术栈

- 后端: Python + FastAPI 
- 前端: HTML + CSS + JS
- 部署: Docker + Nginx

## 快速开始

### 0. 准备环境

- 安装Docker
- 拉取仓库或下载项目

```bash
git clone https://github.com/zkeq/ai-markdown-text-toolkit.git
```

### 1. 环境变量配置

修改 `docker-compose.yml` 中的 `PASSWORD` 为你的密码:

```yaml
PASSWORD: 后台密码
```

### 2. 使用Docker Compose部署

```bash
# 进入项目目录
cd ai-markdown-text-toolkit

# 启动服务
docker-compose up -d
```

服务将在以下端口启动:
- 前端: http://localhost:3030
- 后台: http://localhost:3030/config.html

## 项目结构

```
.
├── backend/                # 后端代码
│   ├── Dockerfile
│   ├── config.json        # 配置文件
│   ├── main.py           # FastAPI应用
│   └── requirements.txt   # Python依赖
├── frontend/              # 前端代码
│   ├── index.html        # 主页面
│   ├── config.html       # 配置页面
│   └── style.css         # 样式文件
├── nginx.conf            # Nginx配置
└── docker-compose.yml    # Docker编排文件
```

## API接口

主要API接口:

- `POST /api/improve`: AI文本优化
- `POST /api/pinyin`: 汉字转拼音
- `POST /api/info`: 获取配置信息
- `PUT /api/info`: 更新配置信息

## 开发说明

1. 后端开发
```bash
cd backend
pip install -r requirements.txt
python main.py
```

2. 前端开发
```bash
# 直接修改frontend目录下的文件即可
# 推荐使用VSCode打开项目,并安装Live Server插件
```

## 注意事项

1. 首次访问配置页面需要输入在docker-compose中设置的PASSWORD
2. 建议在生产环境中使用Nginx反向代理, 并增加SSL证书
3. 有偿代部署请联系微信: TUOJQ666

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。

## 许可证

MIT License