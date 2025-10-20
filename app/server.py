import os
import json
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from app.tools.manim_compile import manim_compile_tool
from app.tools.video_download import video_download_tool

# Initialize FastAPI app
app = FastAPI(
    title="Manim MCP Server",
    description="MCP server for compiling and serving Manim animations",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Available tools
TOOLS = {
    "manim_compile": manim_compile_tool,
    "video_download": video_download_tool
}

class ToolRequest(BaseModel):
    tool: str
    parameters: Dict[str, Any]

class ToolResponse(BaseModel):
    result: Dict[str, Any]
    tool_call_id: str

@app.get("/")
async def root():
    """Root endpoint with basic info about the API."""
    return {
        "name": "Manim MCP Server",
        "version": "0.1.0",
        "available_tools": list(TOOLS.keys())
    }

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: Request):
    """Execute a specific tool by name."""
    if tool_name not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    try:
        # Parse request body
        body = await request.json()
        parameters = body.get("parameters", {})
        
        # Execute the tool
        tool = TOOLS[tool_name]
        result = tool["execute"](parameters)
        
        return {
            "tool": tool_name,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos/{file_id}")
async def download_video(file_id: str):
    """Download a video by its ID."""
    result = video_download_tool["execute"]({"file_id": file_id})
    
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return FileResponse(
        result["file_path"],
        media_type="video/mp4",
        filename=f"manim_animation_{file_id}.mp4"
    )

# LangGraph compatibility endpoints
@app.post("/v1/tools/call")
async def langgraph_tool_call(tool_request: ToolRequest):
    """LangGraph-compatible tool call endpoint."""
    if tool_request.tool not in TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_request.tool}' not found")
    
    tool = TOOLS[tool_request.tool]
    try:
        result = tool["execute"](tool_request.parameters)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/tools")
async def list_tools():
    """List all available tools in LangGraph format."""
    return [
        {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["parameters"]
        }
        for tool in TOOLS.values()
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
