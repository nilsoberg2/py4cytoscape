# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
from datetime import date
import os
import sys
sys.path.insert(0, os.path.abspath('./..'))


# -- Project information -----------------------------------------------------

project = 'py4cytoscape'
copyright = f"2018-{date.today().year}, The Cytoscape Consortium"
author = 'Barry Demchak'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_rtd_theme',
]
# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None



# -- Options for HTML output -------------------------------------------------

import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme" # "nature" # "alabaster" # "sphinx_rtd_theme" #"classic"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'py4cytoscapedoc'



