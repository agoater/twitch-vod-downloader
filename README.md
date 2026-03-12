# Twitch Video Downloader

A Python script that downloads videos from a Twitch channel using the Twitch API and `yt-dlp`.

## How It Works

The script:

- Authenticates with the Twitch API using a client ID and secret
- Fetches the list of videos from a specified Twitch channel
- Checks whether videos already exist locally
- Downloads any missing videos using `yt-dlp`

---

## Features

- Uses the official Twitch API
- Automatically retrieves channel videos
- Skips videos that appear to already exist locally
- Uses `yt-dlp` for reliable downloading
- Saves videos with safe filenames

---

## Requirements

Python **3.9+** recommended.

Install dependencies:

```bash
pip install requests yt-dlp
```

---

## Setup

You must create a Twitch application to obtain API credentials.

1. Go to the Twitch Developer Console:  
   https://dev.twitch.tv/console/apps

2. Create an application and copy your:

- **Client ID**
- **Client Secret**

3. Set them as environment variables.

### Linux / macOS

```bash
export TWITCH_CLIENT_ID="your_client_id"
export TWITCH_CLIENT_SECRET="your_client_secret"
```

### Windows (PowerShell)

```powershell
$env:TWITCH_CLIENT_ID="your_client_id"
$env:TWITCH_CLIENT_SECRET="your_client_secret"
```

---

## Configuration

Edit the following variables in the script:

```python
channel_name = "USERNAME"
download_dir = Path.home()
```

- `channel_name` → Twitch username to download videos from  
- `download_dir` → Folder where videos will be saved

---

## Usage

Run the script:

```bash
python vod_downloader.py
```

---

## Output

Downloaded files are saved as:

```
title-id.extension
```

Example:

```
My_Stream_Title-123456789.mp4
```
