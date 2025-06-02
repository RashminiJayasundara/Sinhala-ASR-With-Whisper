import re

def clean_text(text):

    # Remove inverted commas and quotes
    text = re.sub(r'[\"\“\”\‘\’\'\-\=\#\>\>\@\*\&\^\%\$\(\)\°\}\{\:\[\]\|\,\/\•\–\+\!\;\?\…\»\श\नि\~\෴\↑\→ `]', '', text)

    # Remove "..." and multiple dots
    text = re.sub(r'\.{2,}', '', text)

    # Remove English words (basic method: remove words with a-z or A-Z)
    text = re.sub(r'\b[a-zA-Z]+\b', '', text)
    text = re.sub(r'\b[0-9]+\b','',text)
    return text

def split_long_sentences(text, max_words=12):
    sentences = []
    words = text.split()
    
    for i in range(0, len(words), max_words):
        chunk = words[i:i+max_words]
        sentences.append(' '.join(chunk))
    
    return sentences

def prepare_dataset(raw_text):
    cleaned_text = clean_text(raw_text)
    split_sentences = split_long_sentences(cleaned_text, max_words=12)
    return split_sentences

def save_to_txt(sentences, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(sentence + '\n')

# === Main Function ===
if __name__ == "__main__":
    input_file = 'C:/Users/ASUS/Desktop/FYP/Codes/SpellCorrectorDataset/part_6.txt'
    output_file = 'sinhala_dataset2.txt'

    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    dataset = prepare_dataset(raw_text)
    save_to_txt(dataset, output_file)

    print(f"Cleaned dataset saved to '{output_file}'")
