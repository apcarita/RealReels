import os
import time  # Optional, if you want a delay between runs


if __name__ == "__main__":



        for i in range(6):
           print(f"Running your_script.py - Attempt {i + 1}")
           os.system("python3 ReelCreator.py")  # Replace "python" with "python3" if needed
           time.sleep(5)  # Optional delay in seconds