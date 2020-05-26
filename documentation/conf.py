# Configuration file for the Sphinx documentation builder.
#
# SPDX-License-Identifier: CC-BY-2.0-UK
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import datetime
import re

current_version = "dev"

# String used in sidebar
version = 'Version: ' + current_version
if current_version == 'dev':
    version = 'Version: Current Development'
# Version seen in documentation_options.js and hence in js switchers code
release = current_version

# -- Project information -----------------------------------------------------
project = 'The Yocto Project'
copyright = '2010-%s, The Linux Foundation' % datetime.datetime.now().year
author = 'The Linux Foundation'

# -- General configuration ---------------------------------------------------

# to load local extension from the folder 'sphinx'
sys.path.insert(0, os.path.abspath('sphinx'))

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'docbook-transition'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'transition/*/*.rst', 'transition/*.rst']

# master document name. The default changed from contents to index. so better
# set it ourselves.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_logo = 'sphinx-static/YoctoProject_Logo_RGB.jpg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['sphinx-static']

html_context = {
    'css_files': [
        '_static/theme_overrides.css',
    ],
    'current_version': current_version,
}

# For legacy/transition docs, we need to set the version, and we do
# that here, using the 'folder' name where the project sources are.
def setup(app: "Sphinx"):
    def change(app, config):
        version = re.search(".*/transition/([\d.]+)$", app.srcdir)
        if version is not None:
            config.version = version.group(1)
            config.release = config.version

    app.connect('config-inited', change)
