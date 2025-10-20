import io
import sys
import shutil
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

import manim
from manim import config, tempconfig
from manim.utils.module_ops import scene_classes_from_file

from app.utils import generate_id, get_output_path, save_uploaded_file, cleanup_file


def compile_manim(code: str, scene_name: str, knowledge_point: str) -> Dict[str, Any]:
    """
    Compile Manim code and return the result.

    Args:
        code: The Manim Python code to compile
        scene_name: Name of the specific scene class to compile (required)
        knowledge_point: Knowledge point name indicating the topic (required)

    Returns:
        Dict containing:
        - success: bool indicating if compilation was successful
        - output_path: Absolute path to the output video if successful
        - relative_path: Relative path from output folder (e.g., "勾股定理/Section1.mp4")
        - error: Error message if compilation failed
        - scene_name: Name of the scene that was compiled
        - knowledge_point: Knowledge point name
    """
    # Create knowledge point directory structure
    from app.utils import OUTPUT_FOLDER

    knowledge_point_dir = OUTPUT_FOLDER / knowledge_point
    knowledge_point_dir.mkdir(exist_ok=True)

    # Generate video filename as {knowledge_point}-{scene_name}.mp4
    video_filename = f"{scene_name}.mp4"

    # Save the code file as {scene_name}.py in the knowledge point directory
    code_file_path = knowledge_point_dir / f"{scene_name}.py"
    with open(code_file_path, "w", encoding="utf-8") as f:
        f.write(code)

    # Output video path: {knowledge_point}/{knowledge_point}-{scene_name}.mp4
    output_path = knowledge_point_dir / video_filename

    # Relative path from output folder
    relative_path = f"{knowledge_point}/{video_filename}"

    # Use the saved code file for compilation
    temp_file = code_file_path

    try:
        # Configure Manim to render only the specified scene at 480p (low quality)
        # Use media directory within the knowledge point folder
        media_dir = knowledge_point_dir / "media"
        media_dir.mkdir(exist_ok=True)

        with tempconfig(
            {
                "output_file": f"{scene_name}",
                "media_dir": str(media_dir),
                "save_last_frame": False,
                "format": "mp4",
                "file_writer_command": None,
                "quiet": True,
                "preview": False,
                "write_to_movie": True,
                "disable_caching": True,
                "scene_names": [scene_name],  # Specify which scene to render
                "quality": "low_quality",  # 480p resolution (854x480)
                "pixel_height": 480,
                "pixel_width": 854,
            }
        ):
            # Import the scene from the temporary file
            scene_classes = scene_classes_from_file(temp_file)

            if not scene_classes:
                raise ValueError("No valid Manim scenes found in the provided code")

            # Verify the scene exists
            scene_to_render = None
            all_scene_names = []
            for scene_class in scene_classes:
                all_scene_names.append(scene_class.__name__)
                if scene_class.__name__ == scene_name:
                    scene_to_render = scene_class
                    break

            if not scene_to_render:
                raise ValueError(
                    f"Scene '{scene_name}' not found. Available scenes: {', '.join(all_scene_names)}"
                )

            # Render the selected scene
            scene = scene_to_render()
            scene.render()

            # Get the output file path
            scene_file = Path(scene.renderer.file_writer.movie_file_path)
            if scene_file.exists():
                # Move to our output location using shutil for cross-filesystem compatibility
                shutil.move(str(scene_file), str(output_path))
            else:
                raise FileNotFoundError(f"Rendered video not found at {scene_file}")

        return {
            "success": True,
            "output_path": str(output_path),
            "relative_path": relative_path,
            "scene_name": scene_name,
            "knowledge_point": knowledge_point,
            "code_file": str(code_file_path),
            "error": None,
        }

    except Exception as e:
        # Capture the full traceback
        error_msg = ""
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_type is not None:
            error_msg = "\n".join(
                traceback.format_exception(exc_type, exc_value, exc_traceback)
            )

        return {
            "success": False,
            "output_path": None,
            "relative_path": relative_path,
            "scene_name": scene_name,
            "knowledge_point": knowledge_point,
            "error": error_msg,
        }

    finally:
        # Keep the code file and media directory for future reference
        # No cleanup needed as files are organized by knowledge point
        pass


# LangGraph tool definition
manim_compile_tool = {
    "name": "manim_compile",
    "description": "Compile Manim code and return the relative path to the video file. Requires specifying which scene to compile and knowledge point for organization.",
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Manim Python code to compile",
            },
            "scene_name": {
                "type": "string",
                "description": "Name of the specific scene class to compile (required)",
            },
            "knowledge_point": {
                "type": "string",
                "description": "Knowledge point name for organizing files (required)",
            },
        },
        "required": ["code", "scene_name", "knowledge_point"],
    },
    "execute": lambda params: compile_manim(
        params["code"], params["scene_name"], params["knowledge_point"]
    ),
}
