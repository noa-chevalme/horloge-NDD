import datetime
import time
import threading

current_time = datetime.datetime.now()

def get_current_time():
    global current_time
    return current_time.strftime("%H:%M:%S")

def alarm(ring):
    while True:
        current_time_str = get_current_time()
        if current_time_str == ring:
            print("\nDing! Your alarm is ringing!")
            break
        time.sleep(1)  

def clock():
    try:
        while True:
            print(f"\rCurrent time: {get_current_time()}", end="")
            time.sleep(1)  
    except KeyboardInterrupt:
        print("\nClock stopped.")

def change_time():
    global current_time
    new_time_str = input("Enter the new time (HH:MM:SS): ")
    try:
        new_time = datetime.datetime.strptime(new_time_str, "%H:%M:%S")
        current_time = new_time
        print(f"Time changed to {get_current_time()}")
    except ValueError:
        print("Invalid time format. Please enter in HH:MM:SS format.")

def update_time():
    global current_time
    while True:
        time.sleep(1)  
        current_time += datetime.timedelta(seconds=1)  
def menu():
    alarm_thread = None  
   
    time_updater_thread = threading.Thread(target=update_time, daemon=True)
    time_updater_thread.start()
    
    while True:
        print("\nMenu:")
        print("1: Clock")
        print("2: Set Alarm")
        print("3: Change Time Manually")
        print("4: Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Press Ctrl+C to stop the clock.")
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
            change_time() 
        elif choice == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
menu()
