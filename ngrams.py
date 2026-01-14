with open("data/ebuds/ebuds.txt", "r") as file:
    lines = file.readlines()
    texts = [line.split() for line in lines]

def ngram_frequencies(n, texts):
    ngram_freqs = {}
    for text in texts:
        if len(text) < n:
            continue
        
        i = 0
        while i+n <= len(text):
            current_gram = text[i:i+n]
            current_gram = " ".join(current_gram)
            if current_gram not in ngram_freqs:
                ngram_freqs[current_gram] = 0
            ngram_freqs[current_gram] += 1
            i += 1
    return ngram_freqs

print(sorted(ngram_frequencies(1, texts).items(), key=lambda x: x[1], reverse=True)[:10])
print(sorted(ngram_frequencies(2, texts).items(), key=lambda x: x[1], reverse=True)[:10])
print(sorted(ngram_frequencies(3, texts).items(), key=lambda x: x[1], reverse=True)[:10])