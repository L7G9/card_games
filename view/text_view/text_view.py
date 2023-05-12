class TextView:
    """A simple view to read and write using stdin and stdout."""
    def read(self, prompt: str) -> str:
        """Promt user for input."""
        return input(prompt)

    def write(self, line: str):
        """Write a line."""
        print(line)
