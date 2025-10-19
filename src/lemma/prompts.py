def system_prompt():
    return f""""""

def prompt_generate_informal_proof(theorem_statement):
    return f"""
Generate an informal proof of the following statement:

{theorem_statement}
"""
    
def prompt_generate_lemmas(informal_proof):
    return f"""
Restructure the following informal proof:

{informal_proof}

As a sequence of lemmas which build up to
the final proof.

Return the answer as a pythonic list, separated
by commas as such: [<lemma 1>, <lemma 2>, ..., <lemma n>]
"""
    
def prompt_formalize_lemma(lemma):
    return f"""
In the Lean4 interactive theorem proving language,
formalize the following lemma:

{lemma}
"""
    
def prompt_correct_lemma_formalization(lemma, errors, prev_formalization):
    return f"""
This formalization:

{prev_formalization}

For the following lemma:

{lemma}

Returned these errors by the Lean4 kernel.

{errors}

Fix the errors for the lemma formalization.
"""