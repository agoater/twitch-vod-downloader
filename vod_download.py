import os
from pathlib import Path

import requests
import yt_dlp
from yt_dlp.utils import sanitize_filename


# Twitch API endpoints
TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
TWITCH_USERS_URL = "https://api.twitch.tv/helix/users"
TWITCH_VIDEOS_URL = "https://api.twitch.tv/helix/videos"


def getToken(client_id: str, client_secret: str) -> str:
    """
    Request an app access token from Twitch using client credentials.

    Args:
        client_id: Twitch application client ID.
        client_secret: Twitch application client secret.

    Returns:
        A Twitch OAuth access token as a string.

    Raises:
        requests.HTTPError: If the token request fails.
    """
    response = requests.post(
        TWITCH_TOKEN_URL,
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
    )
    response.raise_for_status()

    data = response.json()
    return data["access_token"]


def getUserID(username: str, client_id: str, access_token: str) -> str:
    """
    Look up a Twitch user's numeric ID from their username/login.

    Args:
        username: Twitch channel username.
        client_id: Twitch application client ID.
        access_token: Valid Twitch OAuth access token.

    Returns:
        The Twitch user ID as a string.

    Raises:
        ValueError: If the username is not found.
        requests.HTTPError: If the API request fails.
    """
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        TWITCH_USERS_URL,
        params={"login": username},
        headers=headers
    )
    response.raise_for_status()

    data = response.json().get("data", [])
    if not data:
        raise ValueError(f"User '{username}' was not found.")

    return data[0]["id"]


def getVideos(username: str, client_id: str, access_token: str) -> list[dict]:
    """
    Fetch video metadata for a Twitch user's channel.

    Args:
        username: Twitch channel username.
        client_id: Twitch application client ID.
        access_token: Valid Twitch OAuth access token.

    Returns:
        A list of video metadata dictionaries from the Twitch API.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    user_id = getUserID(username, client_id, access_token)

    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(
        TWITCH_VIDEOS_URL,
        params={"user_id": user_id},
        headers=headers
    )
    response.raise_for_status()

    return response.json().get("data", [])


def downloadVideos(url: str, download_dir: Path) -> None:
    """
    Download a Twitch video using yt-dlp.

    Args:
        url: Direct Twitch video URL.
        download_dir: Directory where downloaded files should be saved.
    """
    ydl_opts = {
        # Save files as: title-id.extension
        "outtmpl": str(download_dir / "%(title)s-%(id)s.%(ext)s"),
        # Keep filenames filesystem-safe
        "restrictfilenames": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main() -> None:
    """
    Main program flow:
    1. Read Twitch API credentials from environment variables.
    2. Fetch an access token.
    3. Fetch videos for the selected channel.
    4. Skip videos that appear to already exist locally.
    5. Download missing videos.
    """
    channel_name = "USERNAME"  # Change this to the Twitch channel you want to download from
    download_dir = Path.home() # Set the path to a directory to store the downloaded videos

    # Ensure the download directory exists
    download_dir.mkdir(parents=True, exist_ok=True)

    # Read Twitch API credentials from environment variables
    client_id = os.getenv("TWITCH_CLIENT_ID")
    client_secret = os.getenv("TWITCH_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise EnvironmentError(
            "Please set TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET environment variables."
        )

    # Authenticate with Twitch and fetch available videos
    access_token = getToken(client_id, client_secret)
    videos = getVideos(channel_name, client_id, access_token)

    for video in videos:
        # Sanitize the title so it matches the filename style used by yt-dlp
        safe_title = sanitize_filename(video["title"], restricted=True)
        file_path = download_dir / f"{safe_title}.mp4"

        # Skip download if the file already exists
        # Note: yt-dlp saves as title-id.ext, so this check may not perfectly match final filenames.
        if file_path.is_file():
            print(f"Skipping existing file: {file_path.name}")
            continue

        print(f"Downloading: {video['title']}")
        downloadVideos(video["url"], download_dir)


if __name__ == "__main__":
    main()