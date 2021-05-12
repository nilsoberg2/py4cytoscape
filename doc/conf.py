# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
from datetime import date
import os
import sys
sys.path.insert(0, os.path.abspath('./..'))

# This is here as a signal to decorators in py4cytoscape. They should return
# the decorated function instead of the function wrapper they normally would.
# This allows AutoDoc to pick up the function signatures as defined so they
# don't need to be manually generated in the *.rst files.
os.environ['SPHINX_BUILD'] = 'TRUE'


# -- Project information -----------------------------------------------------

project = 'py4cytoscape'
copyright = f"2018-{date.today().year}, The Cytoscape Consortium"
author = 'Barry Demchak'

import py4cytoscape
# The short X.Y version
version = py4cytoscape.__version__
# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
##extensions = [
##    'sphinx.ext.autodoc',
##    'sphinx.ext.napoleon',
##    'sphinx.ext.autosummary',
##    'sphinx_autodoc_typehints',
##    "sphinx.ext.viewcode",
##    'sphinx_rtd_theme',
##    'nbsphinx',
##    'sphinx.ext.autosectionlabel',
##]
# If true, the current module name will be prepended to all description
# unit titles (such as .. function::) in autodoc
add_module_names = False
# if True, gets function signatures added to docstring
napoleon_use_param = True
# If true, generates autosummaries
autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', '_templates']

# The name of the Pygments (syntax highlighting) style to use.
##pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# [BD] Alabaster is the default, but is too white, so I commented out: html_theme = 'alabaster'
# Note that this means we can also comment out certain CSS (located in _static/css)
# import sphinx_rtd_theme
# html_theme = "sphinx_rtd_theme"
html_theme = "classic" # "alabaster" # "sphinx_rtd_theme" #"classic"
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# [BD] from http://stackoverflow.com/questions/32079200/how-do-i-set-up-custom-styles-for-restructuredtext-sphinx-readthedocs-etc/32079202#32079202
##html_logo = '_static/images/cytoscape3-icon-trans-128x128.png'
##html_favicon = '_static/images/cytoscape3-icon.ico'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
##html_theme_options = {
##    'prev_next_buttons_location': 'both',
##    'navigation_depth': 3,
##    'style_external_links': True,
##}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'py4cytoscapedoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'py4cytoscape.tex', 'py4cytoscape Documentation',
     'The Cytoscape Consortium', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'py4cytoscape', 'py4cytoscape Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'py4cytoscape', 'py4cytoscape Documentation',
     author, 'py4cytoscape', 'Python interface to Cytoscape CyREST',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# Add the 'copybutton' javascript, to hide/show the prompt in code examples
##def setup(app):
##    app.add_js_file("copybutton.js")
