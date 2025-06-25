import os
import re

def extract_text_from_srt(srt_path):
    encodings_to_try = ['utf-8', 'utf-16', 'iso-8859-1', 'windows-1252']
    
    for enc in encodings_to_try:
        try:
            with open(srt_path, 'r', encoding=enc) as f:
                lines = f.readlines()
            break  # success
        except UnicodeDecodeError:
            continue
    else:
        print(f"❌ Failed to decode: {srt_path}")
        return ""  # skip this file


    text_lines = []
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+$', line):
            continue  # skip index numbers
        if re.match(r'\d{2}:\d{2}:\d{2},\d{3}', line):
            continue  # skip timestamps
        if line == '':
            continue  # skip empty lines
        line = remove_html_tags(line)
        line = remove_curly_bracket_inside(line)
        text_lines.append(line)
    return ' '.join(text_lines)

def remove_html_tags(text):
    return re.sub(r'<[^>]+>', '', text)

def remove_curly_bracket_inside(text):
    return re.sub(r'{[^}]*}', '', text)


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\"\“\”\‘\’\'\#\=\/\-\!\+\♪\*\@\!\+\;\$\%\&`]', '', text)
    text = re.sub(r'\.{2,}', '', text)
    text = re.sub(r'\b[a-zA-Z]+\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_long_sentences(text, max_words=12):
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def save_to_txt(sentences, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(sentence + '\n')

# New function to process all srt files in a folder
def process_all_srt_in_folder(folder_path, output_file):
    all_sentences = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.srt'):
            srt_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")
            raw_text = extract_text_from_srt(srt_path)
            cleaned = clean_text(raw_text)
            split_sentences = split_long_sentences(cleaned, max_words=12)
            all_sentences.extend(split_sentences)

    save_to_txt(all_sentences, output_file)
    print(f"\n✅ All cleaned text saved to {output_file}")

# Example usage
if __name__ == "__main__":
    folder_path = "C:/Users/ASUS/Desktop/FYP/Codes/SpellCorrectorDataset/srtFiles2"  # Replace with your folder path
    output_file = "C:/Users/ASUS/Desktop/FYP/Codes/SpellCorrectorDataset/sinhala_dataset.txt"
    process_all_srt_in_folder(folder_path, output_file)
