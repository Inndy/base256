package base256_test

import (
	"bytes"
	"errors"
	"strings"
	"testing"

	base256 "go.inndy.tw/base256"
)

func TestRoundTrip(t *testing.T) {
	tests := [][]byte{
		{},
		{0},
		{255},
		{0, 127, 255},
		[]byte("hello"),
	}
	for _, data := range tests {
		encoded := base256.Encode(data, " ")
		decoded, err := base256.Decode(encoded, " ")
		if err != nil {
			t.Errorf("Decode(Encode(%v)) error: %v", data, err)
			continue
		}
		if !bytes.Equal(data, decoded) {
			t.Errorf("Decode(Encode(%v)) = %v", data, decoded)
		}
	}
}

func TestRoundTripAllBytes(t *testing.T) {
	data := make([]byte, 256)
	for i := range data {
		data[i] = byte(i)
	}
	decoded, err := base256.Decode(base256.Encode(data, " "), " ")
	if err != nil {
		t.Fatalf("round trip error: %v", err)
	}
	if !bytes.Equal(data, decoded) {
		t.Fatal("round trip mismatch for all 256 byte values")
	}
}

func TestEncodeWordCount(t *testing.T) {
	data := make([]byte, 10)
	encoded := base256.Encode(data, " ")
	words := strings.Split(encoded, " ")
	if len(words) != 10 {
		t.Errorf("Encode produced %d words, want 10", len(words))
	}
}

func TestDecodeUnknownWord(t *testing.T) {
	_, err := base256.Decode("notaword", " ")
	if err == nil {
		t.Fatal("expected error for unknown word")
	}
	var target base256.ErrUnknownWord
	if !errors.As(err, &target) {
		t.Fatalf("expected ErrUnknownWord, got %T", err)
	}
	if string(target) != "notaword" {
		t.Errorf("ErrUnknownWord = %q, want %q", target, "notaword")
	}
}

func TestDecodeCaseInsensitive(t *testing.T) {
	data := []byte{0, 1, 2}
	encoded := base256.Encode(data, " ")

	upper := ""
	for _, c := range encoded {
		if c >= 'a' && c <= 'z' {
			upper += string(c - 32)
		} else {
			upper += string(c)
		}
	}

	decoded, err := base256.Decode(upper, " ")
	if err != nil {
		t.Fatalf("Decode uppercase error: %v", err)
	}
	if !bytes.Equal(data, decoded) {
		t.Errorf("Decode uppercase = %v, want %v", decoded, data)
	}
}

func TestEncodeEmpty(t *testing.T) {
	if got := base256.Encode(nil, " "); got != "" {
		t.Errorf("Encode(nil) = %q, want empty", got)
	}
}

func TestDecodeEmpty(t *testing.T) {
	decoded, err := base256.Decode("", " ")
	if err != nil {
		t.Fatalf("Decode empty error: %v", err)
	}
	if len(decoded) != 0 {
		t.Errorf("Decode empty = %v, want empty", decoded)
	}
}
