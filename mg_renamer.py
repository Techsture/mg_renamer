#!/usr/bin/env python

# You'll need to `pip install soundfile`

import argparse
import os
import soundfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='System path to directory containing files.')
    args = parser.parse_args()
    directory = args.directory
    file_numbering = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w'    
    ]
    for (dirpath, dirnames, filenames) in os.walk(directory):
        filenames.sort()
        if len(filenames) > 32:
            print(f"More than 32 files in {directory}.  Exiting...")
            exit()
        error_flag = False
        for filename in filenames:
            print(f"Checking {filename}...")
            try:
                wav_file_data = soundfile.SoundFile(f"{dirpath}/{filename}")
                file_length = ( wav_file_data.seek(0, soundfile.SEEK_END) / wav_file_data.samplerate )
                # For troubleshooting purposes:
                #print(f"{filename}\n \
                #    Format: {wav_file_data.format} \n \
                #    Sample Rate: {wav_file_data.samplerate}\n \
                #    Channels: {wav_file_data.channels}\n \
                #    Bit Depth: {wav_file_data.subtype}\n \
                #    Length (in seconds): {file_length} \
                # ")
                if wav_file_data.format != 'WAV':
                    print(f"\t[1] {filename} is not a WAV file.")
                    error_flag = True
                if wav_file_data.samplerate != 48000:
                    print(f"\t[2] {filename} does not have a samplerate of 48kHz.")
                    error_flag = True
                if wav_file_data.channels != 2:
                    print(f"\t[3] {filename} is not Stereo.")
                    error_flag = True
                if wav_file_data.subtype != 'FLOAT':
                    print(f"\t[4] {filename} is not 32-bit.")
                    error_flag = True
                if file_length > 174:
                    print(f"\t[5] {filename} is longer than 174 seconds.")
                    error_flag = True
                if error_flag == False:
                    print("\tOK!")
                soundfile.SoundFile.close(wav_file_data)
            except:
                print(f"\t[1] {filename} is not an audio file.")
                error_flag = True
        if error_flag == False:
            print("\nNo errors found. Continuing...\n")
        else:
            print("\nErrors found!  See above output.  Exiting...")
            exit()
        for filename in filenames:
            new_filename = 'mg' + file_numbering.pop(0) + '.wav'
            print(f"Renaming \"{filename}\" to: {new_filename}")
            os.rename(f'{dirpath}/{filename}', f'{dirpath}/{new_filename}')
    exit()


if __name__ == '__main__':
    main()
