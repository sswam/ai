from pygments.lexer import RegexLexer, bygroups
from pygments.token import Keyword, Text, Name, Operator, String

class KeyValueLexer(RegexLexer):
    """
    Lexer for key: value pair files.

    """
    name = 'Key-Value Pairs'
    aliases = ['keyvalue']
    tokens = {
        'root': [
            (r'^([a-zA-Z\-0-9\._-]*?)(: *)(.*?(\n [^\n]+)*)$',
             bygroups(Keyword, Text, String)),
        ]
    }
