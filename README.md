# YouTube Video Downloader HD

Un téléchargeur de vidéos YouTube moderne avec interface graphique, capable de télécharger des vidéos en haute définition (jusqu'à 4K/8K) avec suivi en temps réel du téléchargement.

![Interface](https://img.shields.io/badge/Interface-CustomTkinter-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Fonctionnalités

- **Interface graphique moderne** avec CustomTkinter (thème sombre)
- **Téléchargement haute définition** jusqu'à 4K/8K selon la disponibilité
- **Barres de progression en temps réel** pour chaque étape :
  - Téléchargement vidéo
  - Téléchargement audio
  - Combinaison des fichiers
- **Gestion automatique des flux adaptatifs** pour la meilleure qualité
- **Conservation du fichier audio** séparé après téléchargement
- **Nettoyage automatique** des fichiers temporaires
- **Gestion d'erreurs complète** avec messages informatifs
- **Threading** pour une interface responsive

## 🖼️ Aperçu

L'application offre une interface intuitive avec :
- Zone de saisie pour l'URL YouTube
- Bouton de téléchargement avec état en temps réel
- Trois barres de progression distinctes
- Messages de statut détaillés
- Gestion des erreurs via boîtes de dialogue

## 🛠️ Installation

### Prérequis

- Python 3.7 ou supérieur
- FFmpeg installé et accessible dans le PATH

### Installation de FFmpeg

**Windows :**
1. Téléchargez FFmpeg depuis [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extrayez l'archive et ajoutez le dossier `bin` au PATH système

**macOS :**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian) :**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Installation des dépendances Python

```bash
pip install customtkinter pytubefix
```

## 🚀 Utilisation

1. **Lancez l'application :**
   ```bash
   python youtube_downloader.py
   ```

2. **Collez l'URL YouTube** dans le champ prévu

3. **Cliquez sur "Télécharger"**

4. **Suivez la progression** avec les barres dédiées :
   - Barre vidéo : Téléchargement du flux vidéo haute définition
   - Barre audio : Téléchargement du flux audio haute qualité
   - Barre combinaison : Fusion des fichiers avec FFmpeg

5. **Récupérez vos fichiers** :
   - `[titre].mp4` : Vidéo finale combinée
   - `[titre]_audio.mp4` : Fichier audio séparé (conservé)

## 📁 Structure des fichiers

```
youtube-downloader-hd/
├── Extractor.py            # Application principale
├── README.md               # Documentation
└── requirements.txt        # Dépendances (optionnel)
```

## ⚙️ Fonctionnement technique

### Sélection de la qualité
1. **Flux adaptatifs prioritaires** : Recherche d'abord les flux non-progressifs (vidéo seule) pour la plus haute résolution
2. **Fallback intelligent** : Si aucun flux adaptatif, utilise les flux progressifs
3. **Audio haute qualité** : Sélection automatique du meilleur bitrate disponible

### Gestion des flux
- **Flux adaptatifs** : Vidéo et audio séparés, permet 1080p+ (jusqu'à 8K)
- **Flux progressifs** : Vidéo et audio combinés, limités à 720p généralement
- **Combinaison FFmpeg** : Fusion lossless des flux adaptatifs

### Interface utilisateur
- **Threading** : Téléchargement en arrière-plan sans bloquer l'interface
- **Callbacks** : Mise à jour en temps réel des barres de progression
- **Gestion d'état** : Désactivation des contrôles pendant le téléchargement

## 🔧 Configuration avancée

### Personnalisation des formats
Modifiez les filtres dans la fonction `download_video()` :

```python
# Pour forcer un format spécifique
video_stream = yt_video.streams.filter(
    progressive=False, 
    file_extension='webm',  # ou 'mp4'
    only_video=True
).order_by('resolution').desc().first()
```

### Dossier de téléchargement
Ajoutez un dossier de destination :

```python
# Dans la fonction download_video()
download_path = "Downloads"
os.makedirs(download_path, exist_ok=True)
video_path = video_stream.download(output_path=download_path, filename=video_filename)
```

## ⚠️ Limitations et notes

- **Respect du copyright** : Utilisez uniquement pour du contenu libre de droits ou dont vous possédez les droits
- **Dépendance FFmpeg** : Requis pour la combinaison des flux haute définition
- **Taille des fichiers** : Les vidéos 4K+ peuvent être très volumineuses
- **Vitesse réseau** : Le téléchargement dépend de votre connexion internet

## 🐛 Résolution des problèmes

### Erreur "FFmpeg not found"
- Vérifiez que FFmpeg est installé et dans le PATH
- Testez avec `ffmpeg -version` dans le terminal

### Échec du téléchargement
- Vérifiez l'URL YouTube
- Certaines vidéos peuvent être protégées ou géo-bloquées
- Essayez avec une autre vidéo pour tester

### Interface qui ne répond pas
- Le téléchargement s'effectue en arrière-plan
- Attendez la fin du processus ou redémarrez l'application

## 🤝 Contribution

Les contributions sont bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- [pytubefix](https://github.com/JuanBindez/pytubefix) - Bibliothèque de téléchargement YouTube
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Interface graphique moderne
- [FFmpeg](https://ffmpeg.org/) - Traitement vidéo et audio

## 📞 Support

Si vous rencontrez des problèmes ou avez des questions :
- Ouvrez une [issue](https://github.com/votre-username/youtube-downloader-hd/issues)
- Consultez la documentation des dépendances
- Vérifiez les prérequis système

---

⭐ **N'oubliez pas de mettre une étoile au projet si vous le trouvez utile !**
