from pathlib import Path
from langchain_core.documents import Document


BASE_DIR = Path(__file__).resolve().parent
RUNBOOK_DIR = BASE_DIR / "runbooks"


def load_runbooks() -> list[Document]:
    documents = []

    for path in sorted(RUNBOOK_DIR.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            continue

        documents.append(
            Document(
                page_content=content,
                metadata={"source": str(path.relative_to(BASE_DIR))},
            )
        )

    return documents


DOCS = load_runbooks()


def retrieve_runbook(query: str, top_k: int = 3) -> str:
    """Simple local keyword retrieval.

    This intentionally avoids an external vector database so the project
    can run locally with minimal setup. It can later be replaced by
    embeddings + Chroma/FAISS/PGVector.
    """
    if not query:
        return ""

    query_words = {
        word.strip(".,:;!?()[]{}'\"").lower()
        for word in query.split()
        if len(word.strip(".,:;!?()[]{}'\"")) >= 3
    }

    scored = []

    for doc in DOCS:
        content_lower = doc.page_content.lower()
        score = sum(1 for word in query_words if word in content_lower)

        if score:
            scored.append((score, doc))

    scored.sort(key=lambda item: item[0], reverse=True)

    selected = scored[:top_k]

    if not selected:
        return (
            "No matching local runbook was found. "
            "Use Kubernetes evidence and clearly state uncertainty."
        )

    sections = []
    for score, doc in selected:
        sections.append(
            f"### Source: {doc.metadata['source']} (match score: {score})\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(sections)
