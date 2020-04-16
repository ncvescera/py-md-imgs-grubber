# py-md-imgs-grubber
Python script for getting imgs links from a Markdown file

## Usage

`python main.py <file_name> [optiona arguments]`

### Required arguments

`file_name` is the only required argument. It is the name of the file you want to operate with.

### Optional arguments

```text
  --nosave     Print the links only, no downloands
  --wget       Downloand files with wget software (you must have wget
               installed)
  --type TYPE  Choose the extention type [<gif>, <png>, ...]
```

* `--nosave`: Print the links only. If omitted, after printing links, the script downloands them
* `--wget`: Downloand links with wget. You must have wget installed in your system. If omitted, the script uses python requests module to downloand links
* `--type TYPE`: Choose the saving format of the links. You have to specify wich format you want: `gif`, `png`, `jpg`, ecc. If omitted the default format is `gif`.

## Tips

If you have some problem downloanding links with the default downloand method, use `--wget`, it will be helpfull.
