# Import pandas library to handle CSV files and work with tabular data
import pandas as pd

# Import TextBlob for sentiment analysis (it helps find polarity of text)
from textblob import TextBlob

# Import matplotlib to create visualizations like bar charts
import matplotlib.pyplot as plt


# This function analyzes the sentiment of a given text
def get_sentiment(text):

    # Convert the text into a TextBlob object and extract polarity score
    # Polarity ranges from -1 (very negative) to +1 (very positive)
    polarity = TextBlob(str(text)).sentiment.polarity

    # If polarity is greater than 0, sentiment is positive
    if polarity > 0:
        return "positive", polarity

    # If polarity is less than 0, sentiment is negative
    elif polarity < 0:
        return "negative", polarity

    # If polarity is exactly 0, sentiment is neutral
    else:
        return "neutral", polarity


# This ensures the below code runs only when this file is executed directly
# (not when imported as a module)
if __name__ == "__main__":

    # Read the cleaned feedback CSV file into a pandas DataFrame
    df = pd.read_csv("Milestone1_cleaned_feedback.csv")

    # Apply sentiment analysis on each feedback entry
    # The function returns two values: sentiment and polarity
    # pd.Series is used to split them into two separate columns
    df[["sentiment", "confidence_score"]] = df["clean_feedback"].apply(
        lambda x: pd.Series(get_sentiment(x))
    )

    # Save the sentiment analysis results into a new CSV file
    df.to_csv("Milestone2_Sentiment_Results_new.csv", index=False)

    # Print confirmation message for successful execution
    print("Milestone 2 completed successfully!")

    # Count how many reviews fall under each sentiment category
    sentiment_counts = df['sentiment'].value_counts()

    # Create a figure for the bar chart with specified size
    plt.figure(figsize=(8, 5))

    # Define colors for positive, negative, and neutral bars
    colors = ['green', 'red', 'gray']

    # Plot a bar chart showing sentiment distribution
    sentiment_counts.plot(kind='bar', color=colors)

    # Set the title of the chart
    plt.title('How Customers Feel - Sentiment Summary', fontsize=14)

    # Label the x-axis
    plt.xlabel('Sentiment', fontsize=12)

    # Label the y-axis
    plt.ylabel('Number of Reviews', fontsize=12)

    # Keep x-axis labels straight for better readability
    plt.xticks(rotation=0)

    # Add count values above each bar for clarity
    for i, count in enumerate(sentiment_counts):
        plt.text(i, count + 20, str(count), ha='center', fontsize=11)

    # Save the bar chart as an image file
    plt.savefig('sentiment_bar_chart.png', dpi=100, bbox_inches='tight')

    # Display the bar chart on screen
    plt.show()

    # Print confirmation message for chart creation
    print("Bar chart saved as: sentiment_bar_chart.png")

    # Display first few rows showing feedback, sentiment, and confidence score
    print(df[["clean_feedback", "sentiment", "confidence_score"]].head())