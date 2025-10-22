# Docker Deployment Guide

This guide explains how to build and run the Manim MCP Server using Docker.

## Prerequisites

- Docker Engine 20.10 or later
- Docker Compose 2.0 or later (optional, for using docker-compose)

## Quick Start with Docker Compose (Recommended)

1. **Build and start the container:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop the container:**
   ```bash
   docker-compose down
   ```

## Manual Docker Build and Run

### Building the Image

Build the Docker image:
```bash
docker build -t manim-mcp-server .
```

This process will:
- Install Python 3.11
- Install FFmpeg for video rendering
- Install complete LaTeX distribution (texlive-full)
- Install all Python dependencies
- Set up the application

**Note:** The build process may take 10-20 minutes due to the large LaTeX installation.

### Running the Container

Run the container with volume mounts:
```bash
docker run -d \
  --name manim-mcp-server \
  -p 8000:8000 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/uploads:/app/uploads \
  -e SECRET_KEY=your-secret-key-here \
  manim-mcp-server
```

### Environment Variables

Set these in a `.env` file or pass them with `-e` flag:

- `SECRET_KEY`: Secret key for JWT authentication (required in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes (default: 30)

## Usage Examples

### Test the Server

Once running, test the server:
```bash
curl http://localhost:8000/
```

### Compile a Manim Animation

```bash
curl -X 'POST' \
  'http://localhost:8000/tools/manim_compile' \
  -H 'Content-Type: application/json' \
  -d '{
    "parameters": {
      "code": "from manim import *\nclass Example(Scene):\n    def construct(self):\n        text = MathTex(r\"\\frac{1}{2} + \\frac{1}{3}\")\n        self.play(Write(text))\n        self.wait()",
      "scene_name": "Example"
    }
  }'
```

### Access API Documentation

Open your browser and visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Container Management

### View Container Logs
```bash
docker logs -f manim-mcp-server
```

### Execute Commands Inside Container
```bash
docker exec -it manim-mcp-server bash
```

### Stop the Container
```bash
docker stop manim-mcp-server
```

### Remove the Container
```bash
docker rm manim-mcp-server
```

### Remove the Image
```bash
docker rmi manim-mcp-server
```

## Volume Mounts

The container uses two volume mounts:

- `./output:/app/output` - Stores compiled Manim videos
- `./uploads:/app/uploads` - Stores uploaded files

These volumes ensure that rendered videos persist even if the container is removed.

## Troubleshooting

### LaTeX Compilation Errors

If you encounter LaTeX errors, the container includes the full texlive distribution. You can verify LaTeX installation:
```bash
docker exec manim-mcp-server pdflatex --version
```

### FFmpeg Issues

Verify FFmpeg installation:
```bash
docker exec manim-mcp-server ffmpeg -version
```

### Memory Issues

For complex animations, you may need to increase Docker's memory limit:
```bash
docker run -d \
  --name manim-mcp-server \
  --memory=4g \
  --memory-swap=4g \
  -p 8000:8000 \
  manim-mcp-server
```

### Build Cache Issues

If you encounter build issues, try building without cache:
```bash
docker build --no-cache -t manim-mcp-server .
```

## Production Deployment

For production deployment:

1. **Use environment variables from a secure source:**
   ```bash
   docker run -d \
     --env-file .env.production \
     -p 8000:8000 \
     manim-mcp-server
   ```

2. **Use a reverse proxy (e.g., Nginx) for HTTPS**

3. **Set resource limits:**
   ```bash
   docker run -d \
     --cpus="2.0" \
     --memory="4g" \
     -p 8000:8000 \
     manim-mcp-server
   ```

4. **Enable automatic restarts:**
   ```bash
   docker run -d \
     --restart=unless-stopped \
     -p 8000:8000 \
     manim-mcp-server
   ```

## Image Size

The Docker image is approximately 3-4 GB due to the complete LaTeX distribution. If size is a concern, you can modify the Dockerfile to install a minimal LaTeX distribution instead of `texlive-full`.

## Health Checks

The container includes a health check that pings the server every 30 seconds. Check the health status:
```bash
docker inspect --format='{{.State.Health.Status}}' manim-mcp-server
```
