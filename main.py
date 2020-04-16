import argparse
import requests
import os
import re


def main(args: argparse):
    links = []  # all the links inside the document
    lines = []  # all the document lines

    # read all the lines, fill lines list
    with open(args.file_name, "r") as file:
        lines = file.readlines()

    # get all the links inside the document
    links = find_all_imgs(lines)

    print(f"Totale: {len(links)}")

    # downloand the links
    if args.nosave is False:
        downloand_links(links, args.wget, args.type)


# find all the img-links in the giving list and print the result
def find_all_imgs(lines: list) -> list:
    links = []

    i = 1  # row number
    for line in lines:
        # regular expressions for getting img-links
        # regex_html and regex_md are lists if somthing is found, otherwise they are empty lists
        regex_html = re.findall(r'<img[^>]+src="([^">]+)"', line.strip(" \n"))  # if an img tag found, get the src values (HTML)
        regex_md = re.findall(r'!\[[^\]]+\]\(([^\)]+)\)', line.strip(" \n"))    # if an ![]() found, get the value inside () (Markdown)

        # concatenate html regex result with markdonw regex result
        total_links = regex_html + regex_md

        # if a link is found
        if len(total_links) > 0:
            j = 0  # imgs number per row

            print(f"Line {i}", end=' ')

            for elem in total_links:
                print(elem, end=' ')

                links.append((elem, f"{i}_{j}"))
                j += 1

            print(j)    # print total links found in the line
        i += 1

    return links


# downloand the links in the list 'links'
# links <list>: list with links
# wget  <bool>: If True, downloand the link with system wget software
# ext   <str>:  The extention that user choose. Default 'gif'
def downloand_links(links: list, wget: bool, ext: str):
    # If the user omitted --type, set ext as 'gif'
    if ext is None:
        ext = "gif"
    
    # downoand links in list links
    for link, row in links:
        # If --wget is passed by the user downloand links with system wget software
        if wget:
            os.system(f"wget \"{link}\" -O \"line{row}.{ext}\"")

        else:
            print(f"Downloanding line{row}.{ext} ...")

            # if the is some problems while downloanding the link,
            # it restarts the downloand
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


# initialize argparse for the command line arguments
def init_args() -> argparse:
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('file_name', help="File to operate with")
    parser.add_argument('--nosave', action='store_true', help="Print the links only, no downloands")
    parser.add_argument('--wget', action='store_true', help="Downloand files with wget software (you must have wget installed)")
    parser.add_argument('--type', help="Choose the extention type [<gif>, <png>, ...]")

    return parser.parse_args()


if __name__ == "__main__":
    args = init_args()

    main(args)
