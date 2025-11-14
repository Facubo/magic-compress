import os
import sys
from engine.ffmpeg_engine import run_engine, video_information, ffmpeg_verify

def input_file_dir():
    """
    This module is responsible for requesting a file path from the user, stored in "path".
    If the path is not correct (i/e does not contain a file) or does not exist,
    The system will return an error message.
    """
    while True:
        path = input("Paste the directory: ").strip('" ') # Strips everything and leaves a clean string for the program to work with
        if path.lower() == "exit":
            sys.exit("Exit code: 0")
        if os.path.isfile(path):
            return path
        print(f"File not found.") # Error Message

def input_file_size(path): # Gets the filesize for the file loaded in "def input_file_dir()"
    return os.path.getsize(path)

def file_size_format(bytes_size):
    """
    This module is responsible for converting the filesize obtained in bytes from "def input_file_size"
    into a readable string using B, KB, MB, or GB, and print it on screen.
    It also selects the appropriate unit (i/e won't show 1190KB instead of 1.19MB)
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0

def file_size_parser(size_str, initial_size):
    """
    This module is responsible for parsing a user-entered file size string
    (i/e 8MB, 500kb', 2 gb), convert it into bytes, validate the
    numeric and unit components, and (for now) return a valueerrror.

    TBD: This will be the desired filesize which the user wants their video to be.
    """

    size_str = size_str.strip().upper().replace(" ", "") #Strips everything and leaves a clean string for the program to work with
    units = [("GB", 1024**3), ("MB", 1024**2), ("KB", 1024), ("B", 1)]

    match True:

        # Case 1: Number without unit
        case _ if size_str.replace('.', '', 1).isdigit():
            raise ValueError("Please specify a unit (B, KB, MB, GB).")

        # Case 2: Anything but a number
        case _ if (unit := next((u[0] for u in units if isinstance(size_str, str) and size_str.endswith(u[0])), None)):
            number_part = size_str[:-len(unit)]
            match number_part.replace('.', '', 1).isdigit():
                case True:
                    parsed_file_size = float(number_part) * dict(units)[unit]
                    match parsed_file_size >= initial_size:
                        case True:
                            raise ValueError(
                                f"Compression size should be less than file size. File size: {file_size_format(initial_size)}")
                        case False:
                            return parsed_file_size
                case False:
                    raise ValueError(f"Invalid input. Please enter a number and specify a valid unit (B, KB, MB, GB)")
        # Case 3: Invalid unit
        case _:
            raise ValueError(f"Unit invalid or not found. Please enter a number and specify a valid unit (B, KB, MB, GB)")

def target_size_prompt(size):
    while True:
        target_file_size = input("Enter the desired filesize: ").strip().lower()

        if target_file_size == 'exit':
            return "EXIT"
        if target_file_size == 'return':
            return "RETURN"
        
        try:
            target_file_size_bytes = file_size_parser(target_file_size, size)
            print(f"Desired filesize: {file_size_format(target_file_size_bytes)}")
            return target_file_size_bytes
        except ValueError as e:
            print(f"{e}")
            continue

def compress(input_path, initial_size):
    """
    Calculates desired bitrate and converts the file to the desired filesize.
    """

    # Verify if there is a FFmpeg version embedded
    if not ffmpeg_verify():
        print("Internal FFmpeg binaries not found inside engine/ffmpeg/bin/")
        return False

    # Read the file information
    file_information = video_information(input_path)
    if not file_information:
        print("Exit code 2: Unable to read video information.")
        return False
    try:
        duration = float(file_information["format"]["duration"])
    except:
        print("Exit code 3: Could not extract video duration.")
        return False

    """
    How to calculate bitrate: (filesize in bits / duration) / 1000
    """
    target_bits = initial_size * 8
    target_bitrate_kbps = (target_bits / duration) / 1000

    if target_bitrate_kbps < 50:
        print("Warning: Target bitrate is extremely low. Output may be unreadable.")
    elif target_bitrate_kbps > 50000:
        print("Warning: Target bitrate is very high. File may grow instead of shrinking.")

    # Name constructor
    base, ext = os.path.splitext(input_path)
    output_path = base + "_compressed" + ext

    # Compression algorithm execution
    args = [
        "-y",                # sobrescribir
        "-i", input_path,
        "-b:v", f"{int(target_bitrate_kbps)}k",
        "-c:v", "libx264",
        "-preset", "medium",
        "-c:a", "aac",
        "-b:a", "128k",
        output_path
    ]

    code, stdout, stderr = run_engine(args)

    if code != 0:
        print("Exit code 4: FFmpeg error during compression:")
        print(stderr)
        return False

    print(f"Exit code 5g: Compression complete: {output_path}")
    return True

def main():
    """
    This module is the main loop and is also responsible for controlling the main program workflow:
    - Query the path
    - Display the original filesize
    - Ask for target compressed filesize
    - Handle 'EXIT' and 'RETURN' signals
    - Trigger the compression engine (TBD)
    """
    while True:
        path = input_file_dir()
        if path == "EXIT":
            sys.exit(0)

        size = input_file_size(path)
        print (f"Original filesize: {file_size_format(size)}")

        target = target_size_prompt(size)
        if target == "EXIT":
            sys.exit(0)
        if target == "RETURN":
            continue

        print("Starting compression engine...")
        compress(path, target)
        break

if __name__ == "__main__":
    main()