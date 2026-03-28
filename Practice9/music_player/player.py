# player.py
# Music player logic — playlist management and pygame.mixer control

import os
import pygame


class MusicPlayer:
    def __init__(self, music_dir: str = "music"):
        pygame.mixer.init()
        self.music_dir    = music_dir
        self.playlist     = self._load_playlist()
        self.current_idx  = 0
        self.is_playing   = False

    # ── Playlist ─────────────────────────────────────────────────────────────

    def _load_playlist(self):
        """Scan music_dir for .mp3 and .wav files."""
        supported = (".mp3", ".wav", ".ogg")
        if not os.path.isdir(self.music_dir):
            return []
        files = sorted(
            f for f in os.listdir(self.music_dir)
            if f.lower().endswith(supported)
        )
        return [os.path.join(self.music_dir, f) for f in files]

    def reload_playlist(self):
        self.playlist = self._load_playlist()

    # ── Controls ─────────────────────────────────────────────────────────────

    def play(self):
        if not self.playlist:
            return
        track = self.playlist[self.current_idx]
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.playlist:
            return
        self.current_idx = (self.current_idx + 1) % len(self.playlist)
        self.play()

    def prev_track(self):
        if not self.playlist:
            return
        self.current_idx = (self.current_idx - 1) % len(self.playlist)
        self.play()

    def toggle_pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True

    # ── Info ─────────────────────────────────────────────────────────────────

    def current_track_name(self) -> str:
        if not self.playlist:
            return "No tracks found"
        return os.path.basename(self.playlist[self.current_idx])

    def status(self) -> str:
        if not self.playlist:
            return "Empty playlist"
        state = "▶ Playing" if self.is_playing else "⏹ Stopped"
        return f"{state}  [{self.current_idx + 1}/{len(self.playlist)}]"

    def position_sec(self) -> float:
        return pygame.mixer.music.get_pos() / 1000
