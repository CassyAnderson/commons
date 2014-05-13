import ast
import re

from ..common import CheckstylePlugin


class PrintStatements(CheckstylePlugin):
  """Enforce the use of print as a function and not a statement."""

  FUNCTIONY_EXPRESSION = re.compile(r'^\s*\(.*\)\s*$')

  def nits(self):
    for print_stmt in self.iter_ast_types(ast.Print):
      # In Python 3.x and in 2.x with __future__ print_function, prints show up as plain old
      # function expressions.  ast.Print does not exist in Python 3.x.  However, allow use
      # syntactically as a function, i.e. ast.Print but with ws "(" .* ")" ws
      logical_line = ''.join(self.python_file[print_stmt.lineno])
      print_offset = logical_line.index('print')
      stripped_line = logical_line[print_offset + len('print'):]
      if not self.FUNCTIONY_EXPRESSION.match(stripped_line):
        yield self.error('T607', 'Print used as a statement.', print_stmt)
