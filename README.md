# notebookTOC

This is a python script to generate a Table of contents from a jupyter notbook containing markdown cells.
  
## Usage
```python generate_toc.py --file NOTEBOOK [--insert]```
  
### optional arguments:  

parameter  | what it does
-----------|--------------
  `--file, -f` | filepath to notebook file for which table of contents should be generated  
  `--insert, -i` | whether to print ToC to Stdout (default) or insert at the beginning of the notebook
