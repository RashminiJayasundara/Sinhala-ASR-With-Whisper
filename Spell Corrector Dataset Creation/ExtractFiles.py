import os
import zipfile
import shutil

def extract_zip_files(zip_folder, extract_temp):
    for file in os.listdir(zip_folder):
        if file.lower().endswith('.zip'):
            zip_path = os.path.join(zip_folder, file)
            print(f"Extracting: {zip_path}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                extract_path = os.path.join(extract_temp, os.path.splitext(file)[0])
                zip_ref.extractall(extract_path)

def collect_srt_files(src_dir, dest_dir):
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith('.srt'):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, file)
                print(f"Copying: {src_path} -> {dest_path}")
                shutil.copy2(src_path, dest_path)

def process_zip_srt(zip_folder, temp_extract_dir, srt_output_dir):
    os.makedirs(temp_extract_dir, exist_ok=True)
    os.makedirs(srt_output_dir, exist_ok=True)

    extract_zip_files(zip_folder, temp_extract_dir)
    collect_srt_files(temp_extract_dir, srt_output_dir)


# Example usage
if __name__ == "__main__":
    zip_folder = "C:/Users/ASUS/Desktop/FYP/Codes/SpellCorrectorDataset/zips2"  # Folder with .zip files
    temp_extract_dir = "C:/Users/ASUS/Desktop/FYP/Codes/SpellCorrectorDataset/extracted"  # Temp folder for unzipping
    srt_output_dir = "C:/Users/ASUS/Desktop/FYP/Codes/SpellCorrectorDataset/srtFiles2"  # Final folder for .srt files

    process_zip_srt(zip_folder, temp_extract_dir, srt_output_dir)
