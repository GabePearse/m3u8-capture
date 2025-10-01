# Documentation Summary for m3u8_capture.py

## Module Overview
Manual `.m3u8` video capture and download script.

This script uses Playwright and ffmpeg to monitor network traffic for `.m3u8` URLs,  
then downloads the corresponding video files. It automates Chrome with remote debugging  
and handles course/module navigation until completion.

---

## Functions

### sanitize_filename(name)
Remove invalid characters from a filename.

**Args:**
- `name`: The original filename string.

**Returns:**
- A sanitized version of `name` safe for filesystem use.

---

### launch_chrome()
Launch Chrome with remote debugging enabled.

Opens Chrome using a custom user data directory so that
Playwright can connect over the Chrome DevTools Protocol.

---

### download_m3u8(input_url, course, module, title)
Download a video from a given `.m3u8` URL using ffmpeg.

**Args:**
- `input_url`: The `.m3u8` playlist URL.
- `course`: The course name (used as a directory).
- `module`: The module name (used as a subdirectory).
- `title`: The video title (used as filename).

**Side Effects:**
- Creates directories for course/module if needed.
- Writes an `.mp4` video file.
- Prints progress of conversion to stdout.

---

### now()
Return the current datetime.

**Returns:**
- `datetime`: Current timestamp.

---

### run()
Main entry point for monitoring and downloading course videos.

Launches Chrome, attaches Playwright, monitors network traffic for
`.m3u8` URLs, downloads videos, and handles navigation between modules
until course completion.

---

#### Nested Functions in `run()`

**on_response(response)**  
Handle network responses and capture `.m3u8` video URLs.

---

**reset_capture_flag(frame)**  
Reset capture flag when navigating to a new page/frame.

---

**check_course_completion()**  
Check whether the course has reached 100% completion.

**Returns:**
- `True` if the course is completed, `False` otherwise.

---

## Usage
Run the script directly to start monitoring and downloading:

```bash
python m3u8_capture.py
```