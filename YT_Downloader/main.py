import os
from pytube import YouTube

def sanitize_filename(name):
    allowed_chars = "._"  # Allow dots and underscores in addition to alphanumerics and spaces
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
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Create a YouTube object with the provided URL
        yt = YouTube(video_url)
        stream = get_stream_by_resolution(yt, resolution)
        
        if stream is None:
            return
        
        # Determine the expected filename with resolution
        filename = sanitize_filename(f"{yt.title} ({stream.resolution}).{stream.subtype}")
        filepath = os.path.join(output_path, filename)
        
        # Check if the file already exists
        if os.path.exists(filepath):
            print(f"{filename} already exists. Skipping download.")
            return
        
        # Download the chosen stream
        print(f'Downloading {yt.title} at {stream.resolution} resolution...')
        stream.download(output_path, filename=filename)
        print('Download completed successfully.')
        
    except Exception as e:
        print(f'An error occurred: {e}')

def download_videos_from_file(file_path, start_index, end_index, resolution, output_path='.'):
    try:
        with open(file_path, 'r') as f:
            video_urls = f.readlines()
        
        # Download the specified range of videos
        for i in range(start_index, end_index + 1):
            video_url = video_urls[i].strip()
            print(video_url)
            download_youtube_video(video_url, resolution, output_path)
            
    except Exception as e:
        print(f'An error occurred: {e}')

def list_playlists(downloads_dir='downloads'):
    try:
        # List all directories in the downloads folder
        playlists = [d for d in os.listdir(downloads_dir) if os.path.isdir(os.path.join(downloads_dir, d))]
        print("Available playlists:")
        for i, playlist in enumerate(playlists):
            print(f"{i}. {playlist}")
        return playlists
    except Exception as e:
        print(f'An error occurred: {e}')
        return []

# Example usage
downloads_dir = 'downloads'  # Directory where playlists are stored
playlists = list_playlists(downloads_dir)

if playlists:
    playlist_index = int(input("Enter the number of the playlist you want to download from: "))
    chosen_playlist = playlists[playlist_index]
    file_path = os.path.join(downloads_dir, chosen_playlist, 'video_urls.txt')
    
    start_index = int(input("Enter the starting index (0-based) of the videos to download: "))
    end_index = int(input("Enter the ending index (0-based) of the videos to download: "))
    resolution = input("Enter the resolution (360p, 720p, 1080p): ")
    output_path = os.path.join(downloads_dir, chosen_playlist)  # Use the same directory as the URLs file
    download_videos_from_file(file_path, start_index, end_index, resolution, output_path)
else:
    print("No playlists found in the downloads directory.")
