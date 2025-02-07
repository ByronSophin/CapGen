import os
import json
import logging
import datetime
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import whisper
import srt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Set up logging
logger = logging.getLogger(__name__)

# Load the Whisper model once (to avoid reloading it on every request)
model = whisper.load_model("large-v2")

def transcribe_audio(video_path):
    """
    Transcribe audio from a video file using Whisper.
    """
    try:
        logger.info(f"Starting transcription for video: {video_path}")
        video = VideoFileClip(video_path)
        audio_path = os.path.join(settings.TEMP_DIR, "temp_audio.wav")
        logger.info(f"Extracting audio to: {audio_path}")
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        logger.info("Transcribing audio...")
        result = model.transcribe(audio_path, task="translate", language="en")
        logger.info("Transcription completed successfully.")
        return result
    except Exception as e:
        logger.error(f"Error during transcription: {e}", exc_info=True)
        raise

def generate_srt(transcription, video_name):
    """
    Generate an SRT file from the transcription.
    """
    try:
        logger.info(f"Generating SRT file for video: {video_name}")
        subtitles = []
        for i, segment in enumerate(transcription['segments']):
            start_time = datetime.timedelta(seconds=segment['start'])
            end_time = datetime.timedelta(seconds=segment['end'])
            subtitles.append(srt.Subtitle(index=i, start=start_time, end=end_time, content=segment['text']))
        
        srt_content = srt.compose(subtitles)
        srt_path = os.path.join(settings.TEMP_DIR, f"{video_name}_subtitles.srt")
        logger.info(f"Saving SRT file to: {srt_path}")
        with open(srt_path, "w", encoding='utf-8') as f:
            f.write(srt_content)
        logger.info("SRT file generated successfully.")
        return srt_path
    except Exception as e:
        logger.error(f"Error generating SRT file: {e}", exc_info=True)
        raise

def overlay_subtitles(video_path, srt_path, video_name):
    """
    Overlay subtitles onto the video.
    """
    try:
        logger.info(f"Overlaying subtitles for video: {video_name}")
        clip = VideoFileClip(video_path)
        subtitle_clips = []
        with open(srt_path, 'r', encoding='utf-8') as f:
            subtitles = list(srt.parse(f.read()))
        
        for subtitle in subtitles:
            start_time = subtitle.start.total_seconds()
            end_time = subtitle.end.total_seconds()
            text = subtitle.content
            txt_clip = TextClip(text, fontsize=30, color='white', align='center', method='caption', size=(clip.size[0], clip.size[1]//10))
            txt_clip = txt_clip.set_start(start_time).set_duration(end_time - start_time).set_position(('center', 'top'))
            subtitle_clips.append(txt_clip)
            
        video = CompositeVideoClip([clip] + subtitle_clips)
        output_path = os.path.join(settings.TEMP_DIR, f"{video_name}_sub.mp4")
        logger.info(f"Saving captioned video to: {output_path}")
        video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        logger.info("Subtitles overlayed successfully.")
        return output_path
    except Exception as e:
        logger.error(f"Error overlaying subtitles: {e}", exc_info=True)
        raise

@csrf_exempt
def transcribe_and_overlay(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            logger.info("Received request to transcribe and overlay video.")
            video_file = request.FILES['file']
            logger.info(f"Processing file: {video_file.name}")

            # Save the uploaded file to the temp directory
            video_path = default_storage.save(os.path.join('temp', video_file.name), ContentFile(video_file.read()))
            logger.info(f"Video saved to: {video_path}")

            # Get the absolute path of the saved file
            absolute_video_path = default_storage.path(video_path)
            logger.info(f"Absolute video path: {absolute_video_path}")

            filename = os.path.splitext(video_file.name)[0]

            # Transcribe audio
            logger.info("Starting transcription...")
            transcription = transcribe_audio(absolute_video_path)  # Use absolute path
            logger.info("Transcription completed.")

            # Generate SRT
            logger.info("Generating SRT file...")
            srt_path = generate_srt(transcription, filename)
            logger.info(f"SRT file generated at: {srt_path}")

            # Overlay subtitles
            logger.info("Overlaying subtitles on video...")
            output_path = overlay_subtitles(absolute_video_path, srt_path, filename)  # Use absolute path
            logger.info(f"Captioned video saved at: {output_path}")

            # Return the path to the processed video
            return JsonResponse({'output_path': output_path}, status=200)
        except Exception as e:
            logger.error(f'Error processing video: {e}', exc_info=True)
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_file_url(request):
    """
    Serve the processed video file for download.
    """
    if request.method == 'POST':
        try:
            logger.info("Received request to download file.")
            body = json.loads(request.body.decode('utf-8'))
            file_name = body.get('fileName')
            
            if not file_name:
                logger.error("File name not provided in request.")
                return JsonResponse({'error': 'File name not provided'}, status=400)

            file_path = os.path.join(settings.TEMP_DIR, file_name)
            logger.info(f"Looking for file at: {file_path}")

            if os.path.isfile(file_path):
                logger.info(f"File found. Serving file: {file_name}")
                with open(file_path, 'rb') as f:
                    response = FileResponse(f, as_attachment=True, filename=file_name)
                    response['Content-Type'] = 'application/octet-stream'
                    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                    return response
            else:
                logger.error(f"File not found: {file_name}")
                return JsonResponse({'error': 'File does not exist'}, status=404)
        except Exception as e:
            logger.error(f'Error serving file: {e}', exc_info=True)
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=405)