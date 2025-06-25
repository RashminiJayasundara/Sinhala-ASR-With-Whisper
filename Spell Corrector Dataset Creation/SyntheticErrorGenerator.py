import random
import csv

vowels = ["අ", "ආ", "ඇ", "ඈ", "ඉ", "ඊ", "උ", "ඌ", "එ", "ඒ", "ඔ", "ඕ"]
vowels_combine = {
    "ආ": "ා",
    "ඉ": "ි",
    "ඊ": "ී",
    "උ": "ු",
    "ඌ": "ූ",
    "එ": "ෙ",
    "ඒ": "ේ",
    "ඔ": "ො", 
    "ඕ": "ෝ",
    "ඇ": "ැ",
    "ඈ": "ෑ"
}
vowels_combine_swapped = {
    "ා": "ආ",
    "ි": "ඉ",
    "ී": "ඊ",
    "ු": "උ",
    "ූ": "ඌ",
    "ෙ": "එ",
    "ේ": "ඒ",
    "ො": "ඔ",
    "ෝ": "ඕ",
    "ැ": "ඇ",
    "ෑ": "ඈ"
}

long_vowels = ["ා", "ී", "ූ", "ේ", "ෝ", "ෑ", "ි", "ු","ො","ැ"]

similar_characters = {
    "ත": "ද",
    "ට": "ඩ",
    "ක": "ග",
    "ප": "බ",
    "හ": "ඝ",
    "ය": "ජ",
    "ය": "ර",
    "ප":"හ",
    "ප":"ම",
    "ල":"ළ",
    "ප":"අ","න":"ණ","ශ":"ෂ","න":"ම","ව":"ම","ශ":"හ","ෂ":"හ",

}
sinhala_consonants = {
    'ක':'ක්', 'ග':'ග්', 
    'ච':'ච්', 'ජ':'ජ්',
    'ට':'ට්', 'ඩ':'ඩ්',  'ණ':'ණ්',
    'ත':'ත්',  'ද':'ද්',  'න':'න්',
    'ප':'ප්', 'බ':'බ්',  'ම':'ම්',
    'ය':'ය්', 'ර':'ර්', 'ල':'ල්', 'ව':'ව්',
     'ස':'ස්', 
}
n_sounds =["ම්","න්","ං","ණ්","ඞ","ඤ්"]
groups = [
    [ 'ක', 'ග', 'හ'], #'අ'
    [ 'ච', 'ජ', 'ය', 'ශ'],#'ඉ',
    ['ට', 'ඩ', 'ණ', 'ර', 'ළ', 'ෂ'],
    ['ත', 'ද', 'න', 'ල', 'ස']
]


# Flatten groups into a dictionary mapping each char to its group
char_to_group = {}
for group in groups:
    for ch in group:
        char_to_group[ch] = group
def merge_words_with_vowel_drop(word1, word2):
    if word2 and word2[0] in vowels:
        
        if  word1[-1] not in long_vowels and len(word1)>=3:
            # Instead of item assignment, create a new string
            if word1[-1]=="්" :
                word1 = word1 +word1[-2] + vowels_combine.get(word2[0], "") 
            else: 
                word1 = word1[:-1] + word1[-1] + vowels_combine.get(word2[0], "")
              
        word2 = word2[1:]  # Remove the first vowel
        return[word1+word2]
    return [word1, word2] 


def second_word_vowels_merge_with_first_word(word1, word2):
    if word2 and word2[0] in vowels and word1[-1] not in long_vowels and len(word1)>=3:
        if word1[-1]=="්":
            word1 = word1 +word1[-2] + vowels_combine.get(word2[0], "")  
        else:
            word1 = word1[:-1] + word1[-1] + vowels_combine.get(word2[0], "")  
            word2 = word2[1:]  # Remove the first vowel
    return [word1, word2] 


def create_vowel_drop_merge(sentence, mistake_chance=0.9):
    words = sentence.strip().split()
    new_words = []
    idx = 0

    while idx < len(words) - 1:
        word1 = words[idx]
        word2 = words[idx + 1]

        if random.random() < mistake_chance:
            # Apply vowel drop merging
            merged_words = merge_words_with_vowel_drop(word1, word2)
            new_words.extend(merged_words) # Add both words if word2 is not empty
            idx += 2  # skip next word because it's merged
        else:
            new_words.append(word1)
            idx += 1

    # If last word was not merged
    if idx == len(words) - 1:
        new_words.append(words[-1])

    return " ".join(new_words)

def create_vowel_drop_split(sentence, mistake_chance=0.9):
    words = sentence.strip().split()
    new_words = []
    idx = 0

    while idx < len(words) - 1:
        word1 = words[idx]
        word2 = words[idx + 1]

        if random.random() < mistake_chance:
            # Apply vowel drop merging
            merged_words = second_word_vowels_merge_with_first_word(word1, word2)
            new_words.extend(merged_words) # Add both words if word2 is not empty
            idx += 2  # skip next word because it's merged
        else:
            new_words.append(word1)
            idx += 1

    # If last word was not merged
    if idx == len(words) - 1:
        new_words.append(words[-1])

    return " ".join(new_words)

# Load your Sinhala clean text
with open("C:/Users/ASUS/Desktop/FYP/Codes/SpellCorrectorDataset/part_6_fil.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
# Chance of introducing a mistake
synthetic_lines = []
synthetic_lines2=[]
for line in lines:
    if random.random()<0.7:
        edit_sentence = create_vowel_drop_merge(line)
        synthetic_lines.append(edit_sentence)
    else:
        synthetic_lines.append(create_vowel_drop_split(line))
a,b,c,d,e,f,g,h,i,j,k =0,0,0,0,0,0,0,0,0,0,0


for line in synthetic_lines:
        words = line.strip().split()
        new_words = []
        synthetic_line2 = ""
        replaced = False
        for word in words:
            # Randomly decide if we introduce a mistake
            if True:
                mistake_type = random.choice(["char_replace","char_replace2","char_replace3","replace_vowel", "vowel_error","vowel_error2", "word_split","char_long","n_sound","i_sound","lop_vowels"])
                if mistake_type == "char_replace":
                    result = ""
                    for ch in word:
                        if not replaced and ch in char_to_group and random.random() < 0.9:
                        # Choose a random character from the same group (excluding itself optional)
                            replacement = random.choice(char_to_group[ch])
                            result += replacement
                            a+=1
                            replaced=True
                        else:
                            result += ch 
                    if result:word=result
                elif mistake_type == "char_replace2":
                    for correct, wrong in similar_characters.items():
                        if correct in word:
                            word.replace(correct,wrong,1)
                            i+=1
                        break
                elif mistake_type == "char_replace3":
                    for  wrong,correct in similar_characters.items():
                        if correct in word:
                            word.replace(correct,wrong,1)
                            j+=1
                        break
                elif mistake_type=="lop_vowels":
                    for vowel in vowels:
                        if vowel in word and vowel==word[0] :
                            word = word[1:]
                            b+=1
                elif mistake_type=="replace_vowel":
                    for pillama,vowel in vowels_combine_swapped.items():
                        if len(word)>=2 and word[1]==pillama:
                            word=vowel+word[2:]
                            h+=1
                        break
                elif mistake_type == "vowel_error":
                    # Randomly remove or duplicate vowels
                    vowels_ = ["ා", "ි", "ී", "ු", "ූ", "ෙ", "ේ", "ො", "ෝ", "ැ", "ෑ"]
                    for vowel in vowels_:
                        if vowel in word and len(word) > 2:
                            word = word.replace(vowel, "", 1)  # Remove vowel once
                            c+=1
                        break
                elif mistake_type == "vowel_error2":
                    # Randomly remove or duplicate vowels
                    vowels_ = ["ා", "ි", "ී", "ු", "ූ", "ෙ", "ේ", "ො", "ෝ", "ැ", "ෑ"]
                    for vowel in vowels_:
                        if vowel in word and len(word) > 2:
                            word = word.replace(vowel, random.choice(vowels_), 1)  # Remove vowel once
                            k+=1
                        break

                elif mistake_type == "word_split" and len(word) > 3:
                    # Split the word into two parts at a random position
                    split_point = random.randint(1, len(word) - 2)
                    word = word[:split_point] + " " + word[split_point:]
                    d+=1
                elif mistake_type == "char_long":
                    for exist, goingtoChange in sinhala_consonants.items():
                        if(exist in word and  exist!= word[0]):
                            point = word.index(exist)
                            word = word[:point]+goingtoChange+word[point:]
                            e+=1
                            break
                elif mistake_type == "n_sound":
                    for m in n_sounds:
                        if(m in word):
                            word = word.replace(m, n_sounds[random.randint(0, 5)], 1)
                            f+=1
                elif mistake_type == "i_sound":
                    if('ෛ' in word):
                        word = word.replace('ෛ','යි',1)
                        g+=1


            new_words.append(word)

        synthetic_line2 = " ".join(new_words)
        synthetic_lines2.append(synthetic_line2)


with open('C:/Users/ASUS/Desktop/FYP/Codes/SpellCorrectorDataset/sinhala_synthetic_dataset_16.tsv', 'w', encoding='utf-8', newline='') as file:
    tsv_writer = csv.writer(file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    tsv_writer.writerow(['prediction', 'groundtruth'])  # header
    
    for pred, gt in zip(synthetic_lines2, lines):
        clean_pred = pred.strip().replace('\n', ' ').replace('\r', '')
        clean_gt = gt.strip().replace('\n', ' ').replace('\r', '')
        tsv_writer.writerow([clean_pred, clean_gt])


print("a=",a,"b=",b,"c=",c,"d=",d,"e=",e,"f=",f,"g=",g,"h=",h,"i=",i,"j=",j,"k=",k)
print("✅ Synthetic misspelled dataset created successfully!")


