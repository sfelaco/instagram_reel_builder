# 📱 **Instagram Reel Builder**

Create stunning Instagram reels from your photos with automatic 9:16 cropping and smooth transitions!

## Features

- ✨ **Automatic 9:16 Cropping**: Images are automatically cropped to Instagram's vertical format
- 🎬 **Smooth Transitions**: Includes zoom in, zoom out, fade in, and fade out effects
- 📐 **Full HD Quality**: Output videos are 1920px height (1080x1920 resolution)
- 🖼️ **Batch Processing**: Upload up to 30 images at once
- 🔄 **Easy Reordering**: Reorder images with up/down buttons after upload
- 🎭 **Custom Transitions**: Select which transitions to use in your video
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
   - Images will appear in the gallery below

4. **Reorder images** (optional):
   - Select an image number in the "Select Image # to Move" field
   - Click "⬆️ Move Up" to move it up in the list
   - Click "⬇️ Move Down" to move it down in the list
   - The video will use the order shown in the list

5. **Select transitions**:
   - Choose which transition effects to use (Zoom In, Zoom Out, Fade In, Fade Out)
   - All transitions are selected by default

6. **Set duration**:
   - Use the slider to set how long each photo appears (default: 4 seconds)

7. **Create video**:
   - Click "Create Video" button
   - Wait for processing (progress bar will show status)

8. **Export**:
   - Preview the video in the interface
   - Click "Export Video" to download the MP4 file

## Technical Details

### Image Processing
- Images are cropped to 9:16 aspect ratio (centered)
- Original height is maintained during cropping
- Final resolution: 1080x1920 pixels (Full HD)
- Supports JPEG and PNG formats
- Button-based reordering (Move Up/Down)

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
