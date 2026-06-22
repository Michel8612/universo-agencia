import subprocess, os, textwrap

OUTPUT = r"D:\Proyectos claude\mundo-multimedia\proyectos\dia-del-padre.mp4"
FFMPEG = r"C:\ffmpeg\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

mensaje = "Gracias por tu amor incondicional\\ny por ser nuestra mayor inspiracion.\\nTu dedicacion y sabiduria\\nnos han ensenado a crecer y sonar grande."

cmd = [
    FFMPEG, "-y",
    "-f", "lavfi",
    "-i", "color=c=0x1a0a00:size=1080x1920:rate=30",
    "-f", "lavfi",
    "-i", "color=c=0xd4a017:size=1080x1920:rate=30",
    "-filter_complex",
    (
        # Borde dorado animado
        "[1]scale=1080:1920,crop=1080:1920[border];"
        "[0][border]overlay=0:0:enable='between(t,0,20)'[bg];"
        "[bg]"
        # Linea decorativa
        "drawbox=x=90:y=300:w=900:h=4:color=0xd4a017@1:t=fill,"
        "drawbox=x=90:y=1580:w=900:h=4:color=0xd4a017@1:t=fill,"
        # Titulo principal
        "drawtext=text='FELIZ DIA':fontsize=110:fontcolor=0xd4a017:x=(w-text_w)/2:y=360:"
        "fontfile='C\\:/Windows/Fonts/arialbd.ttf':alpha='if(lt(t,1),t,1)',"
        "drawtext=text='DEL PADRE':fontsize=110:fontcolor=white:x=(w-text_w)/2:y=490:"
        "fontfile='C\\:/Windows/Fonts/arialbd.ttf':alpha='if(lt(t,1),t,1)',"
        # Emoji corazon (texto)
        "drawtext=text='Con amor':fontsize=55:fontcolor=0xd4a017:x=(w-text_w)/2:y=700:"
        "fontfile='C\\:/Windows/Fonts/arial.ttf':alpha='if(lt(t,1.5),max(0,t-0.5),1)',"
        # Mensaje
        "drawtext=text='Gracias por tu amor incondicional':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=900:"
        "fontfile='C\\:/Windows/Fonts/arial.ttf':alpha='if(lt(t,2),max(0,t-1),1)',"
        "drawtext=text='y por ser nuestra mayor inspiracion.':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=970:"
        "fontfile='C\\:/Windows/Fonts/arial.ttf':alpha='if(lt(t,2),max(0,t-1),1)',"
        "drawtext=text='Tu dedicacion y sabiduria':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=1060:"
        "fontfile='C\\:/Windows/Fonts/arial.ttf':alpha='if(lt(t,2.5),max(0,t-1.5),1)',"
        "drawtext=text='nos han ensenado a crecer y sonar grande.':fontsize=46:fontcolor=white:x=(w-text_w)/2:y=1130:"
        "fontfile='C\\:/Windows/Fonts/arial.ttf':alpha='if(lt(t,2.5),max(0,t-1.5),1)',"
        # Firma agencia
        "drawtext=text='Universo Agencia IA':fontsize=42:fontcolor=0xd4a017:x=(w-text_w)/2:y=1650:"
        "fontfile='C\\:/Windows/Fonts/ariali.ttf':alpha='if(lt(t,3),max(0,t-2),1)',"
        # Fade in/out global
        "fade=t=in:st=0:d=1,fade=t=out:st=18:d=2"
    ),
    "-t", "20",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "23",
    "-pix_fmt", "yuv420p",
    OUTPUT
]

print("Generando video Dia del Padre...")
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    size = os.path.getsize(OUTPUT) / 1024 / 1024
    print(f"VIDEO LISTO: {OUTPUT}")
    print(f"Tamano: {size:.1f} MB")
else:
    print("ERROR:", result.stderr[-500:])
