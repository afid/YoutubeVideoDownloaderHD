import customtkinter as ctk
from pytubefix import YouTube
import os
import subprocess
import re
import threading
from tkinter import messagebox
import time

class YouTubeDownloader:
    def __init__(self):
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self.root.title("YouTube Video Downloader HD")
        self.root.geometry("600x580")
        self.root.resizable(False, False)
        
        # Variables
        self.download_in_progress = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Titre
        title_label = ctk.CTkLabel(
            self.root,
            text="YouTube Video Downloader HD",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Frame pour l'URL
        url_frame = ctk.CTkFrame(self.root)
        url_frame.pack(pady=10, padx=20, fill="x")
        
        # Label et entrée pour l'URL
        url_label = ctk.CTkLabel(url_frame, text="URL YouTube:")
        url_label.pack(pady=(10, 5))
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="Collez l'URL de la vidéo YouTube ici...",
            width=500
        )
        self.url_entry.pack(pady=(0, 10), padx=10)
        
        # Bouton de téléchargement
        self.download_button = ctk.CTkButton(
            self.root,
            text="Télécharger",
            command=self.start_download,
            width=200,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.download_button.pack(pady=20)
        
        # Frame pour les barres de progression
        progress_frame = ctk.CTkFrame(self.root)
        progress_frame.pack(pady=10, padx=20, fill="x")
        
        # Barre de progression vidéo
        self.video_label = ctk.CTkLabel(progress_frame, text="Téléchargement vidéo: 0%")
        self.video_label.pack(pady=(10, 5))
        
        self.video_progress = ctk.CTkProgressBar(progress_frame, width=500)
        self.video_progress.pack(pady=(0, 10), padx=10)
        self.video_progress.set(0)
        
        # Barre de progression audio
        self.audio_label = ctk.CTkLabel(progress_frame, text="Téléchargement audio: 0%")
        self.audio_label.pack(pady=(5, 5))
        
        self.audio_progress = ctk.CTkProgressBar(progress_frame, width=500)
        self.audio_progress.pack(pady=(0, 10), padx=10)
        self.audio_progress.set(0)
        
        # Barre de progression combinaison
        self.combine_label = ctk.CTkLabel(progress_frame, text="Combinaison: 0%")
        self.combine_label.pack(pady=(5, 5))
        
        self.combine_progress = ctk.CTkProgressBar(progress_frame, width=500)
        self.combine_progress.pack(pady=(0, 10), padx=10)
        self.combine_progress.set(0)
        
        # Label de statut
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Prêt à télécharger",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=10)
        
    def sanitize_filename(self, filename):
        """Nettoie le nom de fichier pour éviter les caractères problématiques"""
        return re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    def update_video_progress(self, stream, chunk, bytes_remaining):
        """Callback pour la progression du téléchargement vidéo"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size
        
        # Mise à jour de l'interface dans le thread principal
        self.root.after(0, self._update_video_ui, percentage)
    
    def update_audio_progress(self, stream, chunk, bytes_remaining):
        """Callback pour la progression du téléchargement audio"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size
        
        # Mise à jour de l'interface dans le thread principal
        self.root.after(0, self._update_audio_ui, percentage)
    
    def _update_video_ui(self, percentage):
        """Met à jour l'interface pour la progression vidéo"""
        self.video_progress.set(percentage)
        self.video_label.configure(text=f"Téléchargement vidéo: {percentage*100:.1f}%")
    
    def _update_audio_ui(self, percentage):
        """Met à jour l'interface pour la progression audio"""
        self.audio_progress.set(percentage)
        self.audio_label.configure(text=f"Téléchargement audio: {percentage*100:.1f}%")
    
    def _update_combine_ui(self, percentage):
        """Met à jour l'interface pour la progression de combinaison"""
        self.combine_progress.set(percentage)
        self.combine_label.configure(text=f"Combinaison: {percentage*100:.1f}%")
    
    def _update_status(self, message):
        """Met à jour le message de statut"""
        self.status_label.configure(text=message)
    
    def reset_progress(self):
        """Remet à zéro toutes les barres de progression"""
        self.video_progress.set(0)
        self.audio_progress.set(0)
        self.combine_progress.set(0)
        self.video_label.configure(text="Téléchargement vidéo: 0%")
        self.audio_label.configure(text="Téléchargement audio: 0%")
        self.combine_label.configure(text="Combinaison: 0%")
    
    def simulate_ffmpeg_progress(self, duration=5):
        """Simule la progression de ffmpeg"""
        steps = 20
        for i in range(steps + 1):
            percentage = i / steps
            self.root.after(0, self._update_combine_ui, percentage)
            time.sleep(duration / steps)
    
    def start_download(self):
        """Démarre le téléchargement dans un thread séparé"""
        if self.download_in_progress:
            return
            
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube valide")
            return
        
        self.download_in_progress = True
        self.download_button.configure(text="Téléchargement en cours...", state="disabled")
        self.reset_progress()
        
        # Lancer le téléchargement dans un thread séparé
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_video(self, url):
        """Fonction principale de téléchargement"""
        try:
            # Créer le dossier Downloads s'il n'existe pas
            download_folder = "Downloads"
            os.makedirs(download_folder, exist_ok=True)
            
            self.root.after(0, self._update_status, "Connexion à YouTube...")
            
            # Créer l'objet YouTube pour la vidéo
            yt_video = YouTube(url, on_progress_callback=self.update_video_progress)
            
            self.root.after(0, self._update_status, f"Vidéo trouvée: {yt_video.title}")
            
            # Nettoyer le titre
            clean_title = self.sanitize_filename(yt_video.title)
            
            # Obtenir d'abord les flux adaptatifs (non-progressifs) avec la plus haute résolution
            # Les flux adaptatifs offrent généralement une meilleure qualité
            video_stream = yt_video.streams.filter(progressive=False, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
            
            # Si aucun flux adaptatif trouvé, prendre le flux progressif avec la plus haute résolution
            if video_stream is None:
                video_stream = yt_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            
            if video_stream is None:
                raise Exception("Aucun flux vidéo trouvé")
            
            self.root.after(0, self._update_status, f"Résolution sélectionnée: {video_stream.resolution}")
            
            # Vérifier si le flux est adaptatif (non-progressif)
            if not video_stream.is_progressive:
                self.root.after(0, self._update_status, "Téléchargement de la vidéo...")
                
                # Télécharger la vidéo dans le dossier Downloads
                video_filename = f"{clean_title}_video.mp4"
                video_path = video_stream.download(output_path=download_folder, filename=video_filename)
                
                self.root.after(0, self._update_status, "Téléchargement de l'audio...")
                
                # Créer un nouvel objet YouTube pour l'audio
                yt_audio = YouTube(url, on_progress_callback=self.update_audio_progress)
                
                # Obtenir le flux audio avec la meilleure qualité (le plus haut bitrate)
                audio_stream = yt_audio.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
                
                # Si aucun flux audio mp4 trouvé, prendre le meilleur disponible
                if audio_stream is None:
                    audio_stream = yt_audio.streams.filter(only_audio=True).order_by('abr').desc().first()
                
                if not audio_stream:
                    raise Exception("Aucun flux audio trouvé")
                
                # Télécharger l'audio dans le dossier Downloads
                audio_filename = f"{clean_title}_audio.mp4"
                audio_path = audio_stream.download(output_path=download_folder, filename=audio_filename)
                
                self.root.after(0, self._update_status, "Combinaison vidéo et audio...")
                
                # Combiner avec ffmpeg dans le dossier Downloads
                output_path = os.path.join(download_folder, f"{clean_title}.mp4")
                
                # Simuler la progression de ffmpeg
                ffmpeg_thread = threading.Thread(target=self.simulate_ffmpeg_progress)
                ffmpeg_thread.start()
                
                subprocess.run([
                    'ffmpeg',
                    '-i', video_path,
                    '-i', audio_path,
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-strict', 'experimental',
                    '-y',
                    output_path
                ], check=True, capture_output=True)
                
                ffmpeg_thread.join()
                
                # Nettoyer les fichiers temporaires
                if os.path.exists(video_path):
                    os.remove(video_path)
                # Conserver le fichier audio (ne pas supprimer audio_path)
                
                self.root.after(0, self._update_status, f"Téléchargement terminé: {output_path}")
                
            else:
                # Flux progressif - déjà la meilleure qualité disponible en progressif
                self.root.after(0, self._update_status, f"Téléchargement en cours... Résolution: {video_stream.resolution}")
                output_filename = f"{clean_title}.mp4"
                output_path = video_stream.download(output_path=download_folder, filename=output_filename)
                
                # Simuler la progression audio et combinaison pour l'interface
                self.root.after(0, self._update_audio_ui, 1.0)
                self.root.after(0, self._update_combine_ui, 1.0)
                
                self.root.after(0, self._update_status, f"Téléchargement terminé: {output_path}")
            
            # Afficher le message de succès
            self.root.after(0, lambda: messagebox.showinfo("Succès", f"Téléchargement terminé avec succès!\nFichiers sauvegardés dans: {download_folder}"))
            
        except subprocess.CalledProcessError:
            error_msg = "Erreur lors de la combinaison. Assurez-vous que ffmpeg est installé."
            self.root.after(0, lambda: messagebox.showerror("Erreur", error_msg))
            self.root.after(0, self._update_status, "Erreur lors de la combinaison")
            
        except Exception as e:
            error_msg = f"Erreur: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Erreur", error_msg))
            self.root.after(0, self._update_status, f"Erreur: {str(e)}")
            
        finally:
            # Réactiver le bouton
            self.download_in_progress = False
            self.root.after(0, lambda: self.download_button.configure(text="Télécharger", state="normal"))
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.run()