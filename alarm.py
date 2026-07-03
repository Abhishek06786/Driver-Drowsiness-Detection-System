import pygame

pygame.mixer.init()

pygame.mixer.music.load("alarm.wav")

alarm_playing = False

def play_alarm():
    global alarm_playing

    if not alarm_playing:
        pygame.mixer.music.play(-1)
        alarm_playing = True

def stop_alarm():
    global alarm_playing

    if alarm_playing:
        pygame.mixer.music.stop()
        alarm_playing = False


if __name__ == "__main__":
    print("Testing Alarm...")
    play_alarm()
    input("Press Enter to stop...")
    stop_alarm()