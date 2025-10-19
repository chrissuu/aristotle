class Model:
    def __init__(self, query_fn, system_prompt = ""):
        self.query_fn = query_fn
        self.system_prompt = system_prompt

    def query(
        self, 
        prompt,
        response_validator = id,
        response_extractor = id
    ) -> str | None:
        """
        query

        Args:
            prompt: str
            response_validator: str -> bool | None
            response_extractor: str -> Any  | None

        Returns:
            response_extractor applied to the output of 
            query(self.model, prompt) if response_validator
            accepts query's output | None
        """
        try:
            response = self.query_fn(self.system_prompt + prompt)
        except Exception as e:
            print(f"Caught unexpected exception {e} while \
                  querying model.")

        if response_validator:
            is_valid = response_validator()
        if is_valid:
            return response_extractor(response)
        
        return None
