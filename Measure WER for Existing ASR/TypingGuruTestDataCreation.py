import time
import csv
import os
import pyperclip
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import simpleaudio as sa

TSV_PATH = "C:/Users/ASUS/Desktop/FYP/Codes/spontaniousTest.tsv"
AUDIO_FOLDER = "C:/Users/ASUS/Desktop/FYP/Codes/asr_sinhala/SponAudio_WAV"
WAIT_AFTER_AUDIO = 3
WAIT_AFTER_MIC = 2

chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream") 
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})
# ---- Selenium Setup ----
driver = webdriver.Chrome()
driver.get("https://www.typingguru.net/voice-to-text/sinhala-voice-typing") 


time.sleep(5)


input_box = driver.find_element(By.ID, "final_span")
driver.execute_script("arguments[0].focus();", input_box)
driver.execute_script("arguments[0].click();",input_box)

with open(TSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    rows = list(reader)

results = []

for row in rows:
    audio_file = row[0]
    audio_path = os.path.join(AUDIO_FOLDER, audio_file)

    mic_icon = driver.find_element(By.ID, "start_button")


    driver.execute_script("arguments[0].click();", mic_icon)
    timeout = 2
    time.sleep(timeout)

    wave_obj = sa.WaveObject.from_wave_file(audio_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    time.sleep(1)
    driver.execute_script("arguments[0].focus();", input_box)
    driver.execute_script("arguments[0].click();",input_box)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    transcription = pyperclip.paste().strip()
    driver.execute_script("arguments[0].click();", mic_icon)
    timeout = 10
    time.sleep(WAIT_AFTER_MIC)

    print(transcription)
    results.append((audio_file, transcription))

    clear_button = driver.find_element(By.ID, "reset_button")
    driver.execute_script("arguments[0].click();", clear_button)
    time.sleep(2)

# ---- Save results ----
with open("C:/Users/ASUS/Desktop/FYP/Codes/typingguru_transcriptions_spo.tsv", "w", encoding="utf-8") as out:
    for file_name, transcript in results:
        out.write(f"{file_name}\t{transcript}\n")

driver.quit()
print("✅ All done!")
