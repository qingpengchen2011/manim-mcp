#!/usr/bin/env python3
"""
FastMCP Server for Manim Animation Compilation
Supports both stdio and HTTP transports for compatibility with:
- Claude Desktop (stdio)
- Dify and other web clients (HTTP)
"""

import logging
import sys
from typing import Any

# FastMCP import
from fastmcp import FastMCP
from app.tools.manim_compile import compile_manim
from app.tools.video_download import get_video

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("manim-mcp-server")

# Create FastMCP server instance
mcp = FastMCP("Manim Animation Server")


@mcp.tool()
def manim_compile(code: str, scene_name: str, knowledge_point: str) -> str:
    """
    Compile Manim animation code and return the relative path to the video file.

    Args:
        code: The Manim Python code to compile. Must contain at least one Scene class.
        scene_name: Name of the Scene class to compile (required, case-sensitive)
        knowledge_point: Knowledge point name indicating the topic (required)

    Returns:
        Compilation result with relative video path or error message
    """
    logger.info(
        "Tool called: manim_compile with scene_name: %s, knowledge_point: %s",
        scene_name,
        knowledge_point,
    )

    try:
        if not code or not scene_name or not knowledge_point:
            return "Error: 'code', 'scene_name', and 'knowledge_point' parameters are required"

        # Call the compilation function
        result = compile_manim(code, scene_name, knowledge_point)

        if result["success"]:
            response_text = (
                f"✅ Compilation successful!\n\n"
                f"Relative Path: {result['relative_path']}\n"
                f"Knowledge Point: {result['knowledge_point']}\n"
                f"Scene: {result['scene_name']}\n"
                f"Output: {result['output_path']}\n\n"
                f"Use the 'video_download' tool with path='{result['relative_path']}' to download the video."
            )
        else:
            response_text = f"❌ Compilation failed\n\n" f"Error:\n{result['error']}"

        return response_text

    except Exception as e:
        logger.error(f"Error executing manim_compile: {e}", exc_info=True)
        return f"Error executing tool: {str(e)}"


@mcp.tool()
def video_download(path: str) -> str:
    """
    Download a previously compiled Manim video and return its full base64 encoded content.

    Args:
        path: The relative path to the video file returned from manim_compile
              (format: {knowledge_point}/{filename}.mp4, e.g., "勾股定理/Section1.mp4")

    Returns:
        Video file information and base64 content or error message
    """
    logger.info("Tool called: video_download with path: %s", path)

    try:
        if not path:
            return "Error: 'path' parameter is required"

        # Get the video
        result = get_video(path)

        if result["success"]:
            # Return the full base64 content directly
            relative_path = result.get("relative_path", "unknown")
            file_path = result.get("file_path", "unknown")
            knowledge_point = result.get("knowledge_point", "unknown")
            content = result.get("content", "")

            response_text = (
                f"✅ Video downloaded successfully!\n\n"
                f"Relative Path: {relative_path}\n"
                f"Knowledge Point: {knowledge_point}\n"
                f"File path: {file_path}\n"
                f"Content size: {len(content)} characters (base64)\n\n"
                f"Base64 Video Content:\n"
                f"{content}"
            )
        else:
            relative_path = result.get("relative_path", "unknown")
            error = result.get("error", "Unknown error")

            response_text = (
                f"❌ Video not found\n\n"
                f"Relative Path: {relative_path}\n"
                f"Error: {error}"
            )

        return response_text

    except Exception as e:
        logger.error(f"Error executing video_download: {e}", exc_info=True)
        return f"Error executing tool: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8001)
