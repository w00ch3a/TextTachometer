import os
import spacy
from concurrent.futures import ThreadPoolExecutor

def process_text(content, nlp):
    return [nlp(text) for text in content.split('\n\n') if text.strip()]

def load_and_process_file(file_path, nlp):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return process_text(content, nlp)

def setup_nlp(profile):
    components = ['ner', 'lemmatizer', 'parser']
    if profile in ['1', '2']:  # Basic or Moderate
        components = ['ner', 'parser']  # Disable lemmatizer for less intensive computation
    nlp = spacy.load('en_core_web_sm', disable=components)
    return nlp

def main():
    directory = '/path/to/your/text/files'
    output_directory = '/path/to/output/files'
    os.makedirs(output_directory, exist_ok=True)
    
    print("Select a performance profile:")
    print("1: Basic (Suitable for low-power devices like Raspberry Pi)")
    print("2: Moderate (Suitable for older laptops/PCs)")
    print("3: Balanced (Suitable for modern PCs)")
    print("4: High (Suitable for high-end PCs and workstations)")
    print("5: Extreme (Suitable for servers and cloud environments)")
    
    choice = input("Enter your choice (1-5): ")
    nlp = setup_nlp(choice)
    
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    
    if choice in ['4', '5']:  # High or Extreme performance
        # Using ThreadPoolExecutor for parallel processing of files
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            results = list(executor.map(lambda f: load_and_process_file(f, nlp), files))
    else:
        results = [load_and_process_file(f, nlp) for f in files]
    
    # Saving processed data
    for result, file in zip(results, files):
        output_file = os.path.join(output_directory, os.path.basename(file).replace('.txt', '_processed.txt'))
        with open(output_file, 'w', encoding='utf-8') as f:
            for doc in result:
                f.write(' '.join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha]) + '\n')

    print("Processing complete. Check the output directory for processed files.")

if __name__ == '__main__':
    main()
