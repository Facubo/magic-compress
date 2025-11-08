import os
import sys

def input_file_dir():
    while True:
        path = input("Paste the directory: ").strip('" ')
        if path.lower() == "exit":
            sys.exit("Exit code: 0")
        if os.path.isfile(path):
            return path
        print(f"File not found.")

def input_file_size(path):
    return os.path.getsize(path)

def file_size_format(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0

def file_size_parser(size_str, initial_size):
    size_str = size_str.strip().upper().replace(" ", "")
    units = [("GB", 1024**3), ("MB", 1024**2), ("KB", 1024), ("B", 1)]

    match True:

        # Case 1: Number without unit
        case _ if size_str.replace('.', '', 1).isdigit():
            raise ValueError("Please specify a unit (B, KB, MB, GB).")

        # Case 2: Anything but a number
        case _ if (unit := next((u for u in units if size_str.endswith(u)), None)):
            number_part = size_str[:-len(unit)]
            try:
                parsed_file_size = float(number_part) * units[unit]
            except ValueError:
                raise ValueError(f"Invalid number format. Please enter a number and specify a valid unit (B, KB, MB, GB)")
            
            match parsed_file_size >= initial_size:
                case True:
                    raise ValueError(
                    f"Compression size should be less than file size. File size: {file_size_format(initial_size)}")
                case False:
                    return parsed_file_size
        # Case 3: Invalid unit
        case _:
            return

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

def main():
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

        print(f"compression algorithm NOT ready.")
        break

if __name__ == "__main__":
    main()