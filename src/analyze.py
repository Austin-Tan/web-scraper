from collections import Counter


def prune_tokens(
    url_to_tokens: dict[str, dict[str, int]],
    threshold: float = 0.8,
    max_keywords: int = 10,
):
    """
    url_to_tokens: mapping of URL -> dict(token -> count)
    threshold: fraction of sites a word can appear in before being considered 'too common'
    max_keywords: max number of keywords per URL (excluding the top 'product name')

    Returns: dict[url] = {'product_type': str, 'keywords': list[str]}
    """
    num_sites = len(url_to_tokens)

    # Count how many URLs each word appears in
    word_site_counts = Counter()
    for tokens in url_to_tokens.values():
        word_site_counts.update(tokens.keys())

    # Log top 20 most frequent words across sites
    print("Top words across all sites:")
    for word, count in word_site_counts.most_common(20):
        print(f"{word}: {count} / {num_sites} sites ({count / num_sites:.2%})")

    # Identify 'too common' words
    too_common = {
        word
        for word, count in word_site_counts.items()
        if count / num_sites >= threshold
    }

    # Prune and select top words per URL
    urls_to_keywords = {}
    for url, tokens in url_to_tokens.items():
        # Remove too-common words
        pruned_tokens = {
            word: freq for word, freq in tokens.items() if word not in too_common
        }

        if not pruned_tokens:
            # fallback if everything pruned
            pruned_tokens = tokens.copy()

        # Sort by frequency descending
        sorted_tokens = sorted(
            pruned_tokens.items(), key=lambda item: item[1], reverse=True
        )
        sorted_words = [word for word, freq in sorted_tokens]

        # Assign product_type (most unique/prevalent)
        product_type = sorted_words[0] if sorted_words else ""

        # Assign keywords (next N words)
        keywords = sorted_words[1 : max_keywords + 1] if len(sorted_words) > 1 else []

        urls_to_keywords[url] = {"product_type": product_type, "keywords": keywords}

    return urls_to_keywords
