class DocumentationResult:

    def __init__(self, documentation, diagnosis):
        self.documentation = documentation
        self.diagnosis = diagnosis

    def to_dict(self):
        return {
            "documentation": self.documentation,
            "diagnosis": self.diagnosis
        }

    def summary(self):
        if self.diagnosis["status"] == "healthy":
            return "No known documentation problems were detected."

        findings = self.diagnosis.get("findings", [])

        return f"{len(findings)} documentation problem(s) detected."
