package base256

import "strings"

type ErrUnknownWord string

func (e ErrUnknownWord) Error() string {
	return "unknown word: " + string(e)
}

var wordlist = [256]string{
	"abandon", "ability", "abstract", "account", "acquire", "actress", "adapt", "advance",
	"aerobic", "afford", "agree", "album", "already", "amazing", "analyst", "annual",
	"another", "approve", "attitude", "axis", "bachelor", "balance", "bar", "become",
	"begin", "benefit", "biology", "blossom", "blush", "bright", "broccoli", "buddy",
	"buffalo", "business", "cabin", "canvas", "category", "ceiling", "champion", "charge",
	"check", "chronic", "cigar", "cinnamon", "cliff", "coast", "concert", "convince",
	"cotton", "crumble", "crystal", "culture", "cup", "cupboard", "curious", "daughter",
	"defense", "denial", "deposit", "describe", "diamond", "differ", "dilemma", "dinosaur",
	"display", "divorce", "document", "dog", "dolphin", "drastic", "easily", "economy",
	"edge", "effort", "element", "elevator", "embrace", "empower", "envelope", "episode",
	"eternal", "evidence", "exercise", "exhaust", "exotic", "eyebrow", "faculty", "famous",
	"fashion", "favorite", "fee", "festival", "finish", "follow", "forward", "fragile",
	"frequent", "garbage", "gather", "general", "gesture", "giggle", "goddess", "gorilla",
	"gossip", "gravity", "gym", "hamster", "harvest", "health", "hedgehog", "hip",
	"hockey", "hospital", "hundred", "identify", "illegal", "impulse", "indicate", "injury",
	"install", "interest", "iron", "jaguar", "jealous", "jewel", "job", "journey",
	"kangaroo", "ketchup", "kitten", "know", "language", "laptop", "laundry", "leaf",
	"lecture", "liberty", "liquid", "lobster", "lyrics", "magnet", "material", "maximum",
	"mechanic", "mesh", "middle", "midnight", "million", "monster", "mosquito", "mountain",
	"multiply", "mushroom", "name", "negative", "neglect", "network", "neutral", "nothing",
	"obey", "obscure", "obvious", "office", "olympic", "opinion", "orchard", "original",
	"outdoor", "panther", "peasant", "physical", "picture", "pill", "pledge", "popular",
	"position", "possible", "problem", "property", "pudding", "purchase", "pyramid", "quantum",
	"question", "quiz", "rack", "rebuild", "reform", "remember", "response", "retreat",
	"ribbon", "runway", "sad", "satisfy", "school", "scorpion", "security", "seminar",
	"sentence", "shallow", "shrimp", "shuffle", "silver", "sketch", "slight", "someone",
	"sponsor", "squirrel", "strategy", "student", "success", "surprise", "surround", "sustain",
	"symptom", "talent", "tennis", "thought", "tissue", "tobacco", "toddler", "tomorrow",
	"tortoise", "traffic", "trumpet", "try", "tuition", "typical", "umbrella", "unaware",
	"undo", "unhappy", "unusual", "useless", "utility", "valley", "vehicle", "verb",
	"vicious", "visual", "volcano", "walnut", "warfare", "way", "weather", "wedding",
	"welcome", "window", "world", "yard", "yellow", "young", "zebra", "zoo",
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
