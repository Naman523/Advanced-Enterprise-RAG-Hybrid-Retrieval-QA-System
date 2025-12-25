import json
from typing import List
from rag_chain import ask


# -------------------- UTILS --------------------

def normalize(text: str) -> str:
    return text.lower().strip()


def contains_answer(predicted: str, expected_answers: List[str]) -> bool:
    predicted = normalize(predicted)
    return any(
        normalize(ans) in predicted
        for ans in expected_answers
    )


# -------------------- METRICS --------------------

def precision_at_k(retrieved_docs, expected_answers, k=5):
    """
    Measures how many of top-k retrieved docs
    contain expected answer keywords
    """
    hits = 0

    for doc in retrieved_docs[:k]:
        content = normalize(doc.page_content)
        if any(
            normalize(ans) in content
            for ans in expected_answers
        ):
            hits += 1

    return hits / k


def evaluate(test_file="evaluation/test_set.json"):
    with open(test_file, "r") as f:
        test_cases = json.load(f)

    total = len(test_cases)
    correct = 0
    precision_scores = []

    print("\n📊 Running RAG Evaluation...\n")

    for i, case in enumerate(test_cases, 1):
        question = case["question"]
        expected = case["expected_answer"]

        result = ask(question)
        answer = result["answer"]
        sources = result["sources"]

        # ---- Accuracy ----
        is_correct = contains_answer(answer, expected)
        correct += int(is_correct)

        # ---- Precision@5 ----
        precision = precision_at_k(
            retrieved_docs=[],  # optional if you expose docs
            expected_answers=expected,
            k=5
        )

        precision_scores.append(precision)

        print(f"Q{i}: {question}")
        print(f"Expected: {expected}")
        print(f"Answer: {answer}")
        print(f"Correct: {'✅' if is_correct else '❌'}")
        print("-" * 50)

    accuracy = correct / total
    avg_precision = sum(precision_scores) / len(precision_scores)

    print("\n✅ FINAL METRICS")
    print(f"Answer Accuracy      : {accuracy * 100:.2f}%")
    print(f"Avg Precision@5      : {avg_precision * 100:.2f}%")
    print(f"Total Questions      : {total}")

    return {
        "accuracy": accuracy,
        "precision@5": avg_precision
    }


# -------------------- RUN --------------------

if __name__ == "__main__":
    evaluate()
