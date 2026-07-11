import re


def split_into_sentences(text: str) -> list[str]:
    """
    Splits text into sentences using basic punctuation rules.
    Not perfect (won't handle every edge case like 'Dr. Smith'),
    but good enough for chunking purposes.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, target_size: int = 500, overlap_sentences: int = 1) -> list[str]:
    """
    Groups sentences into chunks up to target_size characters.
    Each chunk overlaps with the previous one by `overlap_sentences`
    sentences, so context isn't lost at chunk boundaries.

    target_size: soft max character length per chunk
    overlap_sentences: how many trailing sentences to repeat at the
                        start of the next chunk
    """
    sentences = split_into_sentences(text)
    if not sentences:
        return []

    chunks = []
    current_chunk_sentences = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)

        # If adding this sentence would exceed target_size, close the chunk
        if current_length + sentence_length > target_size and current_chunk_sentences:
            chunks.append(" ".join(current_chunk_sentences))

            # Start next chunk with overlap from the end of the previous one
            overlap = current_chunk_sentences[-overlap_sentences:] if overlap_sentences > 0 else []
            current_chunk_sentences = overlap.copy()
            current_length = sum(len(s) for s in current_chunk_sentences)

        current_chunk_sentences.append(sentence)
        current_length += sentence_length

    # Add the final chunk if anything's left
    if current_chunk_sentences:
        chunks.append(" ".join(current_chunk_sentences))

    return chunks