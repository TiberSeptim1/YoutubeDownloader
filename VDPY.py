import yt_dlp
import customtkinter as ck
import tkinter
import threading 



ck.set_appearance_mode("dark")
ck.set_default_color_theme("blue")

app = ck.CTk()
app.geometry("1280x720")
app.title("Vedant's YT Downloader")

status_label = ck.CTkLabel(app, text="")
status_label.pack(padx=10, pady=10)

progressbar = ck.CTkProgressBar(app, width=600)
progressbar.pack(padx=10, pady=10)
progressbar.set(0)

def progress_hook(d):
    if d['status']=='downloading':
        downloaded_bytes=d.get('downloaded_bytes', 0)
        total_bytes=d.get('total_bytes', 1)
        speed=d.get('speed',0)
        percentage=downloaded_bytes/total_bytes

        downloaded_mb = downloaded_bytes/(1024*1024)
        total_mb = total_bytes/(1024*1024)
        speed_mb = speed/(1024*1024)

        status_label.configure(text=f"{downloaded_mb:.2f}Mb/{total_mb:.2f}Mb at {speed_mb:.2f}Mbps", text_color="yellow")
        progressbar.set(percentage)
        progressbar.pack(padx=10, pady=10)

    elif d['status']=='finished':
        status_label.configure(text="Download finished")
        progressbar.set(1.0)


def download_video_thread(resolution):
    threading.Thread(target=download_video, args=(resolution,), daemon=True).start()

def download_video(resolution):
    url = entry.get()
    
    if not url:
        status_label.configure(text="Invalid URL!", text_color="red")
        return

    status_label.configure(text="Downloading Plz wait ...", text_color="yellow")
    progressbar.pack(padx=10, pady=10)
    progressbar.start()

    ydl_opts = {
        "format": f"bestvideo[height<={resolution}]+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": "%(title)s.%(ext)s","progress_hooks":[progress_hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.configure(text="Download Complete!", text_color="green")
    except Exception as e:
        status_label.configure(text="Download Failed!", text_color="red")
    
    progressbar.stop()
    progressbar.pack_forget()

tt = ck.CTkLabel(app, text="Paste a YT URL here")
tt.pack(padx=10, pady=10)

entry = ck.CTkEntry(app, width=500, corner_radius=32, border_color="#303F9F")
entry.pack(padx=12, pady=12)

button1 = ck.CTkButton(app, text="1080p", width=100, height=30, corner_radius=32, command=lambda: download_video_thread(1080), border_color="#303F9F")
button1.pack(padx=10, pady=10)

button2 = ck.CTkButton(app, text="720p", width=100, height=30, corner_radius=32, command=lambda: download_video_thread(720), border_color="#303F9F")
button2.pack(padx=10, pady=10)

button3 = ck.CTkButton(app, text="480p", width=100, height=30, corner_radius=32, command=lambda: download_video_thread(480), border_color="#303F9F")
button3.pack(padx=10, pady=10)

button4 = ck.CTkButton(app, text="144p", width=100, height=30, corner_radius=32, command=lambda: download_video_thread(144), border_color="#303F9F")
button4.pack(padx=10, pady=10)


app.mainloop()
