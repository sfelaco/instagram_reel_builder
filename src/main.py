"""Instagram Reel Builder - Main application with Gradio UI."""

import gradio as gr
from pathlib import Path
import tempfile
import shutil
from typing import List, Optional, Tuple
import time

from image_processor import ImageProcessor
from video_builder import VideoBuilder


class ReelBuilder:
    """Main application class for building Instagram reels."""
    
    def __init__(self):
        self.processed_images: List = []
        self.output_video_path: Optional[str] = None
        self.temp_dir = None
    
    def process_and_create_video(
        self, 
        uploaded_files: List, 
        duration: float,
        transitions: List[str],
        progress=gr.Progress()
    ) -> Tuple[Optional[str], str]:
        """
        Process uploaded images and create slideshow video.
        
        Args:
            uploaded_files: List of uploaded file objects from Gradio
            duration: Duration per image in seconds
            transitions: List of selected transition names
            progress: Gradio progress tracker
            
        Returns:
            Tuple of (video_path, status_message)
        """
        try:
            if not uploaded_files:
                return None, "❌ No images uploaded. Please upload at least one image."
            
            if len(uploaded_files) > 30:
                return None, f"❌ Too many images ({len(uploaded_files)}). Maximum is 30 images."
            
            # Create temporary directory for processing
            if self.temp_dir:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            self.temp_dir = tempfile.mkdtemp()
            
            # Extract file paths from uploaded files
            image_paths = [file.name for file in uploaded_files]
            
            # Validate file types
            valid_extensions = {'.jpg', '.jpeg', '.png'}
            for path in image_paths:
                ext = Path(path).suffix.lower()
                if ext not in valid_extensions:
                    return None, f"❌ Invalid file type: {Path(path).name}. Only JPEG and PNG are supported."
            
            # Process images
            status_msg = "🔄 Processing images...\n"
            progress(0.1, desc="Processing images...")
            
            total_images = len(image_paths)
            for idx, path in enumerate(image_paths):
                progress((idx + 1) / total_images * 0.4, desc=f"Processing image {idx + 1}/{total_images}")
            
            self.processed_images = ImageProcessor.process_images(image_paths)
            
            status_msg += f"✅ {len(self.processed_images)} images processed\n\n"
            status_msg += "🎬 Creating video with transitions...\n"
            progress(0.5, desc="Creating video clips...")
            
            # Create output video path
            output_filename = f"instagram_reel_{int(time.time())}.mp4"
            self.output_video_path = str(Path(self.temp_dir) / output_filename)
            
            # Create video with transitions
            progress(0.7, desc="Applying transitions...")
            
            VideoBuilder.create_slideshow(
                self.processed_images,
                duration_per_image=duration,
                output_path=self.output_video_path,
                transitions=transitions,
                progress_callback=None
            )
            
            progress(0.9, desc="Finalizing video...")
            status_msg += "✅ Transitions applied\n"
            status_msg += "✅ Video encoding complete\n\n"
            progress(1.0, desc="✅ Complete!")
            
            final_status = (
                f"✅ VIDEO CREATED SUCCESSFULLY!\n\n"
                f"📊 Statistics:\n"
                f"  • Images processed: {len(self.processed_images)}\n"
                f"  • Duration per image: {duration}s\n"
                f"  • Total video duration: {len(self.processed_images) * duration}s\n"
                f"  • Resolution: 1080x1920 (9:16 Full HD)\n"
                f"  • Format: MP4 (H.264)\n\n"
                f"💾 Click 'Export Video' button to download."
            )
            
            return (self.output_video_path, final_status)
            
        except Exception as e:
            return None, f"❌ Error: {str(e)}"
    
    def export_video(self) -> Optional[str]:
        """
        Export the created video.
        
        Returns:
            Path to the video file for download
        """
        if self.output_video_path and Path(self.output_video_path).exists():
            return self.output_video_path
        return None
    
    def cleanup(self):
        """Clean up temporary files."""
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)


def create_ui() -> gr.Blocks:
    """Create and configure the Gradio UI."""
    
    builder = ReelBuilder()
    
    with gr.Blocks(
        title="Instagram Reel Builder",
        theme=gr.themes.Soft()
    ) as app:
        gr.Markdown(
            """
            # 📱 Instagram Reel Builder
            
            Create stunning Instagram reels from your photos with automatic 9:16 cropping and smooth transitions!
            
            ### How to use:
            1. Upload up to 30 JPEG or PNG images (order will be preserved)
            2. Set the duration for each photo (default: 4 seconds)
            3. Click "Create Video" to process
            4. Download your video with the "Export Video" button
            """
        )
        
        with gr.Row():
            with gr.Column(scale=2):
                # File upload
                file_upload = gr.File(
                    label="📤 Upload Images (JPEG or PNG)",
                    file_count="multiple",
                    file_types=[".jpg", ".jpeg", ".png"],
                    type="filepath"
                )
                
                # Duration slider
                duration_slider = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=4,
                    step=0.5,
                    label="⏱️ Duration per Image (seconds)",
                    info="How long each photo will be displayed"
                )
                
                # Transitions selection
                gr.Markdown("### 🎭 Transitions")
                transition_zoom_in = gr.Checkbox(
                    label="Zoom In",
                    value=True,
                    info="Slow zoom from 100% to 120%"
                )
                transition_zoom_out = gr.Checkbox(
                    label="Zoom Out",
                    value=True,
                    info="Slow zoom from 120% to 100%"
                )
                transition_fade_in = gr.Checkbox(
                    label="Fade In",
                    value=True,
                    info="Gradual appearance from black"
                )
                transition_fade_out = gr.Checkbox(
                    label="Fade Out",
                    value=True,
                    info="Gradual disappearance to black"
                )
                
                # Create button
                create_btn = gr.Button(
                    "🎬 Create Video",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=1):
                # Status output
                status_output = gr.Textbox(
                    label="📊 Status",
                    lines=10,
                    interactive=False,
                    placeholder="Upload images and click 'Create Video' to start..."
                )
                
                # Export button
                export_btn = gr.Button(
                    "💾 Export Video",
                    variant="secondary",
                    size="lg",
                    interactive=False
                )
        
        # Video preview
        video_output = gr.Video(
            label="🎥 Video Preview",
            interactive=False,
            height=480,
            width=270
        )
        
        # Download file
        download_file = gr.File(
            label="📥 Download Video",
            visible=False
        )
        
        # Event handlers
        def on_create(files, duration, zoom_in, zoom_out, fade_in, fade_out):
            if not files:
                return None, "❌ Please upload at least one image.", None, gr.Button(interactive=False)
            
            # Build list of selected transitions
            selected_transitions = []
            if zoom_in:
                selected_transitions.append("zoom_in")
            if zoom_out:
                selected_transitions.append("zoom_out")
            if fade_in:
                selected_transitions.append("fade_in")
            if fade_out:
                selected_transitions.append("fade_out")
            
            if not selected_transitions:
                return None, "❌ Please select at least one transition.", None, gr.Button(interactive=False)
            
            video_path, status = builder.process_and_create_video(files, duration, selected_transitions)
            # Enable export button after successful video creation
            if video_path:
                return video_path, status, video_path, gr.Button(interactive=True)
            return None, status, None, gr.Button(interactive=False)
        
        def on_export():
            video_path = builder.export_video()
            if video_path:
                return gr.File(value=video_path, visible=True)
            return gr.File(visible=False)
        
        create_btn.click(
            fn=on_create,
            inputs=[
                file_upload, 
                duration_slider, 
                transition_zoom_in, 
                transition_zoom_out, 
                transition_fade_in, 
                transition_fade_out
            ],
            outputs=[video_output, status_output, download_file, export_btn]
        )
        
        export_btn.click(
            fn=on_export,
            outputs=[download_file]
        )
        
        # Cleanup on app close
        app.unload(builder.cleanup)
    
    return app


def main():
    """Main entry point."""
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
