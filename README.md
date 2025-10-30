# .m3u8 Video Capture and Download Script

This project provides a **Python script** that demonstrates how to capture and download `.m3u8` HLS video streams using [Playwright](https://playwright.dev/python/) and [ffmpeg](https://ffmpeg.org/).

It is intended for **educational purposes**, testing, or downloading media you own the rights to.  
⚠️ **Do not use this tool to download DRM-protected or copyrighted content you do not own.**

---

## Overview

The script:

- Launches Chrome with remote debugging enabled.  
- Uses Playwright to monitor network traffic for `.m3u8` URLs.  
- Captures the first valid `.m3u8` stream.  
- Downloads the stream using `ffmpeg`.  
- Organizes files by *course*, *module*, and *title*.  

The workflow is generic and can be adapted to any site that uses `.m3u8` streaming, provided you supply the correct **CSS selectors**.

---

## Requirements

- **Python 3.8+**
- **Playwright**
  ```bash
  pip install playwright
  playwright install chromium
  ```
- **ffmpeg**  
  Ensure `ffmpeg` is installed and available on your system `PATH`.

- **Windows only (by default)** because of the `winsound` module.  
  On Linux/Mac, remove or replace the beep calls.

---

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/GabePearse/m3u8-capture
   cd m3u8-capture
   ```

2. Edit the script:
   - Replace `"path/to/chrome.exe"` with your Chrome executable path.  
   - Replace `"path/to/chrome-user-data"` with a user data directory (temporary is fine).  
   - Replace CSS selectors (`CSS TITLE SELECTOR`, `CSS MODULE SELECTOR`, etc.) with ones matching your target site.  
   - Update `base_dir` to the folder where you want to save videos.

3. Run the script:
   ```bash
   python m3u8_capture.py
   ```

4. Navigate to your video page in Chrome.  
   The script will capture the `.m3u8` URL, download the stream, and save it as an `.mp4`.

---

## Example File Structure

```
saved_videos/
└── Course Name/
    └── Module Name/
        └── Lesson Title.mp4
```

---

## Disclaimer

This project is provided **for educational and personal use only**.  
Do not use it to:
- Download or redistribute copyrighted materials.  
- Circumvent DRM or violate the Terms of Service of any platform.  

The author(s) are not responsible for misuse of this tool.  

