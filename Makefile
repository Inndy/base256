all: gen/base256.go

selected_256.txt: bip39wordlist.txt pick_words.py
	python3 pick_words.py

gen/base256.py: selected_256.txt codegen.py
	python3 codegen.py

gen/base256.go: gen/base256.py
