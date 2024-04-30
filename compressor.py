import ffmpeg
import os
import mimetypes
import shutil

input_dir = 'input'
output_dir = 'output'
originals_dir = 'originals'

def is_video_file(filename):
    type, _ = mimetypes.guess_type(filename)
    return type is not None and type.startswith('video')

def main():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(originals_dir):
        os.makedirs(originals_dir)

    for filename in os.listdir(input_dir):
        if is_video_file(filename):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            originals_path = os.path.join(originals_dir, filename)
            ffmpeg.input(input_path).output(output_path, vcodec='libx265', crf=28).run()
            shutil.move(input_path, originals_path)

    print(f"Compression complete. Original files moved to /{originals_dir}.")

if __name__ == '__main__':
    main()