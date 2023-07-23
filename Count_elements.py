import os

def count_elements_in_folders(directory):
    # Percorso assoluto della cartella
    abs_directory = os.path.abspath(directory)

    # Controllo se il percorso esiste
    if not os.path.exists(abs_directory):
        print(f"La cartella '{directory}' non esiste.")
        return

    # Variabili per tenere traccia dei conteggi
    num_files = 0
    num_folders = 0
    num_empty_folders = 0

    # Funzione ricorsiva per conteggio elementi
    def count_recursive(folder):
        nonlocal num_files, num_folders, num_empty_folders
        try:
            # Lista di elementi all'interno della cartella
            items = os.listdir(folder)
        except OSError:
            return

        # Incremento il conteggio in base al tipo di elemento
        for item in items:
            item_path = os.path.join(folder, item)
            if os.path.isfile(item_path):
                num_files += 1
            elif os.path.isdir(item_path):
                num_folders += 1
                if not os.listdir(item_path):  # Controlla se la cartella è vuota
                    num_empty_folders += 1
                count_recursive(item_path)

    # Inizio il conteggio degli elementi
    count_recursive(abs_directory)

    # Stampo i risultati
    print(f"Numero totale di file: {num_files}")
    print(f"Numero totale di cartelle: {num_folders}")
    print(f"Numero totale di cartelle vuote: {num_empty_folders}")

if __name__ == "__main__":
    # Specifica il percorso della cartella da esaminare
    # richiedi all'utente di inserire il percorso
    folder_path = input("Inserisci il percorso della cartella da esaminare: ")
    count_elements_in_folders(folder_path)