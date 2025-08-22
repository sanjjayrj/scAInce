#


import os
import re
import sys
import glob
import shutil
import tempfile
import subprocess


def run_generated_code(code: str, quality: str = "low"):
    """
    Renders Manim code headlessly in Docker and copies the result to Next.js /public/videos.
    Returns (result_dict, return_url).
    """

    # Quality flags for manim
    qflag = {
        "low": "-ql",
        "med": "-qm",
        "high": "-qh",
        "4k": "-qk",
    }.get(quality, "-ql")

    media_dir = os.getenv("MEDIA_DIR", os.path.join(os.getcwd(), "media"))
    public_videos_dir = os.getenv(
        "PUBLIC_VIDEOS_DIR",
        os.path.join(os.getcwd(), "..", "public", "videos"),
    )
    renderer = os.getenv("MANIM_RENDERER", "cairo")

    os.makedirs(public_videos_dir, exist_ok=True)
    print("[DEBUG] MEDIA_DIR:", media_dir)
    print("[DEBUG] PUBLIC_VIDEOS_DIR:", public_videos_dir)
    print("[DEBUG] MANIM_RENDERER:", renderer)

    # default URL if no video is produced
    return_url = "/videos/NotFound.mp4"


    # Work in an isolated temp dir so manim sees a clean module
    with tempfile.TemporaryDirectory(prefix="manim_") as tmpdir:
        temp_filename = os.path.join(tmpdir, "temp_generated.py")
        print("[DEBUG] Saving generated code to:", temp_filename)
        with open(temp_filename, "w") as f:
            f.write(code)

        try:
            is_manim = ("from manim import" in code) or ("import manim" in code)

            if is_manim:
                print("[DEBUG] Detected Manim script. Searching for Scene class...")
                match = re.search(r"class\s+(\w+)\(Scene\)\s*:", code)
                scene_class = match.group(1) if match else None

                if scene_class:
                    print(
                        f"[DEBUG] Found Scene class: {scene_class}. Executing Manim..."
                    )

                    # Headless-friendly: no -p; set renderer + media dir
                    cmd = [
                        "manim",
                        "--renderer",
                        renderer,
                        qflag,
                        "--media_dir",
                        media_dir,
                        temp_filename,
                        scene_class,
                        "-o",
                        f"{scene_class}.mp4",
                    ]
                    print("[DEBUG] Running command:", " ".join(cmd))
                    proc = subprocess.run(
                        cmd, capture_output=True, text=True, check=True
                    )
                    output_log = (proc.stdout or "") + (
                        "\n" + proc.stderr if proc.stderr else ""
                    )

                    # Find the output MP4 anywhere under media_dir
                    candidates = sorted(
                        glob.glob(
                            os.path.join(media_dir, "**", f"{scene_class}.mp4"),
                            recursive=True,
                        ),
                        key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0,
                    )

                    if candidates:
                        original_video_path = candidates[-1]
                        final_video_path = os.path.join(
                            public_videos_dir, f"{scene_class}.mp4"
                        )
                        print(
                            f"[DEBUG] Copying video {original_video_path} -> {final_video_path}"
                        )
                        shutil.copy2(original_video_path, final_video_path)

                        return_url = f"/videos/{scene_class}.mp4"
                        return {
                            "execution_type": "manim",
                            "output_log": output_log,
                            "video_path": return_url,
                        }, return_url
                    else:
                        print("[WARNING] Generated video not found under:", media_dir)
                        return {
                            "execution_type": "manim",
                            "output_log": output_log + "\n[WARNING] No mp4 found.",
                            "video_path": "Not found",
                        }, "Not Found"

                else:
                    print("[DEBUG] No Scene class found. Falling back to plain Python.")

            # ----- Fallback: run as a standard Python script -----
            print("[DEBUG] Running as standard Python script...")
            proc = subprocess.run(
                [sys.executable, temp_filename],
                capture_output=True,
                text=True,
                check=True,
            )
            output_log = (proc.stdout or "") + (
                "\n" + proc.stderr if proc.stderr else ""
            )
            print("[DEBUG] Python script execution completed.")
            return {"execution_type": "python", "output_log": output_log}, return_url

        except subprocess.CalledProcessError as e:
            print("[ERROR] Execution failed:", e)
            print("[ERROR] STDERR:", e.stderr)
            return {
                "execution_type": "error",
                "output_log": f"Execution failed: {e}\n{e.stderr}",
            }, "Not Found"
