import requests
import time
import json
import pytube
import os

base_url = 'Your Bot Url'
downloads_folder = os.path.join('.', "Downloads")
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

def set_commands():
    res = requests.get(f'{base_url}/setMyCommands', {
        "commands": json.dumps([
            {
                "command": "start",
                "description": "Start using bot"
            }
        ])
    })
    print(res.json())

def get_updates(offset=None):
    res = requests.get(f'{base_url}/getUpdates', {
        "offset": offset,
        "timeout": "100"
    })
    return res.json()['result']

def send_message(chat_id, text, message_id=None, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": text,
        "reply_to_message_id": message_id
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    requests.post(f'{base_url}/sendMessage', data=data)

def handle_message(message):
    chat_id = message['chat']['id']
    message_text = message['text']

    if message_text == '/start':
        send_message(chat_id, "Please Send Youtube Video link....")
    elif message_text.startswith('!links'):
          url = message_text.split('!links ')[1]
          yt = pytube.YouTube(url)
          video_buttons = []
          audios_buttons = []

          #TODO: can send all formats and there information 
          for data in yt.streaming_data['adaptiveFormats']:
              if 'mimeType' in data and 'video/mp4' in data['mimeType']:
                  video_button = {"text": data['qualityLabel'], "url": data['url']}
                  video_buttons.append([video_button])
              if 'mimeType' in data and 'audio/mp4' in data['mimeType']:
                  audios_button = {"text": data['audioQuality'], "url": data['url']}
                  audios_buttons.append([audios_button])
          
          reply_markup_for_videos = {
              "inline_keyboard": video_buttons
          }
          reply_markup_for_audios = {
              "inline_keyboard": audios_buttons
          }
          send_message(chat_id, f"Avaliable Quality Video: \n{yt.title}", message['message_id'], reply_markup_for_videos)
          send_message(chat_id, f"Avaliable Quality Audio: \n{yt.title}", message['message_id'], reply_markup_for_audios)
          


    elif message_text.startswith('http'):
        streams = None
        try:
            for x in range(0, 4):
                yt = pytube.YouTube(message_text)
                if yt.streams.filter(progressive=True, file_extension='mp4', res="720p"):
                    streams = yt.streams.filter(progressive=True, file_extension='mp4')
                    break
                print("Waiting for stream...")
                time.sleep(1)
        except pytube.exceptions.VideoUnavailable:
            send_message(chat_id, "Error: Video is unavailable.")
            return
        if not streams:
            streams = yt.streams.filter(progressive=True, file_extension='mp4')
            if not streams:
                send_message(chat_id, "Error: No streams found.")
                return
        buttons = [
            [{"text": f"{stream.resolution}", "callback_data": f"{message_text}|{stream.itag}|{message['message_id']}"}]
            for stream in streams
        ]
        reply_markup = {
            "inline_keyboard": buttons
        }
        send_message(chat_id, "Choose the video quality:", message['message_id'], reply_markup)


def handle_callback_query(callback_query):
    chat_id = callback_query['message']['chat']['id']
    message_id = callback_query['message']['message_id']
    data = callback_query['data']

    try:
        video_url, itag, url_message_id = data.split('|')
    except ValueError:
        send_message(chat_id, "Error: Invalid callback data format.")
        return



    try:
        for x in range(0, 4):
            yt = pytube.YouTube(video_url)
            if yt.streams.get_by_itag(itag):
                stream = yt.streams.get_by_itag(itag)
                break
            print("Waiting for stream...")
            time.sleep(1)


    except pytube.exceptions.VideoUnavailable:
        send_message(chat_id, "Error: Video is unavailable.")
        return

    video_path = os.path.join(downloads_folder, stream.default_filename)
    send_message(chat_id, "Downloading...")

    stream.download(downloads_folder)
    send_message(chat_id, "Sending...")

    with open(video_path, 'rb') as video_file:
        Res = requests.post(f'{base_url}/sendDocument', {
            "chat_id": chat_id,
            "caption": yt.title,
            "reply_to_message_id": url_message_id
        }, files={
            'document': video_file
        })
    os.remove(video_path)


def handle_updates(updates):
    for update in updates:
        if 'message' in update:
            handle_message(update['message'])
        elif 'callback_query' in update:
            handle_callback_query(update['callback_query'])
if __name__ == '__main__':
    latest_update_id = None
    set_commands()
    while True:
        updates = get_updates(latest_update_id)
        if updates:
            latest_update_id = updates[-1]['update_id'] + 1
        print(updates)
        handle_updates(updates)

        time.sleep(1)
