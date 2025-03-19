import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # Requires nltk.download('vader_lexicon')
from nltk import tokenize
import nltk  # Import nltk
import re
import ssl

# Handle SSL certificate verification issues (common on macOS)
try:
    _create_unverified_https_context = ssl._create_unverified_context
    ssl._create_default_https_context = _create_unverified_https_context
except AttributeError:
    pass


# Download required NLTK data (if not already downloaded)
try:
    nltk.data.find('sentiment/vader_lexicon')  # Check if vader_lexicon is already downloaded
except LookupError:
    try:
        nltk.download('vader_lexicon')
    except ssl.SSLError as e:
        print(f"SSL Error downloading vader_lexicon: {e}")
        print("Please try again or manually download and place the lexicon.")
        exit()  # Exit if the download fails

try:
    nltk.data.find('tokenizers/punkt')  # Check if punkt is already downloaded
except LookupError:
    try:
        nltk.download('tokenizers/punkt')
    except ssl.SSLError as e:
        print(f"SSL Error downloading punkt: {e}")
        print("Please try again or manually download and place the tokenizer.")
        exit()  # Exit if the download fails


def analyze_sentiment(transcript_json_file):
    """
    Analyzes the sentiment of the candidate and interviewer in a mock interview transcript.

    Args:
        transcript_json_file (str): Path to the JSON file containing the interview transcript.

    Returns:
        dict: A dictionary containing the average sentiment scores for the candidate and interviewer.
               Returns None if the JSON file is invalid or empty.  Also returns None if no turns exist
    """

    try:
        with open(transcript_json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {transcript_json_file}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {transcript_json_file}")
        return None

    if not isinstance(data, dict) or 'interview' not in data or not isinstance(data['interview'], dict) or 'transcript' not in data['interview'] or not isinstance(data['interview']['transcript'], list):
        print(f"Error: Invalid JSON format. Expected a dictionary with an 'interview' dictionary containing a 'transcript' list.")
        return None

    transcript = data['interview']['transcript']  # Corrected to access the transcript inside the interview object

    if not transcript:
        print("Error: No turns found in the transcript.")
        return None  # Handle empty transcript case

    candidate_utterances = []
    interviewer_utterances = []

    for turn in transcript:
        if not isinstance(turn, dict) or 'speaker' not in turn or 'dialogue' not in turn:  # Changed 'utterance' to 'dialogue'
            print("Warning: Skipping invalid turn format. Expected dictionary with 'speaker' and 'dialogue'.")
            continue  # Skip invalid turns

        speaker = turn['speaker']
        utterance = turn['dialogue']  # Changed 'utterance' to 'dialogue'

        if speaker.lower() == 'alice johnson':  # Changed to match the actual speaker name
            candidate_utterances.append(utterance)
        elif speaker.lower() == 'bob smith':  # Changed to match the actual speaker name
            interviewer_utterances.append(utterance)
        else:
            print(f"Warning: Unknown speaker: {speaker}. Skipping utterance.")  # handle potential errors in data

    # Initialize sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    def calculate_average_sentiment(utterances):
        """Calculates the average sentiment score for a list of utterances.

        Args:
            utterances (list): A list of strings, where each string is an utterance.

        Returns:
            dict: A dictionary containing the average compound, positive, neutral, and negative sentiment scores.
                 Returns None if the list of utterances is empty.
        """
        if not utterances:
            return None  # Handle the case where there are no utterances for a speaker

        compound_scores = []
        positive_scores = []
        negative_scores = []
        neutral_scores = []

        for utterance in utterances:
            # Split the utterance into sentences to increase accuracy
            sentences = tokenize.sent_tokenize(utterance)
            for sentence in sentences:
                # Clean the sentence to remove non-alphanumeric characters (except spaces and basic punctuation) to improve sentiment accuracy
                cleaned_sentence = re.sub(r"[^a-zA-Z0-9\s.,?!']", "", sentence)  # More robust cleaning

                scores = analyzer.polarity_scores(cleaned_sentence)  # Pass sentence by sentence
                compound_scores.append(scores['compound'])
                positive_scores.append(scores['pos'])
                negative_scores.append(scores['neg'])
                neutral_scores.append(scores['neu'])

        avg_compound = sum(compound_scores) / len(compound_scores)
        avg_positive = sum(positive_scores) / len(positive_scores)
        avg_negative = sum(negative_scores) / len(negative_scores)
        avg_neutral = sum(neutral_scores) / len(neutral_scores)

        return {
            'compound': avg_compound,
            'positive': avg_positive,
            'negative': avg_negative,
            'neutral': avg_neutral
        }

    candidate_sentiment = calculate_average_sentiment(candidate_utterances)
    interviewer_sentiment = calculate_average_sentiment(interviewer_utterances)

    return {
        'candidate': candidate_sentiment,
        'interviewer': interviewer_sentiment
    }


def summarize_sentiment(sentiment_results):
    """
    Summarizes the sentiment analysis results into human-readable descriptions.

    Args:
        sentiment_results (dict): The dictionary returned by analyze_sentiment.

    Returns:
        dict: A dictionary containing sentiment summaries for the candidate and interviewer.
    """

    def interpret_sentiment(sentiment_data):
        """Interprets the sentiment data and returns a descriptive summary."""
        if sentiment_data is None:
            return "No sentiment data available."

        compound_score = sentiment_data['compound']

        if compound_score >= 0.05:
            sentiment = "Generally positive."
        elif compound_score <= -0.05:
            sentiment = "Generally negative."
        else:
            sentiment = "Neutral."

        positive_percentage = sentiment_data['positive'] * 100
        negative_percentage = sentiment_data['negative'] * 100
        neutral_percentage = sentiment_data['neutral'] * 100

        summary = f"{sentiment} (Positive: {positive_percentage:.1f}%, Negative: {negative_percentage:.1f}%, Neutral: {neutral_percentage:.1f}%).  Compound Score: {compound_score:.2f}"
        return summary

    candidate_summary = interpret_sentiment(sentiment_results['candidate'])
    interviewer_summary = interpret_sentiment(sentiment_results['interviewer'])

    return {
        'candidate': candidate_summary,
        'interviewer': interviewer_summary
    }


# Example usage
if __name__ == "__main__":
    transcript_file = "interview_transcript.json"

    results = analyze_sentiment(transcript_file)

    if results:
        sentiment_summary = summarize_sentiment(results)
        print("Sentiment Analysis Summary:")
        print("Candidate (Alice Johnson):", sentiment_summary['candidate'])
        print("Interviewer (Bob Smith):", sentiment_summary['interviewer'])
    else:
        print("Sentiment analysis failed. Check the error messages above.")