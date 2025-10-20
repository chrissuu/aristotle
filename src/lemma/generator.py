from lemma.PromptBuilder import PromptBuilder
from lemma.TraceBuilder import TraceBuilder
from parser import *
from model.Model import Model
from utils.Pipe import Pipe
from wrapper.LeanClient import LeanClient

def find_unformalized_lemmas(lemmas, formalized_lemmas) -> list[str]:
    unformalized_lemmas = []
    formalized_lemma_indices = set(k for (k, lemma) in formalized_lemmas)
    for i in range(len(lemmas)):
        if not i in formalized_lemma_indices:
            unformalized_lemmas.append(lemmas[i])
    return unformalized_lemmas

def formalize_lemma(
    lemma: str, 
    model: Model, 
    client: LeanClient,
    pb: PromptBuilder,
    num_lemma_formalization_retries: int
):
    gen_lemma_formalization_prompt = pb.formalize_lemma(lemma)
    formalized_lemma = model.query(gen_lemma_formalization_prompt)
    lemma_formalization_success, errors = client.check(formalized_lemma)
    for _ in range(num_lemma_formalization_retries - 1):
        if not lemma_formalization_success:
            correct_lemma_form_prompt = pb.correct_lemma_formalization(
                lemma,
                errors,
                formalized_lemma
            )
            formalized_lemma = model.query(correct_lemma_form_prompt)
            lemma_formalization_success, errors = client.check(formalized_lemma)
    
    return formalized_lemma if lemma_formalization_success else None

def generate(
    theorem, 
    model: Model, 
    client: LeanClient, 
    num_lemma_rewrite_retries = 3,
    num_lemma_formalization_retries = 10
    ):

    pb = PromptBuilder()

    gen_informal_proof_prompt = pb.generate_informal_proof(str(theorem))
    informal_proof = model.query(gen_informal_proof_prompt)
        
    gen_lemmas_prompt = pb.generate_lemmas(informal_proof)
    lemmas = model.query(gen_lemmas_prompt, extract_lemmas)
    formalized_lemmas_with_indices : list[tuple[int, str]] = []

    for i, lemma in enumerate(lemmas):
        lemma_opt = formalize_lemma(
            lemma,
            model,
            client,
            pb,
            num_lemma_formalization_retries
        )
        if lemma_opt:
            formalized_lemmas_with_indices.append((i, lemma_opt))

    unformalized_lemmas = find_unformalized_lemmas(lemmas, formalized_lemmas_with_indices)
    formalized_lemmas = list(map(lambda e : e[1], formalized_lemmas_with_indices))

    for i in range(num_lemma_rewrite_retries):
        if unformalized_lemmas:
            gen_revised_lemmas_prompt = pb.revise_lemmas(theorem, lemmas, formalized_lemmas, unformalized_lemmas)
            revised_lemmas = model.query(gen_revised_lemmas_prompt, extract_lemmas)
            formalized_lemmas_with_indices : list[tuple[int, str]] = []

            for i, lemma in enumerate(revised_lemmas):
                lemma_opt = formalize_lemma(
                    lemma,
                    model,
                    client,
                    pb,
                    num_lemma_formalization_retries
                )
                if lemma_opt:
                    formalized_lemmas_with_indices.append((i, lemma_opt))

            unformalized_lemmas = find_unformalized_lemmas(revised_lemmas, formalized_lemmas_with_indices)
            formalized_lemmas.extend(list(map(lambda e : e[1], formalized_lemmas_with_indices)))

    return formalized_lemmas