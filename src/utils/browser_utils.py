"""Browser-launch utilities, including WSL URL/path handling."""

import os
import shutil
import subprocess
import webbrowser
from pathlib import Path
from urllib.parse import unquote, urlparse

from src.utils.viewer_server_utils import start_viewer_server, viewer_http_url


def _is_wsl() -> bool:
    # WSL detection
    try:
        return "microsoft" in os.uname().release.lower() or "wsl" in os.uname().release.lower()
    except AttributeError:
        return False


def _wsl_file_uri_to_windows(uri: str) -> str:
    """
    Convert file:///mnt/<drive>/path to file:///C:/path for Windows browsers.
    If the uri doesn't match the pattern, return as-is.
    """
    prefix = "file:///mnt/"
    if not uri.startswith(prefix) or len(uri) <= len(prefix):
        return uri

    drive_letter = uri[len(prefix)]
    if drive_letter < "a" or drive_letter > "z":
        return uri

    rest = uri[len(prefix) + 1 :]
    return f"file:///{drive_letter.upper()}:{rest}"


def _viewer_http_url_from_file_uri(url: str) -> str | None:
    parsed_url = urlparse(url)
    if parsed_url.scheme != "file":
        return None

    file_path = Path(unquote(parsed_url.path))
    if _is_wsl() and parsed_url.netloc and len(parsed_url.netloc) == 2 and parsed_url.netloc[1] == ":":
        drive_letter = parsed_url.netloc[0].lower()
        file_path = Path("/mnt") / drive_letter / unquote(parsed_url.path.lstrip("/"))

    if file_path.suffix.lower() != ".html":
        return None

    if file_path.parent.name != "viewer":
        return None

    start_viewer_server()
    return viewer_http_url(file_path.name)


def take_user_to_browser(url: str) -> None:
    """
    Open the APOD URL in the user's default web browser.

    Returns:
        None
    """
    try:
        local_viewer_http_url = _viewer_http_url_from_file_uri(url)
        if local_viewer_http_url:
            url = local_viewer_http_url

        # If running in WSL, use Windows to open the URL
        if _is_wsl():
            if url.startswith("file://"):
                url = _wsl_file_uri_to_windows(url)
            if shutil.which("wslview"):
                subprocess.run(["wslview", url], check=False)
                return

            # Fallback: Windows start command
            subprocess.run(["cmd.exe", "/c", "start", "", url], check=False)
            return

        print(f"Opening in browser 🌐: {url}")
        webbrowser.open_new_tab(url)

    except Exception as e:
        print(f"Browser error: Unable to open the link. ({e})")
        print(f"URL: {url}")
