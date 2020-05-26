#!/usr/bin/env python
import sys
import os.path

from docutils import statemachine
from docutils.utils.error_reporting import ErrorString
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.misc import Include
from sphinx.util.docutils import SphinxDirective

__version__  = '1.0'

def setup(app):
    app.add_directive("docbook-transition-include", DocBookTransitionInclude)
    return dict(
        version = __version__,
        parallel_read_safe = True,
        parallel_write_safe = True
    )

class DocBookTransitionInclude(Include, SphinxDirective):
    def parse(self, index, version):
        output = ""
        for line in open(index):
            line = line.replace("@VER@", version)
            output += line

        # For debugging the pre-rendered results...
        #print(output, file=open("/tmp/LEGACY.rst", "w"))

        self.state_machine.insert_input(
          statemachine.string2lines(output), index)

    def run(self):
        if not self.state.document.settings.file_insertion_enabled:
            raise self.warning('"%s" directive disabled.' % self.name)

        # find the index file to process
        rel_index, index = self.env.relfn2path(self.arguments[0])

        try:
            self.state.document.settings.record_dependencies.add(index)
            lines = self.parse(index, self.config.version)
        except IOError as error:
            raise self.severe('Problems with "%s" directive path:\n%s.' %
                      (self.name, ErrorString(error)))

        return []
