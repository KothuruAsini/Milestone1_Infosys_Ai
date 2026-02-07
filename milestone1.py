# Import required libraries
import pandas as pd          # Used for reading Excel/CSV files and DataFrame operations
import re                    # Used for regular expressions (text cleaning)
import string                # Used to access punctuation characters
# Define stopwords
# These words will be removed during text cleaning
STOPWORDS = {
    "is", "the", "and", "to", "a", "an", "of", "in", "for",
    "on", "with", "as", "by", "at", "from", "that",
    "this", "it", "be", "are", "was"
}
# Function: clean_text
# Purpose: Clean and normalize feedback text
def clean_text(text):
    # Convert input to string and make everything lowercase
    # This ensures uniform text processing
    text = str(text).lower()
    # Remove URLs (http, https, www links)
    # URLs usually add noise in sentiment/text analysis
    text = re.sub(r"http\S+", "", text)
    # Remove numbers (ratings, IDs, etc. are usually irrelevant)
    text = re.sub(r"\d+", "", text)
    # Remove punctuation symbols like ! @ # $
    # Keeps only words
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Remove extra spaces and leading/trailing whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Remove stopwords to keep only meaningful words
    words = [word for word in text.split() if word not in STOPWORDS]
    # Join the cleaned words back into a single string
    return " ".join(words)
def main():
    # Define file paths
    # Excel is the primary input, CSV is fallback
    file_path_excel = "ReviewSense_Customer_Feedback_5000.xlsx"
    file_path_csv = "Milestone1_cleaned_feedback.csv"
    try:
        # Try reading the Excel file first
        df = pd.read_excel(file_path_excel)
        # Inform user that Excel file was found
        print("Reading from Excel file")
    except FileNotFoundError:
        # If Excel file is missing, attempt to load CSV instead
        print("Excel file not found. Attempting to read from existing CSV.")
        try:
            # Read CSV file
            df = pd.read_csv(file_path_csv)
            # If clean_feedback already exists, skip re-cleaning
            if "clean_feedback" in df.columns:
                print("CSV already has cleaned feedback. Skipping cleaning.")
                return
            # If feedback column exists, proceed to re-clean
            elif "feedback" in df.columns:
                print("Re-cleaning feedback from CSV.")
            # If neither column exists, raise an error
            else:
                raise ValueError("'feedback' column not found in CSV file.")
        except FileNotFoundError:
            # If both Excel and CSV are missing
            raise ValueError(
                "Neither Excel nor CSV file found. Please provide the input file."
            )
    # Final validation to ensure feedback column exists
    if "feedback" not in df.columns:
        raise ValueError("'feedback' column not found in the file.")
    # Apply text cleaning function to feedback column
    df["clean_feedback"] = df["feedback"].apply(clean_text)
    # Save cleaned data into CSV file
    df.to_csv("Milestone1_cleaned_feedback.csv", index=False)
    # Success message
    print("Milestone 1 Completed Successfully")
    # Display sample output for verification
    print(df[["feedback", "clean_feedback"]].head())
if __name__ == "__main__":
    main()
