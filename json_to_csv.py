import json
import csv


def json_to_csv(json_file, csv_file):
    """
    Converts a JSON file to a CSV file with specific headers and only one row.

    Args:
        json_file (str): Path to the input JSON file.
        csv_file (str): Path to the output CSV file.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {json_file}")
        return
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    # Extract data for headers
    try:
        interview_metadata = data.get("interview_metadata", {})
        interview_value = interview_metadata.get("candidate", "") + " " + interview_metadata.get("date", "")
        candidate_value = interview_metadata.get("candidate", "")
        interviewer_value = interview_metadata.get("interviewer", "")
        candidate_sentiment = data.get("candidate_sentiment", {}).get("overall_sentiment", "")
        interviewer_sentiment = data.get("interviewer_sentiment", {}).get("overall_sentiment", "")
        interview_result = data.get("pass_fail", "")
        recommendation = data.get("synthesis_and_recommendation", {}).get("recommendation", "")

    except Exception as e:
        print(f"Error extracting metadata for headers: {e}")
        interview_value = ""
        candidate_value = ""
        interviewer_value = ""
        candidate_sentiment = ""
        interviewer_sentiment = ""
        interview_result = ""
        recommendation = ""

    # Prepare CSV writing
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header row
            header = ["Interview", "Candidate", "Interviewer", "Candidate Sentiment", "Interviewer Sentiment", "Interview Result", "Recommendation"]
            writer.writerow(header)

            # Write data row
            data_row = [interview_value, candidate_value, interviewer_value, candidate_sentiment, interviewer_sentiment, interview_result, recommendation]
            writer.writerow(data_row)

        print(f"Successfully converted {json_file} to {csv_file}")

    except Exception as e:
        print(f"Error writing to CSV: {e}")
        return


# Example usage
if __name__ == "__main__":
    input_json_file = "synthesis_output_with_sentiment.json"  # Replace with your JSON file
    output_csv_file = "output.csv"  # Replace with your desired CSV file name
    json_to_csv(input_json_file, output_csv_file)