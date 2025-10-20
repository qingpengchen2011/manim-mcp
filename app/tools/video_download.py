from typing import Dict, Any
import base64

from app.utils import OUTPUT_FOLDER


def get_video(relative_path: str) -> Dict[str, Any]:
    """
    Retrieve a compiled video by its relative path.

    The relative_path format is: {knowledge_point}/{video_filename}.mp4
    For example: "勾股定理/Section1.mp4"

    Args:
        relative_path: The relative path to the video file from output folder

    Returns:
        Dict containing:
        - success: bool indicating if the video was found
        - file_path: Absolute path to the video file if found
        - relative_path: Relative path provided
        - knowledge_point: The knowledge point extracted from path
        - content: The base64 encoded content of the video file if found
        - error: Error message if video not found
    """
    # Validate relative_path format
    if not relative_path or "/" not in relative_path:
        return {
            "success": False,
            "file_path": None,
            "relative_path": relative_path,
            "knowledge_point": None,
            "content": None,
            "error": f"Invalid path format: {relative_path}. Expected format: {{knowledge_point}}/{{filename}}.mp4",
        }

    # Build absolute path
    video_path = OUTPUT_FOLDER / relative_path

    # Extract knowledge_point from path (first directory)
    path_parts = relative_path.split("/")
    knowledge_point = path_parts[0] if path_parts else None

    # Check if file exists
    if not video_path.exists():
        return {
            "success": False,
            "file_path": None,
            "relative_path": relative_path,
            "knowledge_point": knowledge_point,
            "content": None,
            "error": f"Video at path '{relative_path}' not found",
        }

    # Read video file and encode as base64
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
        video_content = base64.b64encode(video_bytes).decode("utf-8")

    return {
        "success": True,
        "file_path": str(video_path),
        "relative_path": relative_path,
        "knowledge_point": knowledge_point,
        "content": video_content,
        "error": None,
    }


# LangGraph tool definition
video_download_tool = {
    "name": "video_download",
    "description": "Download a compiled Manim video by its relative path. The path format is {knowledge_point}/{filename}.mp4.",
    "parameters": {
        "type": "object",
        "properties": {
            "relative_path": {
                "type": "string",
                "description": "The relative path to the video file (format: {knowledge_point}/{filename}.mp4, e.g., '0-勾股定理/0-勾股定理-Section1.mp4')",
            }
        },
        "required": ["relative_path"],
    },
    "execute": lambda params: get_video(params["relative_path"]),
}
