class Researcher:
    def run(self, query):
        return f"Research notes about {query}"

class Analyst:
    def run(self, notes):
        return f"Analysis summary of {notes}"

class Writer:
    def run(self, summary):
        return f"Final polished answer: {summary}"
