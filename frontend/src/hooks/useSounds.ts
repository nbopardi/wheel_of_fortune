import { useEffect, useRef, useState } from 'react';

interface SoundMap {
  theme_song: HTMLAudioElement;
  speedup: HTMLAudioElement;
  bankrupt: HTMLAudioElement;
  buzzer: HTMLAudioElement;
  choose_letters: HTMLAudioElement;
  ding: HTMLAudioElement;
  puzzle_reveal: HTMLAudioElement;
  puzzle_solve: HTMLAudioElement;
  bonus_wheel_music: HTMLAudioElement;
}

export const useSounds = () => {
  const soundsRef = useRef<SoundMap | null>(null);
  const [soundsLoaded, setSoundsLoaded] = useState(false);
  const currentLoopingSoundRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    // Initialize all sound objects
    const sounds: SoundMap = {
      theme_song: new Audio('/sound_effects/theme_song.mp3'),
      speedup: new Audio('/sound_effects/speedup.mp3'),
      bankrupt: new Audio('/sound_effects/bankrupt.mp3'),
      buzzer: new Audio('/sound_effects/buzzer.mp3'),
      choose_letters: new Audio('/sound_effects/choose_letters.mp3'),
      ding: new Audio('/sound_effects/ding.mp3'),
      puzzle_reveal: new Audio('/sound_effects/puzzle_reveal.mp3'),
      puzzle_solve: new Audio('/sound_effects/puzzle_solve.mp3'),
      bonus_wheel_music: new Audio('/sound_effects/bonus_wheel_music.mp3'),
    };

    // Set looping for specific sounds
    sounds.theme_song.loop = true;
    sounds.speedup.loop = true;
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
      soundsRef.current.speedup,
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

  const playSound = (soundName: keyof SoundMap, options?: { loop?: boolean; stopOthers?: boolean; onEnded?: () => void }) => {
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

    // Set up onended callback if provided
    if (options?.onEnded) {
      sound.onended = options.onEnded;
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