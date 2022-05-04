from subprocess import check_output
from tempfile import mkdtemp
import os
import argparse
import sys
import shutil
from typing import Tuple


def parse_args() -> argparse.Namespace:
    """argument parser"""

    ## parse CLI args
    parser = argparse.ArgumentParser(
        prog="pdfmerge.py",
        description="Merge several pdf documents into one",
    )

    parser.add_argument(
        "-o",
        "--output-path",
        type=str,
        dest="output_path",
        default=None,
        help="oath to the output pdf file.",
    )

    # parser.add_argument(
    #         "-f",
    #         "--force-creation",
    #         dest="force_creation",
    #         action="store_true",
    #         default=False,
    #         help="Should it create the annotation projects?",
    #     )

    parser.add_argument(
        "-f",
        "--files-to-merge",
        dest="files_to_merge",
        nargs="+",
        type=str,
        help="Files to merge in the order they should appear in the output pdf.",
    )

    # parse. If no args display the "help menu"
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()


def _make_tex(
    pdf_paths_list: list = [
        '"/home/jr/Dropbox/CV, C. Motiv. cartas de recomendação/wetransfer_doc005-pdf_2022-05-04_0701/DOC001.pdf"',
        '"/home/jr/Dropbox/CV, C. Motiv. cartas de recomendação/wetransfer_doc005-pdf_2022-05-04_0701/DOC000.pdf"',
    ]
) -> str:
    """Make the tex file"""
    to_insert = "\n".join(["\includepdf[pages=-]{" + _ + "}" for _ in pdf_paths_list])
    # insert them in the tex file
    prefix = """
    \\documentclass{article}
    \\usepackage{pdfpages}
    \\begin{document}
    """
    suffix = """
    \\end{document}
    """
    return "\n".join([prefix, to_insert, suffix])


def make_tex(tex_dir: str, **kwargs) -> str:
    """Make the tex file and store in temp dir"""
    tex = _make_tex(**kwargs)
    texfile = os.path.join(tex_dir, "to_merge.tex")
    with open(texfile, "w+") as tf:
        tf.write(tex)
    return texfile


def make_pdf(tex_path: str, temp_output_dir: str) -> Tuple[str, str]:
    """Make a pdf doc with a tex file"""
    check_output(
        ["pdflatex", f"-output-directory={temp_output_dir}", tex_path], timeout=120
    )
    return temp_output_dir, os.path.join(temp_output_dir, "to_merge.pdf")


def main() -> None:
    args = parse_args()
    input_files_raw = args.files_to_merge
    # copy the input files to a tmp dir for avoiding path issues with tex
    tex_dir = mkdtemp()
    input_files = []
    for input_file in input_files_raw:
        base_name = input_file.split("/")[-1]
        new_name = os.path.join(tex_dir, base_name)
        shutil.copy(src=input_file, dst=new_name)
        input_files.append(new_name)
    # prepare the merge tex
    tex_path = make_tex(pdf_paths_list=input_files, tex_dir=tex_dir)
    # make the pdf
    output_file = args.output_path.split("/")[-1]
    pdf_tmp_dir, pdf_path = make_pdf(
        tex_path=tex_path, temp_output_dir=tex_dir
    )
    # copy
    shutil.copy(src=pdf_path, dst=args.output_path)
    # delete tempdir
    shutil.rmtree(pdf_tmp_dir)
    print(f"[+] The files were merged into: {args.output_path}")


if __name__ == "__main__":
    main()
