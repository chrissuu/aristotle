import ast
from typing import Optional, List

def extract_lemmas(output: str) -> Optional[List[str]]:
    """
    Safely extract a Python list of lemma strings from model output.

    Expected output format:
        [<lemma 1>, <lemma 2>, ..., <lemma n>]

    Returns:
        list of strings if valid, else None.
    """
    if not isinstance(output, str):
        return None

    start = output.find('[')
    end = output.rfind(']')
    if start == -1 or end == -1 or start > end:
        return None

    candidate = output[start:end+1]

    try:
        parsed = ast.literal_eval(candidate)
        if isinstance(parsed, list) and all(isinstance(x, str) for x in parsed):
            return parsed
    except Exception:
        return None

    return None
