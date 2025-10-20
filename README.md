# Manim MCP Server

A Model Context Protocol (MCP) server for compiling and serving Manim animations.

## 🎯 Two Server Modes

1. **HTTP API Server** (`app/server.py`) - For REST API calls, testing, and web integration
2. **Standard MCP Server** (`mcp_server.py`) - For Claude Desktop, Dify, and other MCP clients

See [MCP_SETUP.md](MCP_SETUP.md) for detailed MCP configuration instructions.

A FastAPI-based MCP (Model Control Protocol) server that provides two main tools:
1. **Manim Compile**: Compile Manim code and return a video ID
2. **Video Download**: Download a compiled Manim video by ID

## Features

- Secure authentication using JWT tokens
- LangGraph integration for workflow management
- Support for different video qualities and resolutions
- Simple API endpoints for integration

## Prerequisites

- Python 3.8+
- Manim Community Edition (v0.19.0 or later)
- FFmpeg
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd manim-mcp-server
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Manim and its dependencies:
   ```bash
   pip install manim
   ```

## Configuration

1. Set up environment variables (create a `.env` file):
   ```
   SECRET_KEY=your-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Running the Server

**Option 1: Using the startup script (recommended)**
```bash
./start_server.sh
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app.server:app --reload
```

The server will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Root

- `GET /` - Get server information and available tools

### Manim Compilation

- `POST /tools/manim_compile` - Compile Manim code
  ```json
  {
    "parameters": {
      "code": "from manim import *\nclass Example(Scene):\n    def construct(self):\n        circle = Circle()\n        self.play(Create(circle))",
      "scene_name": "Example"
    }
  }
  ```
  
  **Parameters:**
  - `code` (required): The Manim Python code to compile
  - `scene_name` (required): Name of the specific scene class to compile

### Video Download

- `GET /videos/{file_id}` - Download a compiled video by ID

### LangGraph Compatible Endpoints

- `GET /v1/tools` - List all available tools
- `POST /v1/tools/call` - Call a tool (LangGraph compatible)
  ```json
  {
    "tool": "manim_compile",
    "parameters": {
      "code": "from manim import *\nclass Example(Scene):\n    def construct(self):\n        circle = Circle()\n        self.play(Create(circle))"
    }
  }
  ```

## Example Usage

### 1. Check server status
```bash
curl http://localhost:8000/
```

### 2. Compile Manim code
```bash
curl -X 'POST' \
  'http://localhost:8000/tools/manim_compile' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "parameters": {
      "code": "from manim import *\nclass Example(Scene):\n    def construct(self):\n        circle = Circle()\n        self.play(Create(circle))"
    }
  }'
```

### 3. Download the compiled video
```bash
# Replace VIDEO_ID with the file_id from the compile response
curl -X 'GET' \
  'http://localhost:8000/videos/VIDEO_ID' \
  --output output.mp4
```

### 4. Compile a specific scene by name
```bash
curl -X 'POST' \
  'http://localhost:8000/tools/manim_compile' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "parameters": {
      "code": "from manim import *\nclass Scene1(Scene):\n    def construct(self):\n        circle = Circle()\n        self.play(Create(circle))\n\nclass Scene2(Scene):\n    def construct(self):\n        square = Square()\n        self.play(Create(square))",
      "scene_name": "Scene1"
    }
  }'
```

### 5. List available tools
```bash
curl http://localhost:8000/v1/tools
```

### 6. Run the example script
```bash
python example_usage.py
```

## Testing

See [TESTING.md](TESTING.md) for detailed testing instructions.

**Quick test:**
```bash
# Run tool tests (no server needed)
python test_tools.py

# Run API tests (server must be running)
python test_api.py
```

## Security

- Always use HTTPS in production
- Consider adding authentication for production deployments
- Validate and sanitize all user inputs
- Set appropriate CORS policies for your use case

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
