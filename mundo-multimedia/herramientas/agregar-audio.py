import pyttsx3, subprocess, os

FFMPEG = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"
VIDEO_IN = r"D:\Proyectos claude\mundo-multimedia\proyectos\dia-del-padre.mp4"
AUDIO_TMP = r"D:\Proyectos claude\mundo-multimedia\proyectos\audio-tmp.wav"
VIDEO_OUT = r"D:\Proyectos claude\mundo-multimedia\proyectos\dia-del-padre-con-audio.mp4"

texto = (
    "Feliz Día del Padre. "
    "Gracias por tu amor incondicional y por ser nuestra mayor inspiración. "
    "Tu dedicación y sabiduría nos han enseñado a crecer y soñar grande. "
    "Con mucho cariño, de parte de todos los que te amamos."
)

print("Generando voz...")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Buscar voz en español
for v in voices:
    if 'spanish' in v.name.lower() or 'es' in v.id.lower():
        engine.setProperty('voice', v.id)
        print(f"Voz: {v.name}")
        break
engine.setProperty('rate', 145)
engine.setProperty('volume', 0.95)
engine.save_to_file(texto, AUDIO_TMP)
engine.runAndWait()

print("Combinando vídeo + audio...")
cmd = [
    FFMPEG, "-y",
    "-i", VIDEO_IN,
    "-i", AUDIO_TMP,
    "-c:v", "copy",
    "-c:a", "aac",
    "-shortest",
    VIDEO_OUT
]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode == 0:
    print(f"LISTO: {VIDEO_OUT}")
    print(f"Tamaño: {os.path.getsize(VIDEO_OUT)/1024/1024:.1f} MB")
else:
    print("ERROR:", r.stderr[-300:])

os.remove(AUDIO_TMP)
