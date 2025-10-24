import customtkinter as ctk
from gtts import gTTS
import pygame
import tempfile
import os
import threading

# Initialiser l'apparence
ctk.set_appearance_mode("dark")  # "light" ou "dark"
ctk.set_default_color_theme("blue")

def text_to_speech(text, lang='fr'):
    """Convertit le texte en fichier audio temporaire."""
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_file.close()
    tts.save(temp_file.name)
    return temp_file.name

def play_audio(file_path, play_button):
    """Lit le fichier audio via pygame."""
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    play_button.configure(state="disabled", text="🎧 Lecture en cours...")

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    play_button.configure(state="normal", text="▶️ Lire le texte")

def on_convert_click(entry, play_button):
    """Action quand on clique sur le bouton Convertir."""
    text = entry.get("1.0", "end").strip()
    if not text:
        return

    # Thread pour éviter le blocage de l'UI
    def process():
        try:
            file_path = text_to_speech(text)
            play_audio(file_path, play_button)
            os.remove(file_path)
        except Exception as e:
            print("Erreur :", e)

    threading.Thread(target=process, daemon=True).start()

def main():
    app = ctk.CTk()
    app.title("🎙️ Text-to-Speech App (gTTS)")
    app.geometry("900x500")

    title_label = ctk.CTkLabel(app, text="Text-to-Speech (Google TTS)", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    entry = ctk.CTkTextbox(app, width=400, height=150)
    entry.insert("1.0", "Écris ton texte ici...")
    entry.pack(pady=10)

    play_button = ctk.CTkButton(app, text="▶️ Lire le texte", command=lambda: on_convert_click(entry, play_button))
    play_button.pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    main()
