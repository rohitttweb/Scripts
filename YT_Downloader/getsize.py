from pytube import Playlist, YouTube

def get_video_size(yt, resolution):
    # Try to find the specified resolution stream
    stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
    
    if stream:
        return stream.filesize / (1024 * 1024)  # Convert bytes to megabytes
    else:
        # If specified resolution is not found, get the highest resolution available
        highest_res_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if highest_res_stream:
            return highest_res_stream.filesize / (1024 * 1024)
        else:
            return 0  # Return 0 if no mp4 streams are found

def get_playlist_video_sizes(playlist_url, resolution='720p'):
    playlist = Playlist(playlist_url)
    total_size_bytes_specific = 0
    total_size_bytes_all = 0
    
    for video_url in playlist.video_urls:
        yt = YouTube(video_url)
        
        # Calculate size for specific resolution
        size_mb_specific = get_video_size(yt, resolution)
        if size_mb_specific > 0:
            total_size_bytes_specific += size_mb_specific * (1024 * 1024)  # Convert MB back to bytes for total calculation
        
        # Calculate size for all streams (highest available resolution)
        highest_res_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if highest_res_stream:
            total_size_bytes_all += highest_res_stream.filesize
        
        # Print details for specific resolution
        if size_mb_specific > 0:
            print(f"Video Title: {yt.title}")
            print(f"File Size ({resolution}): {size_mb_specific:.2f} MB")
        else:
            print(f"No {resolution} stream found for video: {yt.title}")
    
    total_size_mb_specific = total_size_bytes_specific / (1024 * 1024)  # Total size for specific resolution in megabytes
    total_size_mb_all = total_size_bytes_all / (1024 * 1024)  # Total size for all videos in megabytes
    
    print(f"Total Size of {resolution} streams in Playlist: {total_size_mb_specific:.2f} MB")
    print(f"Total Size of all streams (highest available resolution) in Playlist: {total_size_mb_all:.2f} MB")

# Example usage:
if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    resolution = input("Enter the resolution (e.g., 720p, 1080p): ")
    get_playlist_video_sizes(playlist_url, resolution)
