from csv import reader
def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    albumFoto ={}
    try:
        infile = open(file_path, "r")
        csvReader = reader(infile)
        for row in csvReader:
            anno = row[4]
            #verifico se il csvReader sta leggendo la prima riga del file (riga di intestazioni colonne)
            if anno.isdigit():
                codice = row[0]
                titolo = row[1]
                autore = row[2]
                mese = int(row[3])
                anno = int(anno)
                if anno not in albumFoto:
                    albumFoto[anno] = {codice:{'titolo':titolo,
                                               'autore': autore,
                                               'mese':mese
                                               }
                                       }
                else:
                    albumFoto[anno][codice]= {'titolo':titolo,
                                              'autore':autore,
                                              'mese': mese
                                             }
        infile.close()
        return albumFoto

    except FileNotFoundError:
        return None



def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    for keyAnno in album:
        if codice in album[keyAnno]:
            return None
    if mese <1 or mese >12:
        return None

    else:
        try:
            outfile = open(file_path, 'a')
            outfile.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
            outfile.close()
            if anno not in album:
                album[anno] = {codice:{'titolo':titolo,
                               'autore':autore,
                               'mese':mese
                                       }
                               }
            else:
                album[anno][codice]= {'titolo':titolo,
                                      'autore':autore,
                                      'mese': mese
                                      }
            riferimentoFoto = album[anno][codice]
        except FileNotFoundError:
            return None
    return riferimentoFoto



def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    trovata = False
    for keyAnno in album:
        if codice in album[keyAnno]:
            trovata = True
            infoFoto = [keyAnno, album[keyAnno][codice]]
            break
    if trovata:
        stringaFoto= f"{codice}, {infoFoto[1]['titolo']}, {infoFoto[1]['autore']}, {infoFoto[1]['mese']}, {infoFoto[0]}"
        return stringaFoto
    else:
        return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno in album:
        listaTitoli = []
        for keyCodice in album[anno]:
            listaTitoli.append(album[anno][keyCodice]['titolo'])
        listaTitoli.sort()
        return listaTitoli
    else:
        return None

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
