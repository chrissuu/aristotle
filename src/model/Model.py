class Model:
    def __init__(self, query_fn, system_prompt = ""):
        self.query_fn = query_fn
        self.system_prompt = system_prompt

    def query(
        self, 
        prompt,
        response_extractor = id
    ) -> str | None:
        """
        Query a model with Model's query_fn.
        Response extractor should be safe to call 
        and not throw any errors. If the output
        is not formatted correctly, None should
        be returned. Otherwise, return the
        extracted output.

        Args:
            prompt: str
            response_extractor: str -> Any

        Returns:
            response_extractor applied to the output of 
            query(self.model, prompt)
        """
        try:
            output = self.query_fn(self.system_prompt + prompt)
        except Exception as e:
            print(f"Caught unexpected exception {e} while \
                  querying model.")

        return response_extractor(output)