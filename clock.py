#Importation of library to manage the date, the time, a thread and a sound for the alarm
import datetime
import time
import threading
import pygame
#Flag for the pause function
pause_event = threading.Event()  
pause_event.set()
#Base variable of the time
current_time = datetime.datetime.now()
#Base variable for the time mode
mode="%H:%M:%S"
#Function to get the time
def get_current_time():
    global current_time
    return current_time.strftime(mode)
#Function to set an alarm, and ring with a sound when its time
def alarm(ring):
    while True:
        current_time_str = get_current_time()
        if current_time_str == ring:
            pygame.mixer.init()
            alarm_sound = pygame.mixer.Sound("Alarm_sound.wav")
            alarm_sound.play()
            print("\nDing! Your alarm is ringing!")
            break
        time.sleep(1)  
#Function to show the clock and go back to the menu with Ctrl+C
def clock():
    try:
        while True:
            print(f"\rCurrent time: {get_current_time()}", end="")
            time.sleep(1)  
    except KeyboardInterrupt:
        print("\nClock closed, back to menu.")
#Function to allow the user to change the time as he please
def change_time():
    global current_time
    new_time_str = input("Enter the new time (HH:MM:SS): ")
    try:
        new_time = datetime.datetime.strptime(new_time_str, mode)
        current_time = new_time
        print(f"Time changed to {get_current_time()}")
    except ValueError:
        print("Invalid time format. Please enter in HH:MM:SS format.")
#Function to update the changed time, adding a second every second
def update_time():
    global current_time
    while True:
        pause_event.wait()
        time.sleep(1)
        current_time += datetime.timedelta(seconds=1)
#Function to reset changed time to default time
def reset_time():
    global current_time
    current_time = datetime.datetime.now()
    print("Time changed to default.")
#Function to pause/unpaused the clock
def pause():
    global pause_event
    if pause_event.is_set():  
        print(f"\nTime paused: {get_current_time()}")
        pause_event.clear()  
    else:
        print("\nTime unpaused.")
        pause_event.set()
#Function to change the time mode to AM/PM and back
def AM_PM():
    global mode
    if mode=="%H:%M:%S":
        mode="%I:%M:%S:%p"
    else:
        mode="%H:%M:%S"
#Function adding a menu to navigate between all the features, and managing the thread for the changed time the alarm
#and the pauuse, allowing them to operate separately from the rest
def menu():
    alarm_thread = None  
    while True:
        print("\nMenu:")
        print("1: Clock")
        print("2: Set alarm")
        print("3: Change time manually")
        print("4: Reset the clock to default time")
        print("5: Pause")
        print("6: Change time mode")
        print("7: Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Press Ctrl+C to go back to menu.")
            clock()
        elif choice == "2":
            ring = input("Enter the time for your alarm (HH:MM:SS): ")
            if alarm_thread and alarm_thread.is_alive():
                print("Alarm already set. Returning to menu.")
            else:
                print("Setting alarm...")
                alarm_thread = threading.Thread(target=alarm, args=(ring,))
                alarm_thread.start()
        elif choice == "3":
            time_updater_thread = threading.Thread(target=update_time, daemon=True)
            time_updater_thread.start()
            change_time() 
        elif choice =="4":
            reset_time()
        elif choice =="5":
            pause()
        elif choice =="6":
            AM_PM()
        elif choice == "7":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 6 or 7.")
#Calling the menu to start the program
menu()
