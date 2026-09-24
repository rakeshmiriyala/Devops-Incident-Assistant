import os
from dotenv import load_dotenv

load_dotenv()

from graph import app


def main():

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
