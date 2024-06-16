# fetch_playlist_urls.py
from pytube import Playlist
import os

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()

def get_video_urls_from_playlist(playlist_url='', url_file_path='', refetch=False):
    try:
        if playlist_url:
            playlist = Playlist(playlist_url)
            playlist_title = sanitize_filename(playlist.title)
        if url_file_path:      
            playlist_title = url_file_path

        output_dir = os.path.join('downloads', playlist_title)

        if os.path.exists(output_dir) and not refetch:
            print(f"Playlist '{playlist_title}' already exists in the downloads folder.")
            output_file = os.path.join(output_dir, 'video_urls.txt')
            try:
                with open(output_file, 'r') as f:
                    video_urls = f.readlines()
                        
            except Exception as e:
                print(f'An error occurred: {e}')

            return output_file, output_dir, video_urls

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        video_urls = playlist.video_urls
        output_file = os.path.join(output_dir, 'video_urls.txt')
        
        with open(output_file, 'w') as f:
            f.write(f"{playlist_url}\n")
            for url in video_urls:
                f.write(f"{url}\n")
        
        print(f"Video URLs have been written to {output_file}.")
        return output_file, output_dir, video_urls

    except Exception as e:
        print(f'An error occurred: {e}')
        return None, None, []

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    get_video_urls_from_playlist(playlist_url)
