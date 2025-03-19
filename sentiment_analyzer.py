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
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Make sure the required NLTK data is downloaded
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    print("Downloading required NLTK data...")
    nltk.download('vader_lexicon')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

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

    interview_data = data['interview']
    transcript = interview_data['transcript']

    if not transcript:
        print("Error: No turns found in the transcript.")
        return None

    candidate_utterances = []
    interviewer_utterances = []

    candidate_name = interview_data.get('candidate', 'Candidate')
    interviewer_name = interview_data.get('interviewer', 'Interviewer')

    for turn in transcript:
        if not isinstance(turn, dict) or 'speaker' not in turn or 'dialogue' not in turn:
            print("Warning: Skipping invalid turn format. Expected dictionary with 'speaker' and 'dialogue'.")
            continue

        speaker = turn['speaker']
        utterance = turn['dialogue']

        if speaker.lower() == candidate_name.lower():
            candidate_utterances.append(utterance)
        elif speaker.lower() == interviewer_name.lower():
            interviewer_utterances.append(utterance)
        else:
            print(f"Warning: Unknown speaker: {speaker}. Skipping utterance.")

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
            return None

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
    Summarizes the sentiment analysis results, breaking down the descriptive elements.

    Args:
        sentiment_results (dict): The dictionary returned by analyze_sentiment.

    Returns:
        dict: A dictionary containing detailed sentiment summaries for the candidate and interviewer.
    """

    def interpret_sentiment(sentiment_data):
        """Interprets the sentiment data and returns a dictionary of descriptive elements."""
        if sentiment_data is None:
            return {
                "overall_sentiment": "No sentiment data available.",
                "positive_percentage": None,
                "negative_percentage": None,
                "neutral_percentage": None,
                "compound_score": None
            }

        compound_score = sentiment_data['compound']

        if compound_score >= 0.05:
            overall_sentiment = "Generally positive"
        elif compound_score <= -0.05:
            overall_sentiment = "Generally negative"
        else:
            overall_sentiment = "Neutral"

        positive_percentage = sentiment_data['positive'] * 100
        negative_percentage = sentiment_data['negative'] * 100
        neutral_percentage = sentiment_data['neutral'] * 100

        return {
            "overall_sentiment": overall_sentiment,
            "positive_percentage": positive_percentage,
            "negative_percentage": negative_percentage,
            "neutral_percentage": neutral_percentage,
            "compound_score": compound_score
        }

    candidate_summary = interpret_sentiment(sentiment_results['candidate'])
    interviewer_summary = interpret_sentiment(sentiment_results['interviewer'])

    return {
        'candidate': candidate_summary,
        'interviewer': interviewer_summary
    }


# Example usage
if __name__ == "__main__":
    transcript_file = "interview_transcript.json"
    output_file = "sentiment_summary.json"  # JSON output file

    try:
        with open(transcript_file, 'r') as f:
            data = json.load(f)
        interview_data = data.get('interview', {}) #extract interview object

        # Extract metadata
        date = interview_data.get('date')
        position = interview_data.get('position')
        candidate_name = interview_data.get('candidate')
        interviewer_name = interview_data.get('interviewer')
        question = interview_data.get('question')

    except (FileNotFoundError, json.JSONDecodeError, AttributeError) as e:
        print(f"Error loading and extracting metadata: {e}")
        date = None
        position = None
        candidate_name = None
        interviewer_name = None
        question = None

    results = analyze_sentiment(transcript_file)

    if results:
        sentiment_summary = summarize_sentiment(results)

        # Prepare JSON output
        output_data = {
            "interview": {
                "date": date,
                "position": position,
                "candidate": candidate_name,
                "interviewer": interviewer_name,
                "question": question,
                "candidate_sentiment": {  # Renamed key
                    "overall_sentiment": sentiment_summary['candidate']['overall_sentiment'],
                    "positive_percentage": sentiment_summary['candidate']['positive_percentage'],
                    "negative_percentage": sentiment_summary['candidate']['negative_percentage'],
                    "neutral_percentage": sentiment_summary['candidate']['neutral_percentage'],
                    "compound_score": sentiment_summary['candidate']['compound_score']
                },
                "interviewer_sentiment": {  # Renamed Key
                    "overall_sentiment": sentiment_summary['interviewer']['overall_sentiment'],
                    "positive_percentage": sentiment_summary['interviewer']['positive_percentage'],
                    "negative_percentage": sentiment_summary['interviewer']['negative_percentage'],
                    "neutral_percentage": sentiment_summary['interviewer']['neutral_percentage'],
                    "compound_score": sentiment_summary['interviewer']['compound_score']
                }
            }
        }

        try:
            with open(output_file, "w") as outfile:
                json.dump(output_data, outfile, indent=4)
            print(f"Sentiment summary written to {output_file}")
        except IOError as e:
            print(f"Error writing to file: {e}")

    else:
        print("Sentiment analysis failed. Check the error messages above.")