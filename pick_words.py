import numpy as np
from itertools import combinations
from collections import Counter

FIRST_CHAR_BONUS = 3
LENGTH_PENALTY = 0.3
MIN_RAW_EDIT_DISTANCE = 2

def weighted_edit_distance(a, b):
    d = edit_distance(a, b)
    if a[0] != b[0]:
        d += FIRST_CHAR_BONUS
    return d

def edit_distance(a, b):
    la, lb = len(a), len(b)
    dp = list(range(lb + 1))
    for i in range(1, la + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, lb + 1):
            tmp = dp[j]
            if a[i-1] == b[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j-1])
            prev = tmp
    return dp[lb]

with open('bip39wordlist.txt') as fp:
    words = fp.read().split()

n = len(words)
print(f"Total words: {n}")
print(f"Computing pairwise weighted edit distances (first-char bonus={FIRST_CHAR_BONUS})...")

raw_dist = np.zeros((n, n), dtype=np.int8)
dist = np.zeros((n, n), dtype=np.int8)
for i in range(n):
    for j in range(i + 1, n):
        rd = edit_distance(words[i], words[j])
        raw_dist[i][j] = rd
        raw_dist[j][i] = rd
        d = rd + (FIRST_CHAR_BONUS if words[i][0] != words[j][0] else 0)
        dist[i][j] = d
        dist[j][i] = d

length_penalty = np.array([len(words[i]) * LENGTH_PENALTY for i in range(n)])

print(f"Selecting 256 words with greedy max-min approach (length_penalty={LENGTH_PENALTY})...")

best_pair = max(combinations(range(n), 2), key=lambda p: dist[p[0]][p[1]] - length_penalty[p[0]] - length_penalty[p[1]])
selected = list(best_pair)

min_dist_to_selected = np.minimum(dist[selected[0]].astype(float), dist[selected[1]].astype(float))

min_raw_dist_to_selected = np.minimum(raw_dist[selected[0]].astype(float), raw_dist[selected[1]].astype(float))

for k in range(2, 256):
    min_dist_to_selected[selected] = -999
    min_raw_dist_to_selected[selected] = -999
    score = min_dist_to_selected - length_penalty
    score[min_raw_dist_to_selected < MIN_RAW_EDIT_DISTANCE] = -999
    best = int(np.argmax(score))
    selected.append(best)
    min_dist_to_selected = np.minimum(min_dist_to_selected, dist[best].astype(float))
    min_raw_dist_to_selected = np.minimum(min_raw_dist_to_selected, raw_dist[best].astype(float))
    if k % 50 == 0:
        mask = min_dist_to_selected > -999
        cur_min = min_dist_to_selected[mask].min() if np.any(mask) else 0
        print(f"  {k}/256 selected, current min edit distance among candidates: {cur_min:.1f}")

selected_words = sorted([words[i] for i in selected])

min_d = 999
min_raw_d = 999
for i in range(len(selected)):
    for j in range(i+1, len(selected)):
        d = dist[selected[i]][selected[j]]
        rd = edit_distance(selected_words[i], selected_words[j])
        if d < min_d:
            min_d = d
        if rd < min_raw_d:
            min_raw_d = rd

print(f"\nMinimum pairwise weighted edit distance: {min_d}")
print(f"Minimum pairwise raw edit distance: {min_raw_d}")

first_char_dist = Counter(w[0] for w in selected_words)
avg_len = sum(len(w) for w in selected_words) / len(selected_words)
avg_len_all = sum(len(w) for w in words) / len(words)
print(f"\nAvg word length: {avg_len:.1f} (full list: {avg_len_all:.1f})")

print(f"\nFirst-char distribution ({len(first_char_dist)} unique letters):")
for ch in sorted(first_char_dist):
    print(f"  {ch}: {first_char_dist[ch]}")

print(f"\nSelected {len(selected_words)} words:\n")

with open('selected_256.txt', 'w') as fp:
    for w in selected_words:
        fp.write(w + '\n')
