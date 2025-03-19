import json

def synthesize_feedback_with_sentiment(analysis_file="analysis_output.json", sentiment_file="sentiment_summary.json", output_file="synthesis_output_with_sentiment.json"):
    """
    Synthesizes interview feedback from two JSON input files (analysis and sentiment),
    generates a written synthesis and recommendation, incorporating sentiment data for both
    candidate and interviewer, and saves the output to a new JSON file.

    Args:
        analysis_file (str): Path to the input JSON file containing interview analysis (scores, etc.).
        sentiment_file (str): Path to the input JSON file containing sentiment summary.
        output_file (str): Path to the output JSON file to save the synthesis.
    """

    try:
        with open(analysis_file, 'r') as f_analysis, open(sentiment_file, 'r') as f_sentiment:
            analysis_data = json.load(f_analysis)
            sentiment_data = json.load(f_sentiment)
    except FileNotFoundError as e:
        print(f"Error: Input file not found: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in file: {e}")
        return

    analysis_metadata = analysis_data.get("interview_metadata", {})
    sentiment_metadata = sentiment_data.get("interview", {})

    # Verify interview metadata matches
    metadata_keys_to_check = ["date", "position", "candidate", "interviewer"]
    for key in metadata_keys_to_check:
        if analysis_metadata.get(key) != sentiment_metadata.get(key):
            print(f"Warning: Interview metadata mismatch for key '{key}'. Synthesis may be inaccurate.")
            break

    scores = analysis_data.get("scores", {})
    assessment_details = analysis_data.get("assessment_details", {})
    pass_fail_status = analysis_data.get("pass_fail", "N/A")
    candidate_overall_sentiment = sentiment_data.get("interview", {}).get("candidate_sentiment", {}).get("overall_sentiment", "N/A")
    interviewer_overall_sentiment = sentiment_data.get("interview", {}).get("interviewer_sentiment", {}).get("overall_sentiment", "N/A")


    strengths = []
    weaknesses = []

    for attribute, score in scores.items():
        if isinstance(score, int): # Only consider attributes with numerical scores
            if score >= 3:
                strengths.append(attribute)
            elif score <= 2:
                weaknesses.append(attribute)

    synthesis_text = ""
    recommendation_text = ""

    sentiment_intro = f"The candidate's overall sentiment during the interview was assessed as '{candidate_overall_sentiment}', and the interviewer's sentiment was assessed as '{interviewer_overall_sentiment}'. "
    synthesis_text += sentiment_intro

    if strengths:
        synthesis_text += "Strengths demonstrated in this interview include: " + ", ".join(strengths) + ". "
    if weaknesses:
        synthesis_text += "Areas for improvement include: " + ", ".join(weaknesses) + ". "
    elif not strengths and not weaknesses:
        synthesis_text += "No strengths or weaknesses identified based on numerical scores. "


    if pass_fail_status == "Pass":
        if not weaknesses and strengths: # exceptional pass
            recommendation_text = "The candidate performed exceptionally well in this mock interview, demonstrating proficiency across all assessed areas. It is recommended that they try a more challenging mock interview next time to further refine their skills. In the meantime, they should focus on showcasing their abilities through portfolio projects and actively engage in their job search."
        else: # standard pass
            recommendation_text = "The candidate passed this mock interview, indicating a good foundation in the assessed areas.  To continue improving, they should keep practicing technical interview questions.  Additionally, they should dedicate time to their job search and portfolio development to maximize their opportunities."
    elif pass_fail_status == "Fail":
        if len(weaknesses) >= 3 and not strengths: # poor fail
             recommendation_text = "The candidate did not pass this mock interview and demonstrated weaknesses in several key areas. It is crucial for the candidate to focus on mastering fundamental computer science concepts and data structures before further interview practice. Targeted study in these areas will build a stronger foundation for future success."
        else: # standard fail
            recommendation_text = "The candidate did not pass this mock interview, indicating areas for improvement in their technical interview skills.  It is recommended they double down on practicing technical interview questions, paying particular attention to the identified areas for improvement. Consistent practice and focused effort will be key to passing future interviews."
    else: # Should not happen based on problem description, but handling just in case.
        recommendation_text = "Unable to determine pass/fail status clearly. Please review the scores and reassess. In the meantime, focus on practicing all aspects of the technical interview."

    # Sentiment-based recommendations
    if candidate_overall_sentiment in ["Negative", "Neutral"] or interviewer_overall_sentiment in ["Negative", "Neutral"]:
        recommendation_text += "  Additionally, the candidate should pay attention to their own and their interviewer's body language, tone, and facial expressions in future interviews to ensure a positive and engaging interaction."
    elif candidate_overall_sentiment == "Positive" and interviewer_overall_sentiment == "Positive":
        recommendation_text += "  Keep up the good work with your body language, tone, and facial expression! It seems like everyone had a positive sentiment during this interview."


    synthesis_and_recommendation = {
        "synthesis": synthesis_text.strip(),
        "recommendation": recommendation_text.strip()
    }

    output_data = {
        "interview_metadata": analysis_metadata,
        "scores": scores,
        "assessment_details": assessment_details,
        "pass_fail": pass_fail_status,
        "synthesis_and_recommendation": synthesis_and_recommendation,
        "candidate_sentiment": sentiment_data.get("interview", {}).get("candidate_sentiment", {}), # Include sentiment data in output
        "interviewer_sentiment": sentiment_data.get("interview", {}).get("interviewer_sentiment", {}) # Include interviewer sentiment
    }

    try:
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=4)
        print(f"Synthesis and recommendation with sentiment saved to: {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")


if __name__ == "__main__":
    synthesize_feedback_with_sentiment()