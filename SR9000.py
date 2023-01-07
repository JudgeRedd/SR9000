import os
import glob
import argparse
import re
from termcolor2 import c
from logger import log

parser = argparse.ArgumentParser(description='Argument parser description')
parser.add_argument('--directory', '-d', type=str, help='Directory to target')
inputArgs = parser.parse_args()

DIRECTORY = inputArgs.directory
EXTENTIONS = ['mkv', 'mp4']

print(c('''
    ███████ ██    ██ ██████  ████████ ██ ████████ ██      ███████     ██████  ███████ ███    ██  █████  ███    ███ ███████ ██████       █████   ██████   ██████   ██████  
    ██      ██    ██ ██   ██    ██    ██    ██    ██      ██          ██   ██ ██      ████   ██ ██   ██ ████  ████ ██      ██   ██     ██   ██ ██  ████ ██  ████ ██  ████ 
    ███████ ██    ██ ██████     ██    ██    ██    ██      █████       ██████  █████   ██ ██  ██ ███████ ██ ████ ██ █████   ██████       ██████ ██ ██ ██ ██ ██ ██ ██ ██ ██ 
         ██ ██    ██ ██   ██    ██    ██    ██    ██      ██          ██   ██ ██      ██  ██ ██ ██   ██ ██  ██  ██ ██      ██   ██          ██ ████  ██ ████  ██ ████  ██ 
    ███████  ██████  ██████     ██    ██    ██    ███████ ███████     ██   ██ ███████ ██   ████ ██   ██ ██      ██ ███████ ██   ██      █████   ██████   ██████   ██████
''').green.bold)

def main():

    # check if directory was specified
    if(DIRECTORY == None):
        log('No directory specified', 'error')
        return

    # get list of files in directory
    files = os.scandir(DIRECTORY)

    # loop through each file
    for file in files:
        try:
            # check if file is an srt
            if(not file.name.endswith('.srt')):
                continue
            else:
                # get episode number from file name, assume it is in the format S01E01 etc.
                regex = re.compile(r'S\d{2}E\d{2}', re.IGNORECASE)
                episode_number = re.findall(regex, file.name)[0]

                # get list of files that match the episode number
                episode_files = glob.glob(f'*{episode_number}*', root_dir=f'{DIRECTORY}')
                log(f'- Found subtitle file {episode_files[0][:-4]}', 'info')
                
                # check if there are any video files that match the episode number
                if(any(list(filter(x.endswith, EXTENTIONS)) for x in episode_files)):
                    log('  Found matching video file', 'success')

                    # check if there are more than 2 files that match the episode number
                    if(len(episode_files) > 2):
                        log(f'  Too many files ({len(episode_files)}) found', 'error')
                        continue
                else:
                    log('  No matching video file found', 'error')
                    continue


                for ep in episode_files:
                    # get the srt
                    if(ep.endswith('.srt')):
                        sub_file = ep
                    
                    # get the video file
                    if(list(filter(ep.endswith, EXTENTIONS))):
                        ext = list(filter(ep.endswith, EXTENTIONS))
                        video_file = ep

                # check if the files are already named correctly
                if(sub_file[:-4] == video_file[:-4]):
                    log(f'  Subtitle file already named correctly', 'warning')
                    continue

                try:
                    # rename the srt file to match the video file
                    log(f'  Renaming {sub_file} to {video_file.replace(f".{ext[0]}", ".srt")}', 'action')
                    os.rename(f'{DIRECTORY}/{sub_file}', f'{DIRECTORY}/{video_file.replace(f".{ext[0]}", ".srt")}')
                    log(f'  Successfully renamed {sub_file}', 'success')
                except:
                    log(f'  Failed to rename {sub_file}', 'error')
                    continue
        except Exception as e:
            print(c(e))

    print("")

main()