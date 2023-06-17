from gradio_client import Client

client = Client("https://sanchit-gandhi-whisper-jax.hf.space/")
result = client.predict(
    "https://www.youtube.com/watch?v=bre2eJsAdhM",  # str  in 'YouTube URL' Textbox component
    "transcribe",  # str  in 'Task' Radio component
    False,  # bool  in 'Return timestamps' Checkbox component
    api_name="/predict_2",
)
print(result)
