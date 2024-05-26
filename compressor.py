import ffmpeg
import os
import mimetypes
import shutil
import subprocess

def is_video_file(filename):
    type, _ = mimetypes.guess_type(filename)
    return type is not None and type.startswith('video')

def get_gpu_info():
    try:
        subprocess.check_output(['nvidia-smi'])
        return 'nvidia'
    except subprocess.CalledProcessError:
        pass
    
    try:
        subprocess.check_output(['amdgpu-pro-smi'])
        return 'amd'
    except subprocess.CalledProcessError:
        pass
    
    return None

def main():
    input_dir = 'input'
    output_dir = 'output'
    originals_dir = 'originals'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(originals_dir):
        os.makedirs(originals_dir)

    print("Choose operation:")
    print("1. Compress")
    print("2. Convert to MP4")
    print("3. Compress and convert to MP4")
    choice = input("Enter your choice (1, 2, or 3): ")

    valid_choices = {'1', '2', '3'}
    if choice not in valid_choices:
        print("Invalid choice. Exiting.")
        return

    gpu = get_gpu_info()
    if gpu == 'nvidia':
        encoder = 'h264_nvenc'
    elif gpu == 'amd':
        encoder = 'h264_amf'
    else:
        encoder = 'libx265'

    for filename in os.listdir(input_dir):
        if is_video_file(filename):
            input_path = os.path.join(input_dir, filename)
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_dir, base_name + '.mp4') if choice in {'2', '3'} else os.path.join(output_dir, filename)
            originals_path = os.path.join(originals_dir, filename)

            if choice == '1':
                ffmpeg.input(input_path).output(output_path, vcodec=encoder, crf=28).run()
            elif choice == '2':
                ffmpeg.input(input_path).output(output_path, format='mp4').run()
            elif choice == '3':
                ffmpeg.input(input_path).output(output_path, vcodec=encoder, crf=28, format='mp4').run()
            
            shutil.move(input_path, originals_path)

    print(f"Operation complete. Original files moved to /{originals_dir}.")

if __name__ == '__main__':
    main()