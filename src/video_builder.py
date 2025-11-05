"""Video builder module for creating slideshow videos with transitions."""

from typing import List, Callable
import numpy as np
from moviepy import ImageClip, concatenate_videoclips, VideoClip, vfx


class VideoBuilder:
    """Build slideshow videos with transitions."""
    
    TRANSITION_DURATION = 0.5  # Duration of transitions in seconds
    
    @staticmethod
    def create_zoom_in_clip(image: np.ndarray, duration: float) -> VideoClip:
        """
        Create a clip with slow zoom-in effect.
        
        Args:
            image: Image as numpy array
            duration: Duration of the clip in seconds
            
        Returns:
            VideoClip with zoom-in effect
        """
        def make_frame(t):
            # Calculate zoom factor (1.0 to 1.2)
            zoom = 1.0 + (t / duration) * 0.2
            h, w = image.shape[:2]
            
            # Calculate new dimensions
            new_h, new_w = int(h * zoom), int(w * zoom)
            
            # Resize image
            from PIL import Image as PILImage
            pil_img = PILImage.fromarray(image)
            zoomed = pil_img.resize((new_w, new_h), PILImage.Resampling.LANCZOS)
            zoomed_array = np.array(zoomed)
            
            # Crop to center
            crop_y = (new_h - h) // 2
            crop_x = (new_w - w) // 2
            cropped = zoomed_array[crop_y:crop_y+h, crop_x:crop_x+w]
            
            return cropped
        
        return VideoClip(make_frame, duration=duration)
    
    @staticmethod
    def create_zoom_out_clip(image: np.ndarray, duration: float) -> VideoClip:
        """
        Create a clip with slow zoom-out effect.
        
        Args:
            image: Image as numpy array
            duration: Duration of the clip in seconds
            
        Returns:
            VideoClip with zoom-out effect
        """
        def make_frame(t):
            # Calculate zoom factor (1.2 to 1.0)
            zoom = 1.2 - (t / duration) * 0.2
            h, w = image.shape[:2]
            
            # Calculate new dimensions
            new_h, new_w = int(h * zoom), int(w * zoom)
            
            # Resize image
            from PIL import Image as PILImage
            pil_img = PILImage.fromarray(image)
            zoomed = pil_img.resize((new_w, new_h), PILImage.Resampling.LANCZOS)
            zoomed_array = np.array(zoomed)
            
            # Crop to center
            crop_y = (new_h - h) // 2
            crop_x = (new_w - w) // 2
            cropped = zoomed_array[crop_y:crop_y+h, crop_x:crop_x+w]
            
            return cropped
        
        return VideoClip(make_frame, duration=duration)
    
    @staticmethod
    def create_fade_in_clip(image: np.ndarray, duration: float) -> VideoClip:
        """
        Create a clip with fade-in effect.
        
        Args:
            image: Image as numpy array
            duration: Duration of the clip in seconds
            
        Returns:
            VideoClip with fade-in effect
        """
        clip = ImageClip(image, duration=duration)
        return clip.with_effects([vfx.FadeIn(VideoBuilder.TRANSITION_DURATION)])
    
    @staticmethod
    def create_fade_out_clip(image: np.ndarray, duration: float) -> VideoClip:
        """
        Create a clip with fade-out effect.
        
        Args:
            image: Image as numpy array
            duration: Duration of the clip in seconds
            
        Returns:
            VideoClip with fade-out effect
        """
        clip = ImageClip(image, duration=duration)
        return clip.with_effects([vfx.FadeOut(VideoBuilder.TRANSITION_DURATION)])
    
    @staticmethod
    def create_slideshow(
        images: List[np.ndarray], 
        duration_per_image: float = 4.0,
        output_path: str = "output.mp4",
        transitions: List[str] = None,
        progress_callback: Callable[[int, int, str], None] = None
    ) -> str:
        """
        Create a slideshow video from processed images with transitions.
        
        Args:
            images: List of processed images as numpy arrays
            duration_per_image: Duration each image is shown (seconds)
            output_path: Path to save the output video
            transitions: List of transition names to use (e.g., ['zoom_in', 'fade_out'])
            progress_callback: Optional callback for progress updates
            
        Returns:
            Path to the created video file
        """
        if not images:
            raise ValueError("No images provided")
        
        # Map transition names to functions
        transition_map = {
            'zoom_in': VideoBuilder.create_zoom_in_clip,
            'zoom_out': VideoBuilder.create_zoom_out_clip,
            'fade_in': VideoBuilder.create_fade_in_clip,
            'fade_out': VideoBuilder.create_fade_out_clip,
        }
        
        # Use all transitions if none specified
        if not transitions:
            transitions = ['zoom_in', 'zoom_out', 'fade_in', 'fade_out']
        
        # Build list of transition functions based on selected transitions
        transition_funcs = [transition_map[t] for t in transitions if t in transition_map]
        
        if not transition_funcs:
            raise ValueError("No valid transitions selected")
        
        clips = []
        total = len(images)
        
        if progress_callback:
            progress_callback(0, total, "Creating video clips...")
        
        # Create clips with alternating transitions
        for idx, image in enumerate(images):
            # Select transition (cycle through selected transitions)
            transition_func = transition_funcs[idx % len(transition_funcs)]
            clip = transition_func(image, duration_per_image)
            clips.append(clip)
            
            if progress_callback:
                progress_callback(idx + 1, total, f"Creating clip {idx + 1}/{total}")
        
        if progress_callback:
            progress_callback(total, total, "Concatenating clips...")
        
        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method="compose")
        
        if progress_callback:
            progress_callback(total, total, "Writing video file...")
        
        # Write video file
        final_video.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio=False,
            preset='medium',
            logger=None  # Suppress moviepy progress bar
        )
        
        # Clean up
        final_video.close()
        for clip in clips:
            clip.close()
        
        if progress_callback:
            progress_callback(total, total, "Video created successfully!")
        
        return output_path
