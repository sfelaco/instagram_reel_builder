"""Image processor module for cropping and resizing images to 9:16 aspect ratio."""

from typing import List, Tuple
from pathlib import Path
from PIL import Image
import numpy as np


class ImageProcessor:
    """Process images for Instagram reels (9:16 aspect ratio)."""
    
    TARGET_HEIGHT = 1920
    TARGET_WIDTH = int(TARGET_HEIGHT * 9 / 16)  # 1080px
    ASPECT_RATIO = 9 / 16
    
    @staticmethod
    def crop_to_9_16(image: Image.Image) -> Image.Image:
        """
        Crop image to 9:16 aspect ratio, centered.
        Maintains original height, adjusts width.
        
        Args:
            image: PIL Image to crop
            
        Returns:
            Cropped PIL Image
        """
        width, height = image.size
        
        # Calculate target width for 9:16 ratio based on current height
        target_width = int(height * ImageProcessor.ASPECT_RATIO)
        
        # If image is already narrower than target, no cropping needed
        if width <= target_width:
            return image
        
        # Calculate crop box (centered)
        left = (width - target_width) // 2
        right = left + target_width
        top = 0
        bottom = height
        
        return image.crop((left, top, right, bottom))
    
    @staticmethod
    def resize_to_target(image: Image.Image) -> Image.Image:
        """
        Resize image to target dimensions (1920px height, maintaining aspect ratio).
        
        Args:
            image: PIL Image to resize
            
        Returns:
            Resized PIL Image
        """
        # Calculate new dimensions maintaining aspect ratio
        width, height = image.size
        aspect_ratio = width / height
        
        new_height = ImageProcessor.TARGET_HEIGHT
        new_width = int(new_height * aspect_ratio)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def process_image(image_path: str) -> np.ndarray:
        """
        Process a single image: crop to 9:16 and resize to 1920px height.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Processed image as numpy array (RGB)
        """
        # Load image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary (handles RGBA, grayscale, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Crop to 9:16 aspect ratio (centered)
        cropped = ImageProcessor.crop_to_9_16(image)
        
        # Resize to target height (1080px)
        resized = ImageProcessor.resize_to_target(cropped)
        
        # Convert to numpy array
        return np.array(resized)
    
    @staticmethod
    def process_images(image_paths: List[str], progress_callback=None) -> List[np.ndarray]:
        """
        Process multiple images.
        
        Args:
            image_paths: List of paths to image files
            progress_callback: Optional callback function for progress updates
            
        Returns:
            List of processed images as numpy arrays
        """
        processed_images = []
        total = len(image_paths)
        
        for idx, path in enumerate(image_paths):
            processed = ImageProcessor.process_image(path)
            processed_images.append(processed)
            
            if progress_callback:
                progress_callback(idx + 1, total, f"Processing image {idx + 1}/{total}")
        
        return processed_images
