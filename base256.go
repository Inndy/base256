package base256

import "strings"

type ErrUnknownWord string

func (e ErrUnknownWord) Error() string {
	return "unknown word: " + string(e)
}

var wordToByte map[string]byte

func init() {
	wordToByte = make(map[string]byte, 256)
	for i, w := range wordlist {
		wordToByte[w] = byte(i)
	}
}

func Encode(data []byte) string {
	parts := make([]string, len(data))
	for i, b := range data {
		parts[i] = wordlist[b]
	}
	return strings.Join(parts, " ")
}

func Decode(phrase string) ([]byte, error) {
	words := strings.Fields(strings.ToLower(phrase))
	result := make([]byte, len(words))
	for i, w := range words {
		b, ok := wordToByte[w]
		if !ok {
			return nil, ErrUnknownWord(w)
		}
		result[i] = b
	}
	return result, nil
}
