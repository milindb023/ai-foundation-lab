import { useState, useEffect, useRef } from "react";

export function useSpeechRecognition() {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      
      if (SpeechRecognition) {
        const rec = new SpeechRecognition();
        rec.continuous = false;
        rec.interimResults = false;
        rec.lang = "en-US";

        rec.onstart = () => {
          setIsListening(true);
        };
        rec.onend = () => {
          setIsListening(false);
        };
        rec.onresult = (event: any) => {
          const text = event.results[0][0].transcript;
          setTranscript(text);
        };

        recognitionRef.current = rec;
      }
    }
  }, []);

  const startListening = () => {
    if (recognitionRef.current) {
      setTranscript("");
      try {
        recognitionRef.current.start();
      } catch (err) {
        console.error("Speech recognition start failed:", err);
      }
    } else {
      console.warn("Web Speech API is not supported in this browser.");
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  return {
    isListening,
    transcript,
    startListening,
    stopListening,
    isSupported: !!recognitionRef.current
  };
}
