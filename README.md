# pdfmergepy

A python CLI tool for merging pdfs. Requires [pdftex](https://www.tug.org/applications/pdftex/).

## Usage


```bash
usage: pdfmerge.py [-h] [-o OUTPUT_PATH] [-f FILES_TO_MERGE [FILES_TO_MERGE ...]]

Merge several pdf documents into one

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        oath to the output pdf file.
  -f FILES_TO_MERGE [FILES_TO_MERGE ...], --files-to-merge FILES_TO_MERGE [FILES_TO_MERGE ...]
                        Files to merge in the order they should appear in the output pdf.
```

```bash
python3 pdfmerge.py -f "data/sample_docs/Treaty_on_the_EU.pdf" "data/sample_docs/Treaty_on_the_functioning_of_the_EU.pdf" -o "data/EU_treaties_merged.pdf"
```