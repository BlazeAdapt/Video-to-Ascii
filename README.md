# Video To Ascii Art

Play any video in your terminal as colored ASCII art, with audio.

(Or simply a constant art is displayed if an image is given as argument)

Frames are converted first, and saved to a cache so the next playback of the same video starts instantly.


## Features

- **Truecolor ASCII rendering**: each character is tinted with the pixel's color (24-bit ANSI)
- **Per-video cache**: a finished dump is reused automatically on later runs
- **Aspect-ratio correction**: output fits your terminal without looking stretched
- **Clean terminal handling**: uses the alternate screen, hides the cursor, and restores everything on exit

## Requirements

- Python 3.8+
- A terminal with truecolor support (most modern terminals do)

Python packages:

```bash
pip install opencv-python numpy pygame moviepy
```

## Usage

```bash
python vidtoascii.py path/to/video.mp4
```
Unless `tput` is supported on your terminal, You will have to swap the `width` and `height` in the code to whatever your terminal supports.
```python
import shutil
width, height = shutil.get_terminal_size()
width-=1
height-=1
```
`height` is kept 1 less than terminal height so as to not cause problems due to automatic scrolling.
Press `Ctrl+C` to quit.

Tip: make the terminal window the size you want **before** starting. The output is sized to fit the terminal at launch.

## How the cache works

Dumps and extracted audio are stored in `cache/` next to where you run the script.

The dump's filename includes a hash of:

- the video's absolute path, file size and modified time
- the terminal size (columns x rows)
- the color quantization setting

That means the cache is reused only when it's actually valid. Editing the video, resizing the terminal, or changing quantization produces a new dump rather than playing a stale one.

To clear everything, delete the `cache/` folder.

## How it works

1. **Read** the video sequentially with OpenCV, using `video.read()` with `frame_id` to skip frames you don't need (no seeking).
2. **Render** each frame: resize to the terminal grid, map luminance to a character ramp, quantize colors, and only emit a color escape code when the color changes.
3. **Cache** each frame to a .cache, length-prefixed file as it's produced.
4. **Play** by reading each frame from the cache file generated, played at a valid fps for the video close to 12.

## Configuration

Constants at the top of `vidtoascii.py`:

| Constant        | Purpose                                                        |
|-----------------|----------------------------------------------------------------|
| `QUANT`   | Color bucket size. Higher means fewer escape codes and a faster, blockier look |
| `scale`          | Characters used for brightness, in order                       |
| `width & height` | Change this to your terminal's size if retrieving through python is not an option |

## Limitations

- No pause, seek or volume controls yet
- Long videos produce large dumps
- Large terminal sizes have a slower frame writing time, and hence the video may lag behind the audio

