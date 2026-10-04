from csv import reader, writer

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    albumFoto ={}
    try:
        infile = open(file_path, "r")
        csvReader = reader(infile)
        for (indice, row) in enumerate(csvReader):
            #verifico che csvReader non stia leggendo la prima riga del file (riga di intestazioni colonne)
            if indice !=0:
                codice = row[0]
                titolo = row[1]
                autore = row[2]
                mese = int(row[3])
                anno = int(row[4])
                if anno not in albumFoto:
                    """inserisco nel dizionario AlbumFoto un elemento con chiave anno e valor associato
                    un altro dizionario con un elemento con chiave codice e valor un altro dizionario,  """
                    albumFoto[anno] = {codice:{'titolo':titolo,
                                               'autore': autore,
                                               'mese':mese
                                               }
                                       }

                else:
                    """ inserisco nel dizionario che rappresenta il valor associato alla chiave anno presente
                    nel dizionario albumFoto un elemento avente come chiave codice e valor un atro dizionario"""
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

    # verifico che il codice della foto non sia gia presente nell'album fotografico
    for keyAnno in album:
        if codice in album[keyAnno]:
            return None
    #verifico se il mese inserito è valido (il mese è già stato convertito in intero)
    if mese <1 or mese >12:
        return None

    else:
        try:

            outfile = (open(file_path, 'a'))
            csvWriter= writer(outfile, lineterminator='\n')
            csvWriter.writerow([codice, titolo, autore, mese, anno])
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
        #se il file non vien trovato, la funzione restituisce None
        except FileNotFoundError:
            return None
    #restituisco un riferimento alla foto aggiunta
    return riferimentoFoto



def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    trovata = False
    #itero su ogni chiave (che rappresenta un anno) presente nel dizionario ALbumFoto
    for keyAnno in album:
        if codice in album[keyAnno]:
            trovata = True
            """creo una lista con in prima pos la chiave del dizionario album tale per cui nel dizionario associato
             a essa è stato trovato un elemento che ha per chiave il codice cercato, e in seconda pos il dizionario 
             associato alla chiave codice (contenuta nel dizionario album)"""
            infoFoto = [keyAnno, album[keyAnno][codice]]
            break
    if trovata:
        # restituisco una strnga con le informazioni della foto avente quel codice
        stringaFoto= f"{codice}, {infoFoto[1]['titolo']}, {infoFoto[1]['autore']}, {infoFoto[1]['mese']}, {infoFoto[0]}"
        return stringaFoto
    else:
        return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno in album:
        listaTitoli = []

        """itero sulle chiavi (che son i codici delle foto) del dizionario che è il valor associato alla chiave 
        anno nel dizionario album"""
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
