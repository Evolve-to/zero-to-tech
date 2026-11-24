# 文字实验室

零到全栈课程的贯穿项目。输入一段中文，查看情绪分和全文拼音。分析记录存入数据库，每个访客可以查看自己的历史。

## 技术栈

- 前端用 Next.js（静态导出）和 React
- 后端用 FastAPI 和 Uvicorn
- 文本分析用 snownlp 和 pypinyin
- 数据存储用 PostgreSQL 16，线上由 Nginx 提供静态文件并转发 API 请求

## 项目结构

| 路径 | 内容 |
| --- | --- |
| `app/`、`components/` | 页面和 React 组件 |
| `css/`、`public/` | 样式和静态资源 |
| `backend/main.py` | 分析和历史记录 API |
| `backend/storage.py` | 数据库连接、建表和读写 |
| `backend/requirements.txt` | 后端依赖 |

## 准备环境和配置

需要 Node.js 18.18+、Python 3.10+ 和 PostgreSQL 16。先启动 PostgreSQL，用管理员身份创建项目用户和数据库。

```sql
CREATE USER textlab_backend;
CREATE DATABASE textlab OWNER textlab_backend;
```

在同一个 `psql` 会话里用 `\password textlab_backend` 设置密码。首次启动后端时会自动创建历史记录表和索引。

参考项目里的 `.env.example` 和 `backend/.env.example` 准备配置文件。

| 配置 | 本地 | 线上 |
| --- | --- | --- |
| 前端 `NEXT_PUBLIC_API_BASE_URL` | 在 `.env.local` 填 `http://localhost:8000` | 在 `.env.production` 留空，前端用相对路径访问 `/api/` |
| 后端 `ALLOWED_ORIGINS` | `http://localhost:3000` | 站点地址，例如 `https://example.com` |
| 后端 `DATABASE_URL` | 本地数据库的连接串 | 服务器数据库的连接串 |

后端两项都写在 `backend/.env`。连接串形如 `postgresql://textlab_backend:PASSWORD@localhost:5432/textlab`，把 `PASSWORD` 换成对应环境的密码。真实密码只放在各自环境的 `.env` 里。

## 本地运行

在项目根目录打开两个终端。第一个终端用来启动后端，先按系统创建并激活虚拟环境。已有 `.venv` 时，直接激活即可。

**macOS / Ubuntu**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

**Windows（PowerShell）**

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

激活后，安装依赖并启动后端。三个系统的写法一样。

```bash
pip install -r requirements.txt
fastapi dev                     # http://localhost:8000
```

在另一个终端从项目根目录启动前端。

```bash
npm install
npm run dev                     # http://localhost:3000
```

## 部署到服务器

服务器另需安装 Nginx。准备好 PostgreSQL 和线上配置后，按下面的顺序部署。

1. **前端**。在项目根目录运行 `npm install` 和 `npm run build`，构建产物在 `out/`。
2. **后端**。在 `backend` 创建并激活虚拟环境，执行 `pip install -r requirements.txt`。将下面的配置保存为 `/etc/systemd/system/zero-backend.service`，按实际部署账号和目录修改。

   ```ini
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/zero-to-tech/backend
   ExecStart=/home/ubuntu/zero-to-tech/backend/.venv/bin/fastapi run --host 127.0.0.1
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   运行 `sudo systemctl daemon-reload` 和 `sudo systemctl enable --now zero-backend`。

3. **Nginx**。网站根目录指向项目的 `out/`，页面路由用 `try_files $uri $uri.html $uri/ =404;`，在 `/api/` 的配置里用 `proxy_pass http://127.0.0.1:8000;`。预留给后端和数据库的 8000 和 5432 都留在本机。
