import os
from dotenv import load_dotenv

load_dotenv()

from graph import app


def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Create a .env file and add your API key."
        )

    question = input("Ask Incident Question: ").strip()

    if not question:
        print("Please enter an incident question.")
        return

    result = app.invoke({"question": question})

    print("\n" + "=" * 70)
    print("DEVOPS INCIDENT ANALYSIS")
    print("=" * 70)
    print(result.get("response", "No response generated."))


if __name__ == "__main__":
    main()
