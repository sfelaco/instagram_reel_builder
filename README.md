# 📱 Instagram Reel Builder

Create stunning Instagram reels from your photos with automatic 9:16 cropping and smooth transitions!

## Features

- ✨ **Automatic 9:16 Cropping**: Images are automatically cropped to Instagram's vertical format
- 🎬 **Smooth Transitions**: Includes zoom in, zoom out, fade in, and fade out effects
- 📐 **HD Quality**: Output videos are 1080px height (608x1080 resolution)
- 🖼️ **Batch Processing**: Upload up to 30 images at once
- ⏱️ **Customizable Duration**: Set how long each photo appears (1-10 seconds)
- 🎨 **Modern UI**: Easy-to-use Gradio interface
- 💾 **Easy Export**: Download your video with one click

## Installation

### Using Poetry (Recommended)

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run the application
python src/main.py
```

### Using pip

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install gradio pillow opencv-python numpy moviepy

# Run the application
python src/main.py
```

## Usage

1. **Start the application**:
   ```bash
   python src/main.py
   ```

2. **Open your browser** at `http://localhost:7860`

3. **Upload images**:
   - Click "Upload Images" and select up to 30 JPEG or PNG files
   - Images will be processed in the order you upload them

4. **Set duration**:
   - Use the slider to set how long each photo appears (default: 4 seconds)

5. **Create video**:
   - Click "Create Video" button
   - Wait for processing (progress bar will show status)

6. **Export**:
   - Preview the video in the interface
   - Click "Export Video" to download the MP4 file

## Technical Details

### Image Processing
- Images are cropped to 9:16 aspect ratio (centered)
- Original height is maintained during cropping
- Final resolution: 608x1080 pixels
- Supports JPEG and PNG formats

### Video Creation
- Format: MP4 (H.264 codec)
- Frame rate: 30 fps
- Transitions: Zoom in, zoom out, fade in, fade out (alternating)
- Transition duration: 0.5 seconds

### Transitions
The tool cycles through four transition effects:
1. **Zoom In**: Slow zoom from 100% to 120%
2. **Zoom Out**: Slow zoom from 120% to 100%
3. **Fade In**: Gradual appearance from black
4. **Fade Out**: Gradual disappearance to black

## Project Structure

```
instagram_reel_builder/
├── src/
│   ├── main.py              # Gradio UI and main application
│   ├── image_processor.py   # Image cropping and resizing
│   └── video_builder.py     # Video creation with transitions
├── pyproject.toml           # Poetry dependencies
└── README.md               # This file
```

## Requirements

- Python 3.11 or higher
- Dependencies:
  - gradio >= 4.0.0
  - pillow >= 10.0.0
  - opencv-python >= 4.8.0
  - numpy >= 1.24.0
  - moviepy >= 1.0.3

## Troubleshooting

### MoviePy Issues
If you encounter issues with MoviePy, you may need to install ffmpeg:

**Windows**:
```bash
# Using chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS**:
```bash
brew install ffmpeg
```

**Linux**:
```bash
sudo apt-get install ffmpeg
```

### Memory Issues
If processing many large images causes memory issues:
- Reduce the number of images
- Reduce the duration per image
- Process images in smaller batches

## License

MIT License - Feel free to use and modify as needed!

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
