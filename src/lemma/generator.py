from lemma.PromptBuilder import PromptBuilder
from lemma.TraceBuilder import TraceBuilder
from parser import *
from model.Model import Model
from utils.Pipe import Pipe
from repl.LeanRepl import LeanRepl

def generate(theorem, model: Model, repl: LeanRepl, num_retries = 10):
    pb = PromptBuilder()
    tb = TraceBuilder()
    success = False
    while success:
        gen_informal_proof_prompt = pb.prompt_generate_informal_proof(str(theorem))
        informal_proof = model.query(gen_informal_proof_prompt)
        
        gen_lemmas_prompt = pb.prompt_generate_lemmas(informal_proof)
        lemmas = model.query(gen_lemmas_prompt, extract_lemmas)

        for lemma in lemmas:
            for _ in range(num_retries):
                gen_lemma_formalization_prompt = pb.prompt_formalize_lemma(lemma)
                formalized_lemma = model.query(gen_lemma_formalization_prompt)
                success, errors = repl.type_check(formalized_lemma)