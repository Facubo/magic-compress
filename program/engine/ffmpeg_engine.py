import os
import subprocess

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FFMPEG_BINARIES = os.path.join(DIRECTORY, "ffmpeg", "bin", "ffmpeg.exe")
FFPROBE_BINARIES = os.path.join(DIRECTORY, "ffmpeg", "bin", "ffprobe.exe")

def ffmpeg_verify():
    return os.path.isfile(FFMPEG_BINARIES)

def run_engine(args):

    command = [FFMPEG_BINARIES] + args
    process = subprocess.Popen(
        command,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines=True
    )

    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

def video_information(path):

    command = [
        FFPROBE_BINARIES,
        "-v", "quiet",
        "-print_format", "json"
        "-show_format",
        "-show_streams",
        path,
    ]

    process = subprocess.Popen(
        command,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines=True
    )
    
    out, err = process.communicate()
    return out