from flask import Flask, render_template, request, redirect, url_for, flash
import os
from pytube import Playlist, YouTube
from fetch_playlist_urls import get_video_urls_from_playlist
from download_videos import download_youtube_video, download_videos_from_file

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        download_type = request.form['download_type']
        url = request.form['url']
        resolution = request.form['resolution']
        refetch = request.form.get('refetch') == 'yes'

        if download_type == 'playlist':
            playlist_title = sanitize_filename(Playlist(url).title)
            output_dir = os.path.join('downloads', playlist_title)
            url_file = os.path.join(output_dir, 'video_urls.txt')

            if os.path.exists(output_dir) and not refetch:
                flash(f"Using existing URLs from {url_file}.")
            else:
                url_file, output_dir, video_urls = get_video_urls_from_playlist(url, refetch)

            if url_file:
                start_index = int(request.form['start_index'])
                end_index = int(request.form['end_index'])
                download_videos_from_file(url_file, start_index, end_index, resolution, output_dir)
        else:
            download_youtube_video(url, resolution, 'downloads')

        return redirect(url_for('progress', resolution=resolution, url=url, download_type=download_type))

    return render_template('index.html')

@app.route('/progress')
def progress():
    resolution = request.args.get('resolution')
    url = request.args.get('url')
    download_type = request.args.get('download_type')
    return render_template('progress.html', resolution=resolution, url=url, download_type=download_type)

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '_')).rstrip()

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
