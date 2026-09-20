class DiagnosisResult:
    def __init__(self, project_types, diagnosis):
        self.project_types = project_types
        self.diagnosis = diagnosis

    def to_dict(self):
        return {
            "project_types": self.project_types,
            "diagnosis": self.diagnosis
        }

    def summary(self):
        if self.diagnosis["status"] == "healthy":
            return "No known problems were detected."

        findings = self.diagnosis.get("findings", [])

        return f"{len(findings)} problem(s) detected."
