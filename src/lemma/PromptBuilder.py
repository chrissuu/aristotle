import textwrap

def clean_prompts(cls):
    for name, value in vars(cls).items():
        if isinstance(value, staticmethod):
            fn = value.__func__
            def wrapper(*args, fn=fn, **kwargs):
                result = fn(*args, **kwargs)
                return textwrap.dedent(result).strip() if isinstance(result, str) else result
            setattr(cls, name, staticmethod(wrapper))
    return cls

@clean_prompts
class PromptBuilder:

    @staticmethod
    def system_prompt():
        return f""""""

    @staticmethod
    def prompt_generate_informal_proof(theorem_statement):
        prompt = f"""
        Generate an informal proof of the following statement:

        {theorem_statement}
        """

        return prompt
    
    @staticmethod
    def prompt_generate_lemmas(informal_proof):
        prompt = f"""
        Restructure the following informal proof:

        {informal_proof}

        As a sequence of informal, short lemmas which build up to
        the final proof.

        Return your final answer as a pythonic list, separated
        by commas as such: [<lemma 1>, <lemma 2>, ..., <lemma n>]
        """

        return prompt
    
    def prompt_formalize_lemma(lemma):
        prompt = f"""
        In the Lean4 interactive theorem proving language,
        formalize the following lemma:

        {lemma}
        """

        return prompt
    
    def prompt_correct_lemma_formalization(lemma, errors, prev_formalization):
        prompt = f"""
        This formalization:

        {prev_formalization}

        For the following lemma:

        {lemma}

        Returned these errors by the Lean4 kernel.

        {errors}

        Fix the errors for the lemma formalization.
        """

        return prompt