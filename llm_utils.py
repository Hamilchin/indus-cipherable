
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


one_gram_freqs = ngram_frequencies(1, texts)
two_gram_freqs = ngram_frequencies(2, texts)
three_gram_freqs = ngram_frequencies(3, texts)

def top_n(freqs, n):
    top_items = sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:n]
    return dict(top_items)

domain_of_interest = set(top_n(two_gram_freqs, 2).keys()) | set(top_n(three_gram_freqs, 1).keys())
symbols_in_doi = sorted(set(word for item in domain_of_interest for word in item.split()), key=lambda x: int(x))
print(" ".join(symbols_in_doi)) 

