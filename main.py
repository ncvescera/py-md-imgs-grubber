import argparse
import requests
import os
import re


def main(args):
    links = []
    lines = []

    with open(args.file_name, "r") as file:
        lines = file.readlines()

    links = find_all_imgs(lines)

    print(f"Totale: {len(links)}")

    if args.nosave is False:
        downloand_links(links, args.wget, args.type)


def find_all_imgs(lines):
    links = []

    i = 1  # row number
    for line in lines:
        regex_html = re.findall(r'<img[^>]+src="([^">]+)"', line.strip(" \n"))  # prende il contenuto di src
        regex_md = re.findall(r'!\[[^\]]+\]\(([^\)]+)\)', line.strip(" \n"))    # prende il contenuto in ()

        total_links = regex_html + regex_md

        if len(total_links) > 0:
            j = 0  # imgs number per row

            print(f"Line {i}", end=' ')

            for elem in total_links:
                print(elem, end=' ')

                links.append((elem, f"{i}_{j}"))
                j += 1

            print(j)    # alla fine sarà il numero di link trovati
        i += 1

    return links


def downloand_links(links, wget, ext):
    if ext is None:
        ext = "gif"
    
    # Scarica i link trovati
    for link, row in links:
        if wget:
            os.system(f"wget \"{link}\" -O \"line{row}.{ext}\"")

        else:
            print(f"Downloanding line{row}.{ext} ...")

            # L'immagine verrà scaricata per forza !
            # Se non riesce a scaricare l'immagine ci riporva
            end = True
            while end:
                try:
                    req = requests.get(link, timeout=5)
                    open(f"line{row}.{ext}", 'wb').write(req.content)

                except Exception:
                    print("\tRiprovo...")
                    continue

                end = False

            print("OK")


def init_args():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('file_name', help="File to operate with")
    parser.add_argument('--nosave', action='store_true', help="Print the links only, no downloands")
    parser.add_argument('--wget', action='store_true', help="Downloand files with wget software (you must have wget installed)")
    parser.add_argument('--type', help="Choose the extention type [<gif>, <png>, ...]")

    return parser.parse_args()


if __name__ == "__main__":
    args = init_args()

    main(args)
