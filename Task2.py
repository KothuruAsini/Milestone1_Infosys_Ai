import pandas as pd
import re

file_path = "ReviewSense_Customer_Feedback_5000.xlsx"
df = pd.read_excel(file_path)

keywords = {
    "Delivery": ["delivery", "late", "shipping", "courier"],
    "Product": ["product", "quality", "item", "defective"],
    "Support": ["support", "service", "help", "customer care"],
    "Price": ["price", "cost", "expensive", "cheap"]
}

basic_words = {
    "the", "is", "was", "very", "good", "bad", "late", "product",
    "delivery", "price", "support", "quality", "service", "help",
    "cost", "item", "cheap", "expensive", "and", "to", "for", "of"
}

def classify_feedback(feedback):
    text = feedback.lower()
    for category, words in keywords.items():
        if any(word in text for word in words):
            return category
    return "General"

def detect_errors(feedback):
    errors = []

    # Ignore single-word feedbacks (names)
    if len(feedback.split()) == 1:
        return ["Ignored (Not a feedback sentence)"]

    if "  " in feedback:
        errors.append("Extra spacing found")

    if feedback.isupper():
        errors.append("All letters are uppercase")
    elif feedback.islower():
        errors.append("All letters are lowercase")

    words = re.findall(r'\b\w+\b', feedback.lower())
    misspelled = [w for w in words if w not in basic_words]

    if misspelled:
        errors.append("Possible spelling issues: " + ", ".join(set(misspelled)))

    return errors if errors else ["No errors found"]

# ✅ CHANGE COLUMN HERE (use correct feedback column)
for index, row in df.iterrows():
    feedback = str(row.iloc[2])  # <-- feedback column
    category = classify_feedback(feedback)
    errors = detect_errors(feedback)

    print("\nFeedback:", feedback)
    print("Category:", category)
    print("Errors:", "; ".join(errors))
