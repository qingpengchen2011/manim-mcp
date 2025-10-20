# 快速参考指南

## 🚀 启动服务器

### 1. MCP 服务器 (HTTP 模式) - 用于 Dify
```bash
python mcp_server.py --http 8001
# 或使用脚本
./start_mcp_http.sh
```

**端点：**
- SSE: `http://localhost:8001/sse`
- Messages: `http://localhost:8001/messages`

### 2. MCP 服务器 (stdio 模式) - 用于 Claude Desktop
```bash
# 由 Claude Desktop 自动启动，无需手动运行
# 配置文件: ~/Library/Application Support/Claude/claude_desktop_config.json
```

### 3. HTTP API 服务器 - 用于测试和自定义集成
```bash
uvicorn app.server:app --reload
# 或使用脚本
./start_server.sh
```

**端点：**
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

## 📦 安装依赖

```bash
# 安装所有依赖
pip install -r requirements.txt

# 或单独安装 MCP 相关
pip install mcp starlette sse-starlette
```

## 🔧 Dify 配置

### 选项 1: MCP over HTTP (推荐)

1. 启动服务器：
   ```bash
   python mcp_server.py --http 8001
   ```

2. 在 Dify 中配置：
   - Base URL: `http://localhost:8001`
   - SSE: `http://localhost:8001/sse`
   - Messages: `http://localhost:8001/messages`

### 选项 2: 传统 REST API

1. 启动服务器：
   ```bash
   uvicorn app.server:app --reload
   ```

2. 在 Dify 中配置：
   - Base URL: `http://localhost:8000`
   - 端点: `/tools/manim_compile`, `/videos/{file_id}`

## 🧪 测试

```bash
# 测试工具
python test_tools.py

# 测试 API (需要先启动 HTTP API 服务器)
python test_api.py

# 测试 MCP HTTP 端点
curl -X POST http://localhost:8001/messages \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## 📋 可用工具

### manim_compile
编译 Manim 动画代码

**参数：**
- `code` (string, 必需): Manim Python 代码
- `scene_name` (string, 必需): Scene 类名

**示例：**
```json
{
  "code": "from manim import *\nclass Test(Scene):\n    def construct(self):\n        circle = Circle()\n        self.play(Create(circle))",
  "scene_name": "Test"
}
```

### video_download
获取已编译视频的文件路径

**参数：**
- `file_id` (string, 必需): 视频 ID

## 🎯 端口使用

| 服务 | 端口 | 用途 |
|------|------|------|
| HTTP API | 8000 | REST API, 测试 |
| MCP HTTP | 8001 | Dify, Web 客户端 |
| MCP stdio | N/A | Claude Desktop |

## 📝 常用命令

```bash
# 启动 MCP HTTP 服务器
python mcp_server.py --http

# 启动 MCP HTTP 服务器（指定端口）
python mcp_server.py --http 8001

# 启动 HTTP API 服务器
uvicorn app.server:app --reload

# 运行测试
python test_tools.py
python test_api.py

# 查看 API 文档
open http://localhost:8000/docs
```

## 🔍 故障排查

### MCP 服务器无法启动
```bash
# 检查依赖
pip install mcp starlette sse-starlette

# 查看错误日志
python mcp_server.py --http
```

### Dify 无法连接
1. 确认服务器正在运行
2. 检查端口是否正确 (8001)
3. 测试端点是否可访问：
   ```bash
   curl http://localhost:8001/sse
   ```

### Claude Desktop 找不到工具
1. 检查配置文件路径
2. 确认 Python 路径正确
3. 重启 Claude Desktop

## 📖 更多信息

- 详细配置: [MCP_SETUP.md](MCP_SETUP.md)
- 测试指南: [TESTING.md](TESTING.md)
- API 文档: http://localhost:8000/docs
