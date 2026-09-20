class AdapterContract:

    framework = "unknown"

    def run(self, path):
        raise NotImplementedError(
            "Adapter must implement the run() method."
        )

    def verify(self, path):

        result = self.run(path)

        if not isinstance(result, dict):
            return False

        if "documentation" not in result:
            return False

        if "diagnosis" not in result:
            return False

        return True
