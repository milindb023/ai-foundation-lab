import { useState, useRef } from "react";
import { textToSpeech } from "../lib/api";

export function useTextToSpeech() {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const speak = async (text: string) => {
    try {
      setIsPlaying(true);
      
      // Request synthesized audio binary stream from the API
      const audioBlob = await textToSpeech(text);
      const url = URL.createObjectURL(audioBlob);

      // Stop any audio actively playing
      if (audioRef.current) {
        audioRef.current.pause();
      }

      const audio = new Audio(url);
      audio.onended = () => {
        setIsPlaying(false);
      };
      audio.onerror = () => {
        setIsPlaying(false);
      };

      audioRef.current = audio;
      await audio.play();
    } catch (err) {
      console.error("Text-to-speech audio playback failed:", err);
      setIsPlaying(false);
    }
  };

  const stop = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  return {
    speak,
    stop,
    isPlaying
  };
}
