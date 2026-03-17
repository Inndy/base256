#!/usr/bin/env python3
import os
import textwrap

with open(os.path.join(os.path.dirname(__file__), '..', 'selected_256.txt')) as fp:
    words = fp.read().split()

assert len(words) == 256, f"Expected 256 words, got {len(words)}"


def format_wordlist_py():
    lines = []
    for i in range(0, 256, 8):
        chunk = ', '.join(f'"{w}"' for w in words[i:i+8])
        lines.append(f'    {chunk},')
    return '\n'.join(lines)


def format_wordlist_go():
    lines = []
    for i in range(0, 256, 8):
        chunk = ', '.join(f'"{w}"' for w in words[i:i+8])
        lines.append(f'\t{chunk},')
    return '\n'.join(lines)


PYTHON_TEMPLATE = textwrap.dedent('''\
    #!/usr/bin/env python3
    """BIP-39 based byte encoder/decoder (256 words)."""

    WORDLIST = [
    {wordlist}
    ]

    WORD_TO_BYTE = {{w: i for i, w in enumerate(WORDLIST)}}


    def encode(data: bytes) -> str:
        return " ".join(WORDLIST[b] for b in data)


    def decode(phrase: str) -> bytes:
        return bytes(WORD_TO_BYTE[w] for w in phrase.lower().split())


    if __name__ == "__main__":
        import sys

        if len(sys.argv) < 2 or sys.argv[1] not in ("encode", "decode"):
            print(f"Usage: {{sys.argv[0]}} encode|decode", file=sys.stderr)
            sys.exit(1)
        if sys.argv[1] == "encode":
            data = sys.stdin.buffer.read()
            print(encode(data))
        else:
            phrase = sys.stdin.read().strip()
            sys.stdout.buffer.write(decode(phrase))
''')

GO_TEMPLATE = textwrap.dedent('''\
    package base256

    var wordlist = [256]string{{
    {wordlist}
    }}
''')

py_path = os.path.join(os.path.dirname(__file__), '..', 'base256.py')
with open(py_path, 'w') as fp:
    fp.write(PYTHON_TEMPLATE.format(wordlist=format_wordlist_py()))
print(f"Generated {py_path}")

go_path = os.path.join(os.path.dirname(__file__), '..', 'wordlist.go')
with open(go_path, 'w') as fp:
    fp.write(GO_TEMPLATE.format(wordlist=format_wordlist_go()))
print(f"Generated {go_path}")
