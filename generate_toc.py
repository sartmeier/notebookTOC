import json
import re
import argparse
"""script to make Table of contents from jupter notebooks
   and prints them
"""


def argparser():
    """parse command line arguments

    Returns:
        tuple: path to notebook, print mode
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", help="file path to notebook", 
                        required=True, dest="notebook")
    parser.add_argument("--insert", "-i", help="whether to print ToC to Stdout (default) or insert into notebook", 
                        action="store_true", required=False, dest="insert")
    args = parser.parse_args()
    notebook = args.notebook
    insert = args.insert
    return notebook, insert


def load(notebook):
    """function to load jupyter notebook

    Parameters
    ----------
    notebook : string
        path to jupyter notebook

    Returns
    -------
    dict
        dict of jupyter notebook
    """
    with open(notebook, "r") as f:
        lines = json.load(f)
    return lines


def get_headers(lines):
    """extract header lines from markdown cells

    Parameters
    ----------
    lines : dict
        jupyter notebook json

    Returns
    -------
    list
        list of headers in jupyter notebook
    """
    item = lines.get("cells")
    headers = []
    for i in item:
        if i.get("cell_type") == "markdown":
            content = i.get("source")
            if not re.search("# Summary", content[0]):
                header = [h.strip() for h in content if re.match("#", h)]
                for h in header:
                    headers.append(h)
    return headers


def make_toc(headers):
    """function to make a table of contents list with properly indented headers
       and links to the sections

    Parameters
    ----------
    headers : list
        list containing all header from markdown cells

    Returns
    -------
    list
        contains properly indented markdown list elements with section links
    """
    # a table of contents string should look like this:
    # {(#-count-1)*2 spaces}- [Notes](#Notes)
    toc = ["# Summary\n", "\n"]
    for h in headers:
        header = h.split(" ")
        toc_order = header[0]
        toc_order = (len(toc_order)-1)*2
        spaces = " "*toc_order
        header_content = " ".join(header[1:])
        ref_link = "-".join(header[1:])
        toc_string = "{}- [{}](#{})\n".format(spaces, header_content, ref_link)
        toc.append(toc_string)
    return toc


def print_toc(toc, notebook=None, insert=False, path=None):
    """[summary]

    Parameters
    ----------
    toc : list
        list with ToC strings
    notebook : dict, optional
        json with notebook entries, by default None
    insert : bool, optional
        should be inserted into notebook, by default False
    path : string, optional
        output file, by default None
    """    
    if not insert:
        for t in toc:
            print(t)
    else:
        if re.search("# Summary", notebook["cells"][0]["source"][0]):
            notebook["cells"][0]["source"] = toc
        else:
            cell = {"cell_type": "markdown",
                    "metadata": {},
                    "source": toc}
            notebook["cells"].insert(0, cell)
        #print(notebook)
        with open(path, 'w') as outfile:
            json.dump(notebook, outfile)


if __name__ == '__main__':
    notebook, insert = argparser()
    cells = load(notebook)  # "Documentation.ipynb"
    doc_headers = get_headers(cells)
    contents = make_toc(doc_headers)
    if insert:
        print_toc(contents, cells, insert, notebook)
    else:
        print_toc(contents)
