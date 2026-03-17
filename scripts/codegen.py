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

    import "strings"

    type ErrUnknownWord string

    func (e ErrUnknownWord) Error() string {{
    \treturn "unknown word: " + string(e)
    }}

    var wordlist = [256]string{{
    {wordlist}
    }}

    var wordToByte map[string]byte

    func init() {{
    \twordToByte = make(map[string]byte, 256)
    \tfor i, w := range wordlist {{
    \t\twordToByte[w] = byte(i)
    \t}}
    }}

    func Encode(data []byte) string {{
    \tparts := make([]string, len(data))
    \tfor i, b := range data {{
    \t\tparts[i] = wordlist[b]
    \t}}
    \treturn strings.Join(parts, " ")
    }}

    func Decode(phrase string) ([]byte, error) {{
    \twords := strings.Fields(strings.ToLower(phrase))
    \tresult := make([]byte, len(words))
    \tfor i, w := range words {{
    \t\tb, ok := wordToByte[w]
    \t\tif !ok {{
    \t\t\treturn nil, ErrUnknownWord(w)
    \t\t}}
    \t\tresult[i] = b
    \t}}
    \treturn result, nil
    }}
''')

py_path = os.path.join(os.path.dirname(__file__), '..', 'base256.py')
with open(py_path, 'w') as fp:
    fp.write(PYTHON_TEMPLATE.format(wordlist=format_wordlist_py()))
print(f"Generated {py_path}")

go_path = os.path.join(os.path.dirname(__file__), '..', 'base256.go')
with open(go_path, 'w') as fp:
    fp.write(GO_TEMPLATE.format(wordlist=format_wordlist_go()))
print(f"Generated {go_path}")
