# zero-to-tech-4-5 · Next.js 版（模块 4.5 配套代码）

4.5 的终点成品：把 4.4 的 React 项目整体搬到 Next.js。网站长相不变；变的是路由层（手搓 `useRoute` → 文件夹路由）和入口（`index.html` + `main.jsx` + `App.jsx` → `app/`）。

## 跑起来

```bash
npm install
npm run dev          # http://localhost:3000   （Next 默认端口是 3000）
```

## 把你的 4.4 项目（`zero-to-tech`）迁成这样：整包替换

1. 把 `~/zero-to-tech` 里**除隐藏的 `.git` 外的所有文件删掉**。
2. 把本 demo 下的所有文件拷进去（`node_modules`、`.next` 不用拷）。
3. 跑起来确认还是那个网站：
   ```bash
   npm install
   npm run dev          # http://localhost:3000
   ```
4. 确认无误后 `git add` / `commit` / `push`。

## 项目结构

```
app/                     ← 文件夹 = 路由
  layout.jsx             ← 全站外壳（页面包裹 + import 8 个 css）
  page.jsx               ← /         → 渲染 <HomeView />
  text-lab/page.jsx      ← /text-lab → 渲染 <TextLabView />
components/
  Nav.jsx                ← <Link> + usePathname（"use client"）
  HomeView.jsx           ← 4.4 的 HomePage 改名
  TextLabView.jsx        ← 4.4 的 TextLabPage 改名
  PageHeading.jsx        ← 同 4.4
  InputCard.jsx          ← 同 4.4（"use client"）
  ResultCard.jsx         ← 同 4.4（"use client"）
  AnimatedCardGrid.jsx   ← 同 4.4（"use client"）
css/                     ← 8 个 css，同 4.4
data/site.js             ← 同 4.4
next.config.mjs          ← 空 {}
```

相比 4.4，没了 `index.html`、`src/main.jsx`、`src/App.jsx`、`src/router/useRoute.js`——这一坨被 `app/` 取代了。

# 文字实验室

一个中文文本分析小工具：输入一段话，给出情感倾向评分和全文拼音，
并把每次分析的结果存下来，各人只看得到自己的那一份。

零到全栈课程的贯穿项目。

## 技术栈

- 前端：Next.js（静态导出）＋ React
- 后端：FastAPI ＋ uvicorn
- 分析：snownlp（情感）、pypinyin（注音）
- 存储：SQLite
- 线上：Nginx

## 本地跑起来

需要：Node.js 18+、Python 3.10+

**后端**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # 按下面「配置说明」填好
fastapi dev                   # → http://localhost:8000
```

**前端**（另开一个终端）

```bash
npm install
npm run dev                   # → http://localhost:3000
```

## 部署到服务器

前提：服务器上已装好 Python 3.10+、Node.js 18+ 和 Nginx，
且 Nginx 的站点根目录已指向本项目的 `out/`、监听 80 端口。

**1. 拉取代码**

```bash
cd ~/zero-to-tech
git pull
```

**2. 前端：装依赖并构建**

```bash
npm install
npm run build                     # 产物进 out/，由 Nginx 提供服务
```

**3. 后端：建环境、装依赖、写配置**

```bash
cd backend
python3 -m venv --prompt=zero-to-tech .venv   # 首次部署才需要
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env              # 按下面「配置说明」填好
```

**4. 后端：在后台跑起来**

```bash
nohup .venv/bin/fastapi run > backend.log 2>&1 &
```

`fastapi run` 是生产模式，监听 `0.0.0.0:8000`；`nohup ... &` 让它在
SSH 断开后继续运行，日志写进 `backend.log`。

查看日志、停止服务：

```bash
tail -f backend.log           # 看日志
ps aux | grep fastapi         # 找到进程号
kill 进程号                    # 停掉
```

**5. 配置 Nginx API 代理**

确保 Nginx 将 `/api/` 转发到本机 `127.0.0.1:8000`。生产环境的前端使用同源 `/api/...` 路径，8000 端口无需对公网开放。

**6. 验证**

浏览器访问部署域名，打开文字实验室做一次分析，再看历史记录。
换一个浏览器（或无痕窗口）再试一次，两边的历史记录应该是互相看不到的。
历史记录按浏览器 Cookie 中的会话 ID 区分；从 IP 切换到域名后，旧 IP 下的记录不会自动出现在域名下。

## 配置说明

后端配置文件不进 Git，请照着 `backend/.env.example` 自己建一份。

前端不需要配置 API 地址：开发时请求 `http://localhost:8000`，生产时请求同源 `/api`，由 Nginx 转发。

**后端**：`backend/.env`

| 键 | 说明 | 本地 | 线上 |
| --- | --- | --- | --- |
| `ALLOWED_ORIGINS` | 允许跨源访问的前端地址，多个用逗号隔开 | `http://localhost:3000` | `http://服务器IP`（不带端口） |
