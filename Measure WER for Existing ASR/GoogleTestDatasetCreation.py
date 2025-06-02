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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---- CONFIGURATION ----
TSV_PATH = "C:/Users/ASUS/Desktop/FYP/Codes/spontaniousTest.tsv"
AUDIO_FOLDER = "C:/Users/ASUS/Desktop/FYP/Codes/asr_sinhala/SponAudio_WAV"
WAIT_AFTER_AUDIO = 3
WAIT_AFTER_MIC = 1

chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Auto-allow mic/cam
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,  # 1=allow
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})
# ---- Selenium Setup ----
driver = webdriver.Chrome()#executable_path="C:/chromDriver/chrome-headless-shell-win64/chrome-headless-shell.exe")  # Make sure chromedriver is in PATH
driver.get("https://translate.google.lk/?hl=en&vi=c&sl=si&tl=en&op=translate")  # Example Helakuru web keyboard

# Wait for page to load
time.sleep(5)

# Focus on the input box
input_box = driver.find_element(By.CLASS_NAME, "er8xn")  # Adjust selector as needed
driver.execute_script("arguments[0].focus();", input_box)
driver.execute_script("arguments[0].click();",input_box)
wait = WebDriverWait(driver, 10)
# ---- Process TSV ----
with open(TSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    rows = list(reader)

# ---- Loop through audio files ----
results = []

for row in rows:
    audio_file = row[0]
    audio_path = os.path.join(AUDIO_FOLDER, audio_file)

    mic_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='Sz6qce']"))
    )
    driver.execute_script("arguments[0].click();", mic_button)
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
    driver.execute_script("arguments[0].click();", mic_button)
    timeout = 10
    time.sleep(WAIT_AFTER_MIC)
    print(transcription)
    results.append((audio_file, transcription))
    clear_button = driver.find_element(By.CSS_SELECTOR,"button[aria-label='Clear source text']")
    driver.execute_script("arguments[0].click();", clear_button)
    time.sleep(2)

# ---- Save results ----
with open("C:/Users/ASUS/Desktop/FYP/Codes/google_transcriptions_spont.tsv", "w", encoding="utf-8") as out:
    for file_name, transcript in results:
        out.write(f"{file_name}\t{transcript}\n")

driver.quit()
print("✅ All done!")
