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

// Encode encodes data as a sequence of words joined by sep.
// The separator must not contain only letters, as it may conflict with dictionary words.
func Encode(data []byte, sep string) string {
	parts := make([]string, len(data))
	for i, b := range data {
		parts[i] = wordlist[b]
	}
	return strings.Join(parts, sep)
}

// Decode decodes a phrase produced by Encode back into bytes.
// The separator must not be a substring of any dictionary word,
// so avoid using only letters as sep.
func Decode(phrase string, sep string) ([]byte, error) {
	if phrase == "" {
		return nil, nil
	}
	words := strings.Split(strings.ToLower(phrase), strings.ToLower(sep))
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
