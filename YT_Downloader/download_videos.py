# download_videos.py
import os
from pytube import YouTube

def sanitize_filename(name):
    allowed_chars = "._"
    return "".join(c for c in name if c.isalnum() or c in allowed_chars or c == ' ').rstrip()

def get_stream_by_resolution(yt, resolution):
    streams = yt.streams.filter(progressive=True, file_extension='mp4', res=resolution)
    if streams:
        return streams.first()
    else:
        print(f"No stream found for resolution {resolution}.")
        return None

def download_youtube_video(video_url, resolution, output_path='.'):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        yt = YouTube(video_url)
        stream = get_stream_by_resolution(yt, resolution)

        if stream is None:
            return
        
        filename = sanitize_filename(f"{yt.title} ({stream.resolution}).{stream.subtype}")
        filepath = os.path.join(output_path, filename)

        if os.path.exists(filepath):
            print(f"{filename} already exists. Skipping download.")
            return
        print(f'Downloading.... {filename}.')
        stream.download(output_path, filename=filename)
        
        print('Download completed successfully.')

    except Exception as e:
        print(f'An error occurred: {e}')

def download_videos_from_file(file_path, start_index, end_index, resolution, output_path='.'):
    try:
        with open(file_path, 'r') as f:
            video_urls = f.readlines()
        
        for i in range(start_index, end_index + 1):
            video_url = video_urls[i].strip()
            download_youtube_video(video_url, resolution, output_path)

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    file_path = input("Enter the path to the video URLs file: ")
    start_index = int(input("Enter the starting index (0-based) of the videos to download: "))
    end_index = int(input("Enter the ending index (0-based) of the videos to download: "))
    resolution = input("Enter the resolution (360p, 720p, 1080p): ")
    output_path = os.path.dirname(file_path)
    download_videos_from_file(file_path, start_index, end_index, resolution, output_path)
    