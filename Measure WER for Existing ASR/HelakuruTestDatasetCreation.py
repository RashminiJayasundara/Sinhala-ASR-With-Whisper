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

TSV_PATH = "C:/Users/ASUS/Desktop/FYP/Codes/SpellCorrectorDataset/30refinedOrigiinal.tsv"
AUDIO_FOLDER = "C:/Users/ASUS/Desktop/FYP/Codes/whisper/testData2WAV"
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
driver.get("https://www.helakuru.lk/")  


time.sleep(5)

# Focus on the input box
input_box = driver.find_element(By.ID, "results") 
driver.execute_script("arguments[0].focus();", input_box)
driver.execute_script("arguments[0].click();",input_box)


with open(TSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    rows = list(reader)

results = []
mic_div = driver.find_element(By.CSS_SELECTOR, "div[class*='voice-typing-icon']") 
for row in rows:
    audio_file = row[0]+".wav"
    audio_path = os.path.join(AUDIO_FOLDER, audio_file)
    mic_icon = mic_div.find_element(By.CSS_SELECTOR, "i.fal.fa-microphone")


    driver.execute_script("arguments[0].click();", mic_icon)
    timeout = 1
    time.sleep(timeout)
    wave_obj = sa.WaveObject.from_wave_file(audio_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

    time.sleep(1)

    driver.execute_script("arguments[0].focus();", input_box)
    driver.execute_script("arguments[0].click();",input_box)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1) 
    transcription = pyperclip.paste().strip()

    driver.execute_script("arguments[0].click();", mic_icon)
    timeout = 10
    time.sleep(WAIT_AFTER_MIC)
    print(transcription)
    results.append((audio_file, transcription))

    button = driver.find_element(By.XPATH, "//a[text()='Clear']")
    button.click()
    time.sleep(2)
    
with open("C:/Users/ASUS/Desktop/FYP/Codes/helakuru_transcriptions_script.tsv", "w", encoding="utf-8") as out:
    for file_name, transcript in results:
        out.write(f"{file_name}\t{transcript}\n")

driver.quit()
print("✅ All done!")
