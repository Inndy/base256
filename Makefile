all: base256.go

selected_256.txt: bip39wordlist.txt scripts/pick_words.py
	python3 scripts/pick_words.py

base256.py: selected_256.txt scripts/codegen.py
	python3 scripts/codegen.py

base256.go: base256.py
