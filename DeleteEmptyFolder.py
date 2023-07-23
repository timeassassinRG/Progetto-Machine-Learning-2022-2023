import os

def delete_empty_folders(directory):
    # Percorso assoluto della cartella
    abs_directory = os.path.abspath(directory)

    # Controllo se il percorso esiste
    if not os.path.exists(abs_directory):
        print(f"La cartella '{directory}' non esiste.")
        return

    # Funzione ricorsiva per eliminare cartelle vuote
    def delete_empty_recursive(folder):
        try:
            # Lista di elementi all'interno della cartella
            items = os.listdir(folder)
        except OSError:
            return

        # Se non ci sono elementi, elimino la cartella vuota
        if not items:
            print(f"Rimozione della cartella vuota: {folder}")
            os.rmdir(folder)
            return

        # Controllo se ci sono altre cartelle all'interno
        subfolders = [item for item in items if os.path.isdir(os.path.join(folder, item))]

        # Se ci sono cartelle, continuo la ricerca in profondità
        for subfolder in subfolders:
            delete_empty_recursive(os.path.join(folder, subfolder))

    # Inizio l'eliminazione delle cartelle vuote
    delete_empty_recursive(abs_directory)

if __name__ == "__main__":
    # Specifica il percorso della cartella da esaminare
    # richiedi all'utente di inserire il percorso
    folder_path = input("Inserisci il percorso della cartella da esaminare: ")
    delete_empty_folders(folder_path)