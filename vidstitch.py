"""
1. command-line script that to concat any videos in a folder
    a. well documented
    b. short, concise code
2. arguments
    a. POSITIONAL - input directory of video files
    b. OPTIONAL - output video format
    c. OPTIONAL - output directory
    d. OPTIONAL - help
3. ffmpeg concat the video files into the output format and directory
4. delete the .txt list of video files
"""

import argparse
import os
import subprocess

def concat_videos(input_dir, output_dir, output_format):
    """
    concat videos in input_dir into output_dir in output_format
    """
    # create a list of video files in input_dir
    video_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.mp4')]
    # create a text file with the list of video files
    with open('video_list.txt', 'w') as f:
        for video in video_files:
            f.write("file '{}'\n".format(video))
    # concat the video files
    subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'video_list.txt', '-c', 'copy', '{}/concat.{}'.format(output_dir, output_format)])
    # delete the text file
    os.remove('video_list.txt')

def main():
    """
    main function
    """
    # create an argument parser
    parser = argparse.ArgumentParser(description='Concatenate videos in a folder')
    # add arguments
    parser.add_argument('input_dir', help='input directory of video files')
    parser.add_argument('-o', '--output_dir', default='.', help='output directory')
    parser.add_argument('-f', '--output_format', default='mp4', help='output video format')
    # parse arguments
    args = parser.parse_args()
    # concat videos
    concat_videos(args.input_dir, args.output_dir, args.output_format)

if __name__ == '__main__':
    main()
