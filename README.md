# EChemDB - 电化学实验条件数据库平台

## 快速启动 (本地)
`ash
python app.py --port=5002
# 访问 http://localhost:5002
`

## 部署到云端

### 方案一：Render (推荐，免费)
1. 将代码推送到 GitHub
2. 在 [render.com](https://render.com) 注册账号
3. 点击 "New +" → "Web Service"
4. 连接你的 GitHub 仓库
5. Render 会自动检测 ender.yaml 或 Procfile
6. 点击 "Deploy"
7. 等待 2-3 分钟，即可获得 https://your-app.onrender.com

### 方案二：PythonAnywhere
1. 在 [pythonanywhere.com](https://pythonanywhere.com) 注册 (免费账号)
2. 进入 Web 面板 → Add a new web app
3. 选择 "Manual Configuration" → "Python 3.12"
4. 使用 Git 或上传文件
5. 设置 WSGI 配置指向 pp.py
6. 重启 web app

### 方案三：Railway
1. 将代码推送到 GitHub
2. 在 [railway.app](https://railway.app) 注册
3. 点击 "New Project" → "Deploy from GitHub repo"
4. Railway 自动检测 Python/Flask 应用
5. 部署完成后获得 https://your-app.up.railway.app

## 配置

### 环境变量
- SECRET_KEY - Flask 密钥 (生产环境必填)
- PORT - 服务器端口 (云平台自动设置)

### 数据库
默认使用 SQLite (适合小型团队)。
如需 PostgreSQL，在 pp.py 中替换 SQLALCHEMY_DATABASE_URI：
`python
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///ecdb.sqlite3')
`

## API 接口
- GET /health - 健康检查
- POST /api/reactions/similar - 反应式相似度搜索
- POST /api/smiles/name - SMILES 名称查询
