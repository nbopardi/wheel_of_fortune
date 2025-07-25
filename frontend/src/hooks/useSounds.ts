import { useEffect, useRef, useState } from 'react';

interface SoundMap {
  theme_song: HTMLAudioElement;
  toss_up: HTMLAudioElement;
  bankrupt: HTMLAudioElement;
  buzzer: HTMLAudioElement;
  choose_letters: HTMLAudioElement;
  ding: HTMLAudioElement;
  puzzle_reveal: HTMLAudioElement;
  puzzle_solve: HTMLAudioElement;
}

export const useSounds = () => {
  const soundsRef = useRef<SoundMap | null>(null);
  const [soundsLoaded, setSoundsLoaded] = useState(false);
  const currentLoopingSoundRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    // Initialize all sound objects
    const sounds: SoundMap = {
      theme_song: new Audio('/sound_effects/theme_song.mp3'),
      toss_up: new Audio('/sound_effects/toss_up.mp3'),
      bankrupt: new Audio('/sound_effects/bankrupt.mp3'),
      buzzer: new Audio('/sound_effects/buzzer.mp3'),
      choose_letters: new Audio('/sound_effects/choose_letters.mp3'),
      ding: new Audio('/sound_effects/ding.mp3'),
      puzzle_reveal: new Audio('/sound_effects/puzzle_reveal.mp3'),
      puzzle_solve: new Audio('/sound_effects/puzzle_solve.mp3'),
    };

    // Set looping for specific sounds
    sounds.theme_song.loop = true;
    sounds.toss_up.loop = true;
    sounds.choose_letters.loop = true;

    // Set volume levels (adjust as needed)
    Object.values(sounds).forEach(sound => {
      sound.volume = 0.7;
    });

    soundsRef.current = sounds;
    setSoundsLoaded(true);

    // Cleanup function
    return () => {
      Object.values(sounds).forEach(sound => {
        sound.pause();
        sound.currentTime = 0;
      });
    };
  }, []);

  const stopAllSounds = () => {
    if (!soundsRef.current) return;
    
    Object.values(soundsRef.current).forEach(sound => {
      sound.pause();
      sound.currentTime = 0;
    });
    currentLoopingSoundRef.current = null;
  };

  const stopLoopingSounds = () => {
    if (!soundsRef.current) return;
    
    // Stop only looping sounds
    const loopingSounds = [
      soundsRef.current.theme_song,
      soundsRef.current.toss_up,
      soundsRef.current.choose_letters
    ];
    
    loopingSounds.forEach(sound => {
      sound.pause();
      sound.currentTime = 0;
    });
    
    if (currentLoopingSoundRef.current && loopingSounds.includes(currentLoopingSoundRef.current)) {
      currentLoopingSoundRef.current = null;
    }
  };

  const playSound = (soundName: keyof SoundMap, options?: { loop?: boolean; stopOthers?: boolean }) => {
    if (!soundsRef.current || !soundsLoaded) return;

    const sound = soundsRef.current[soundName];
    if (!sound) return;

    // If this sound is already playing and not paused, don't restart it
    if (!sound.paused && sound.currentTime > 0 && currentLoopingSoundRef.current === sound) {
      return;
    }

    // Stop other sounds if requested
    if (options?.stopOthers) {
      stopAllSounds();
    }

    // Reset and play the sound
    sound.currentTime = 0;
    sound.play().catch(error => {
      console.warn(`Failed to play sound ${soundName}:`, error);
    });

    // Track looping sounds
    if (sound.loop || options?.loop) {
      currentLoopingSoundRef.current = sound;
    }
  };

  const playDing = (count: number) => {
    if (!soundsRef.current || !soundsLoaded || count <= 0) return;

    const sound = soundsRef.current.ding;
    let playCount = 0;

    const playNext = () => {
      if (playCount < count) {
        sound.currentTime = 0;
        sound.play().catch(error => {
          console.warn('Failed to play ding sound:', error);
        });
        playCount++;
        
        // Wait for the sound to finish before playing the next one
        sound.onended = () => {
          if (playCount < count) {
            setTimeout(playNext, 200); // Small delay between dings
          }
        };
      }
    };

    playNext();
  };

  return {
    playSound,
    playDing,
    stopAllSounds,
    stopLoopingSounds,
    soundsLoaded,
  };
}; 