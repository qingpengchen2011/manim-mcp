#!/bin/bash
# Start MCP server in HTTP/SSE mode for Dify and web clients

PORT=${1:-8001}

echo "======================================"
echo "  Starting Manim MCP Server (HTTP)"
echo "======================================"
echo ""
echo "Port: $PORT"
echo "SSE Endpoint: http://localhost:$PORT/sse"
echo "Messages Endpoint: http://localhost:$PORT/messages"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python mcp_server.py --http $PORT
