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
    def generate_informal_proof(theorem_statement):
        prompt = f"""
        Generate an informal proof of the following statement:

        {theorem_statement}
        """

        return prompt
    
    @staticmethod
    def generate_lemmas(informal_proof):
        prompt = f"""
        Restructure the following informal proof:

        {informal_proof}

        As a sequence of informal, short, and more importantly,
        standalone lemmas which build up to the final proof.

        Return your final answer as a pythonic list, separated
        by commas as such: [<lemma 1>, <lemma 2>, ..., <lemma n>]

        The last lemma should be the informal proof of the theorem,
        describing how to coalesce the lemmas that you've developed 
        along the way.
        """

        return prompt
    
    def formalize_lemma(lemma):
        prompt = f"""
        In the Lean4 interactive theorem proving language,
        formalize the following lemma:

        {lemma}
        """

        return prompt
    
    def correct_lemma_formalization(lemma, errors, prev_formalization):
        prompt = f"""
        For the following lemma:

        {lemma}
        
        This formalization:

        {prev_formalization}

        Returned these errors by the Lean4 kernel.

        {errors}

        Fix the errors for the lemma formalization.
        """

        return prompt

    def revise_lemmas(
        theorem,
        informal_proof,
        lemmas, 
        formalized_lemmas, 
        unsuccessful_lemmas
        ):
        """
        Args:
            theorem: the original theorem
            lemmas: the (to-be-formalized) lemmas which the model originally generated
            formalized_lemmas: the successfully formalized lemmas produced by the model
            unformalized_lemmas: 
        """
        original_lemmas_block: str = "\n".join(
            f"Original lemma {i}: {lemmas[i]}" for i in range(len(lemmas))
        )

        formalized_lemmas_block: str = "\n".join(
            f"Succesfully formalized lemma {i}: {formalized_lemmas[i]}" for i in range(len(formalized_lemmas))
        )

        unsuccessful_lemmas_block: str = "\n".join(
            f"Unformalized lemma {i}: {unsuccessful_lemmas[i]}" for i in range(len(unsuccessful_lemmas))
        )

        prompt = f"""
        While attempting to prove the following theorem:

        {theorem}

        We first considered this approach:

        {informal_proof}

        and generated these lemmas as short building
        blocks towards the final proof:

        {original_lemmas_block}

        We were able to successfully formalize some of these
        lemmas to:

        {formalized_lemmas_block}

        But were unsuccessful in formalizing these lemmas:

        {unsuccessful_lemmas_block}

        Broadly speaking, the original attempt will have failed 
        for a combination of the following two reasons. First,
        the original proof, or at least the portion that was not 
        proved, may follow an unworkable strategy which
        needs to be fundamentally altered. And second, the strategy
        may have been sound but not broken down into sufficiently 
        granular lemmas for the search algorithm to prove them directly. 

        Propose a new set of lemmas in natural language, which either use the 
        formalized lemmas and builds on top of them, or constructs new ones.

        Return your final answer as a pythonic list, separated
        by commas as such: [<lemma 1>, <lemma 2>, ..., <lemma n>]
        
        The last lemma should be the informal proof of the theorem,
        describing how to coalesce the lemmas that you've developed 
        along the way.
        """

        return prompt
