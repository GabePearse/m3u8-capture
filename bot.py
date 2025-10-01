"""Manual .m3u8 video capture and download script.

This script uses Playwright and ffmpeg to monitor network traffic
for `.m3u8` URLs in the network section of google, then downloads
the corresponding video files. It automates Chrome with remote
debugging and handles course/module navigation until completion.
"""

from playwright.sync_api import sync_playwright
import re
from datetime import datetime
import subprocess
import os
import time
import winsound

PATTERN = r'^.m3u8$'
RE = re.compile(PATTERN)

# The course page URL (leave blank or update manually)
COURSE_URL = "https://example.com/course"


def sanitize_filename(name):
    """Remove invalid characters from a filename.

    Args:
        name: The original filename string.

    Returns:
        A sanitized version of `name` safe for filesystem use.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)


def launch_chrome():
    """Launch Chrome with remote debugging enabled.

    Opens Chrome using a custom user data directory so that
    Playwright can connect over the Chrome DevTools Protocol.
    """
    chrome_path = r"path/to/chrome.exe"
    user_data_dir = r"path/to/chrome-user-data"

    command = [
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={user_data_dir}"
    ]

    subprocess.Popen(command)


def download_m3u8(input_url, course, module, title):
    """Download a video from a given `.m3u8` URL using ffmpeg.

    Args:
        input_url: The `.m3u8` playlist URL.
        course: The course name (used as a directory).
        module: The module name (used as a subdirectory).
        title: The video title (used as filename).

    Side Effects:
        Creates directories for course/module if needed.
        Writes an `.mp4` video file.
        Prints progress of conversion to stdout.
    """
    base_dir = r"path/to/save/videos"
    output_dir = os.path.join(base_dir, course, module)
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{title}.mp4")

    command = [
        "ffmpeg",  # assumes ffmpeg is on PATH
        "-n",
        "-i", input_url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        output_file
    ]

    time_regex = re.compile(r"time=(\d+):(\d+):(\d+).(\d+)")

    with subprocess.Popen(command, stderr=subprocess.PIPE, text=True, bufsize=1) as process:
        for line in process.stderr:
            line = line.strip()
            match = time_regex.search(line)
            if match:
                hours, minutes, seconds, centis = map(int, match.groups())
                print(f"\rConverted duration so far: "
                      f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centis:02d}", end="")
        process.wait()
        print(f"\nDownload complete: {output_file}")


def now():
    """Return the current datetime."""
    return datetime.now()


def run():
    """Main entry point for monitoring and downloading course videos.

    Launches Chrome, attaches Playwright, monitors network traffic for
    `.m3u8` URLs, downloads videos, and handles navigation between modules
    until course completion.
    """
    launch_chrome()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        page.pause()

        def on_response(response):
            """Handle network responses and capture `.m3u8` video URLs."""
            if check_course_completion():
                return

            url = response.url
            if RE.fullmatch(url):
                if getattr(page, "_m3u8_captured", False):
                    return  # already handled

                page._m3u8_captured = True

                try:
                    title = page.query_selector(
                        "CSS TITLE SELECTOR"
                    )
                    module = page.query_selector(
                        "CSS MODULE SELECTOR"
                    )
                    course = page.query_selector(
                        "CSS COURSE SELECTOR"
                    )
                except Exception as e:
                    print("Error grabbing headings:", e)

                start_time = time.perf_counter()

                download_m3u8(
                    url,
                    sanitize_filename(course.inner_text()),
                    sanitize_filename(module.inner_text()),
                    sanitize_filename(title.inner_text())
                )

                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                minutes = int(elapsed_time // 60)
                seconds = elapsed_time % 60
                print(f"Script execution time: {minutes} minutes and {seconds:.2f} seconds")

                try:
                    button = page.wait_for_selector('CSS NEXT VIDEO SELECTOR', timeout=2000)
                    button.click()
                    print("Clicked next video button")
                except Exception as e:
                    print("Could not click complete video button:", e)

                try:
                    button = page.wait_for_selector('CSS NEXT MODULE SELECTOR', timeout=2000)
                    button.click()
                    print("Clicked 'Next Module' button")
                except Exception as e:
                    print("Could not click next module button:", e)

        def reset_capture_flag(frame):
            """Reset capture flag when navigating to a new page/frame."""
            if hasattr(page, "_m3u8_captured"):
                page._m3u8_captured = False
                print("Page navigated – ready to capture new .m3u8")

        def check_course_completion():
            """Check whether the course has reached 100% completion.

            Returns:
                True if the course is completed, False otherwise.
            """
            try:
                percent_elem = page.query_selector("CSS PROGRESS BAR")
                if percent_elem:
                    percent_text = percent_elem.inner_text().strip().replace("%", "")
                    if percent_text.isdigit() and int(percent_text) >= 100:
                        print("Course is 100% complete!")
                        winsound.Beep(700, 700)
                        page.pause()  # Or browser.close()
                        return True
            except Exception as e:
                print("Error checking completion:", e)
            return False

        page.on("framenavigated", reset_capture_flag)
        page.on("response", on_response)

        print("Monitoring network requests for .m3u8 URLs...")
        page.wait_for_timeout(600000)


if __name__ == "__main__":
    run()
