from pytube import Playlist
import os

def sanitize_filename(name):
    # Remove invalid characters from filename
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()

def get_video_urls_from_playlist(playlist_url):
    try:
        # Create a Playlist object with the provided URL
        playlist = Playlist(playlist_url)
        
        # Get the playlist title and sanitize it for use as a folder name
        playlist_title = sanitize_filename(playlist.title)
        output_dir = os.path.join('downloads', playlist_title)
        
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Fetch all video URLs in the playlist
        video_urls = [video_url for video_url in playlist.video_urls]
        
        # Write video URLs to a text file in the playlist directory
        output_file = os.path.join(output_dir, 'video_urls.txt')
        if output_file:
            os.remove(output_file)
        with open(output_file, 'w') as f:
            for url in video_urls:
                f.write(f"{url}\n")
        
        print(f"Video URLs have been written to {output_file}.")
        return output_file, output_dir, video_urls
        
    except Exception as e:
        print(f'An error occurred: {e}')
        return None, None, []

# Example usage
playlist_url = input("Enter the YouTube playlist URL: ")
url_file, output_dir, video_urls = get_video_urls_from_playlist(playlist_url)
