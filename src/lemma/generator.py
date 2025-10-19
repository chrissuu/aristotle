from prompts import *
from model.Model import Model
from utils.Pipe import Pipe

def generate(theorem, model: Model):
    success = False
    while success:
        informal_proof_prompt = prompt_generate_informal_proof(str(theorem))
        informal_proof = model.query(prompt=informal_proof_prompt)



