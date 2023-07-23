import os
from PIL import Image
import hashlib
from tqdm import tqdm

def calculate_md5(image_path):
    with open(image_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def find_and_remove_duplicates(folder_path, input_image_path):
    input_md5 = calculate_md5(input_image_path)
    duplicates = []
    removed_count = 0

    total_files = sum([len(files) for _, _, files in os.walk(folder_path)])

    with tqdm(total=total_files, desc="Processing images") as pbar:
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                image_path = os.path.join(root, file_name)
                if image_path != input_image_path:
                    md5 = calculate_md5(image_path)
                    if md5 == input_md5:
                        duplicates.append(image_path)
                        removed_count += 1
                        os.remove(image_path)
                pbar.update(1)

    print(f"Removed {removed_count} duplicate images.")

if __name__ == "__main__":
    # Inserisci il percorso della cartella contenente le immagini e l'immagine di input
    folder_path = input("Inserisci il percorso della cartella contenente le immagini: ")
    input_image_path = "132.jpg"

    find_and_remove_duplicates(folder_path, input_image_path)
