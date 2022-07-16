import wave
import glob

path = "./"
file_extension = 'wav'
file_list = glob.glob(f'{path}/**/*.{file_extension}', recursive=True)

error = 0
frame_too_little = 0
for file_name in file_list: 
    try:
        with wave.open(file_name, "rb") as wave_file:
            frame_rate = wave_file.getframerate()
            if frame_rate < 44100:
                frame_too_little += 1
                print(file_name, ":", frame_rate, "Hz")
    except:
        error += 1
        continue

print("error times:", error)
print("frame too little number:", frame_too_little)
