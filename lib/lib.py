import inspect
import ast
import sys
import os
from random import sample
import inspect
import pprint
import json
import yaml
import contextlib
import jq
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.data import YamlLexer
from pygments.formatters import TerminalFormatter
from pygments.formatters import Terminal256Formatter
from kv import KeyValueLexer
import re
# from functools import reduce

# Directory and File Utilities ###############################################

@contextlib.contextmanager
def cd(path):
	"""Change directory to path, then change back to original directory when done."""
	old_dir = os.getcwd()
	os.chdir(path)
	try:
		yield
	finally:
		os.chdir(old_dir)

# Stack and Frame Inspection #################################################

def nth_frame(level=1):
	"""Get the nth frame from the current frame."""
	return inspect.stack()[level][0]

def caller_source(level=1):
	"""Get the source code of the caller."""
	frame = nth_frame(level=level + 1)
	return inspect.getsource(frame)

def caller_locals(level=1, copy=True):
	"""Get the local variables of the caller."""
	frame = nth_frame(level=level + 1)
	v = frame.f_locals
	if copy:
		v = v.copy()
	return v

def source_symbols(source_code):
	"""Get a list of symbols from source code."""
	ast_tree = ast.parse(source_code)

	symbols = []
	for node in ast.walk(ast_tree):
		# Extract function and method names
		if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
			symbols.append(node.name)
			# Extract function parameter names
			for arg in node.args.args:
				symbols.append(arg.arg)
		# Extract variable names from assignments
		elif isinstance(node, ast.Assign):
			for target in node.targets:
				if isinstance(target, ast.Name):
					symbols.append(target.id)
		# Extract variable names from references
		elif isinstance(node, ast.Name):
			if not isinstance(node.ctx, ast.Load):
				# Ignore words inside strings
				continue
			symbols.append(node.id)

	return symbols

def uniqo(seq):
	"""Return a list of unique elements in the order they appear in seq."""
	python_version = sys.version_info
	if python_version >= (3, 7):
		return uniq(seq)
	else:
		from collections import OrderedDict
		return list(OrderedDict.fromkeys(seq).keys())

def uniq(seq):
	"""Return a list of unique elements, not necessarily in order."""
	return list(dict.fromkeys(seq))

def shuf(seq):
	"""Return a shuffled copy of seq."""
	return sample(seq, len(seq))

def test_uniqo():
	assert uniqo([7, 7, 1, 1, 1, 3, 3, 3, 3, 2, 2]) == [7, 1, 3, 2]

def test_shuf():
	assert sorted(shuf([1, 2, 3, 4, 5])) == [1, 2, 3, 4, 5]
	max_iter = 100
	for i in range(max_iter):
		if shuf([1, 2, 3, 4, 5]) != [1, 2, 3, 4, 5]:
			break
	else:
		assert False, 'shuf() did not shuffle'

def is_256_color_terminal():
	"""Return True if the terminal supports 256 colors."""
	if os.environ.get('TERM') == 'xterm-256color':
		return True
	elif os.environ.get('COLORTERM') == 'truecolor':
		return True
	elif '256color' in os.environ.get('TERM'):
		return True
	else:
		return False

def is_primitive_type(obj):
	"""Return True if obj is a primitive type."""
	return isinstance(obj, (int, float, str, bytes, bool, type(None)))

def simple_primitive_type(obj):
	return is_primitive_type(obj) and "," not in repr(obj)

def kv_dump_generator(obj, squash_tuples=True, squash_lists=False):
	"""Dump an object as key-value pairs."""

	squashable = squash_tuples and isinstance(obj, tuple) or squash_lists and isinstance(obj, list)

	if isinstance(obj, str):
		yield obj
	elif is_primitive_type(obj):
		yield repr(obj)
	elif squashable and all(simple_primitive_type(item) for item in obj):
		yield ", ".join(str(item) for item in obj)
	elif isinstance(obj, (list, tuple)):
		for item in obj:
			yield from kv_dump_generator(item)
	elif isinstance(obj, dict):
		for key, value in obj.items():
			value_text = kv_dump(value)
			value_text = re.sub(r'\n(.)', '\n \\1', value_text)
			value_text = value_text.rstrip('\n')
			yield f'{key}: {value_text}'
	else:
		yield repr(obj)

def kv_dump(obj):
	"""Dump an object as key-value pairs."""
	text = ''
	for line in kv_dump_generator(obj):
		text += line + '\n'
	return text

def dump(printme, format='kv', color=None, Formatter=None, style='monokai'):
	"""Print printme in the specified format."""
	if color is None:
		color = sys.stderr.isatty()
	if Formatter is None:
		Formatter = Terminal256Formatter if is_256_color_terminal() else TerminalFormatter
	if format == 'python':
		text = pprint.pformat(printme)
		Lexer = PythonLexer
	elif format == 'json':
		text = json.dumps(printme, indent=4)
		Lexer = JsonLexer
	elif format == 'yaml':
		text = yaml.dump(printme, sort_keys=False)
		Lexer = YamlLexer
	elif format == 'kv':
		text = kv_dump(printme)
		Lexer = KeyValueLexer
	else:
		return None
	if color:
		text = highlight(text, Lexer(), Formatter(style=style))
	return text

def eprint(*args, **kwargs):
	"""Print to stderr."""
	print(*args, file=sys.stderr, **kwargs)

def show_locals(exclude=None, locals_now=None, format='kv', color=None, level=1):
	"""Print the local variables of the caller in order."""
	level += 1
	locals_now = locals_now or caller_locals(level=level)
	src = caller_source(level=level)
	caller_symbols_in_order = source_symbols(src)
	if exclude is None:
		exclude = {}
	printme = {}
	for key in caller_symbols_in_order:
		if key not in locals_now or key in printme:
			continue
		value = locals_now[key]
		if key.startswith('_') or key in exclude and value == exclude[key]:
			continue
		printme[key] = value
	if format is not None:
		eprint(dump(printme, format=format, color=color))
	return printme

def quarto_post_date(post_file):
	"""Get the date of a quarto post."""
	with open(post_file) as f:
		text = f.read()
	metadata = jq.compile('.cells[] | select(.cell_type == "raw") | .source | join("")').input(text=text).first()
	match = re.search(r'^date: "(.*?)"$', metadata, re.MULTILINE)
	if not match:
		raise Exception('no date found in post metadata for ' + post_file)
	date = match.group(1)
	return date
