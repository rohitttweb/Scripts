# main.py
import os
from pytube import Playlist
from fetch_playlist_urls import get_video_urls_from_playlist
from download_videos import download_youtube_video, download_videos_from_file

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()

def is_playlist(url):
    return 'playlist' in url


def list_playlists(downloads_dir='downloads'):
    try:
        playlists = [d for d in os.listdir(downloads_dir) if os.path.isdir(os.path.join(downloads_dir, d))]
        print("Available playlists:")
        for i, playlist in enumerate(playlists):
            print(f"{i}. {playlist}")
        
        return playlists
    except Exception as e:
        print(f'An error occurred: {e}')
        return []

def download_single_video(video_url, resolution):
    output_path = 'downloads'
    download_youtube_video(video_url, resolution, output_path)

def main():
    url = input("Enter the YouTube URL (video or playlist): Or p for choosing Existing playlist ").strip()
    resolution = input("Enter the resolution (360p, 720p, 1080p): ").strip()
    if url == 'p':
        playlist_title = list_playlists()
        output_dir = os.path.join('downloads', playlist_title)
        url_file = os.path.join(output_dir, 'video_urls.txt')
        url_file, output_dir, video_urls = get_video_urls_from_playlist(playlist_title , refetch=False)
    
    if is_playlist(url):
        playlist_title = sanitize_filename(Playlist(url).title)
        output_dir = os.path.join('downloads', playlist_title)
        url_file = os.path.join(output_dir, 'video_urls.txt')

        if os.path.exists(output_dir):
            refetch = input(f"Playlist '{playlist_title}' already exists. Do you want to refetch the URLs? (yes/No): ").strip().lower()
            if refetch == 'yes':
                url_file, output_dir, video_urls = get_video_urls_from_playlist(url, refetch=True)
            else:
                print(f"Using existing URLs from {url_file}.")
        else:
            url_file, output_dir, video_urls = get_video_urls_from_playlist(url, refetch=False)

        if url_file:
            start_index = int(input("Enter the starting index (0-based) of the videos to download: "))
            end_index = int(input("Enter the ending index (0-based) of the videos to download: "))
            download_videos_from_file(url_file, start_index, end_index, resolution, output_dir)
    else:
        download_single_video(url, resolution)

if __name__ == "__main__":
    main()
