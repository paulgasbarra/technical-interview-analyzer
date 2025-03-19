#!/usr/bin/env python3
"""
Sentiment Analysis Script

This script takes a transcript file, processes it with the sentiment analyzer,
and outputs the results.
"""

import argparse
import json
import os
from sentiment_analyzer import analyze_sentiment, summarize_sentiment

def main():
    """Main function to parse arguments and run the sentiment analysis."""
    parser = argparse.ArgumentParser(description='Analyze sentiment in a transcript file.')
    parser.add_argument('file', help='Path to the transcript file (text or JSON)')
    parser.add_argument('--output', help='Output JSON file path (default: sentiment_results.json)')
    
    args = parser.parse_args()
    
    # Determine input file type and process accordingly
    input_file = args.file
    output_file = args.output or 'sentiment_results.json'
    
    # Check if input is a text file that needs conversion
    if input_file.endswith('.txt'):
        # Import transcript converter
        from transcript_converter import process_file
        
        # Convert text to JSON
        json_file, _ = process_file(input_file)
        print(f"Converted text transcript to JSON: {json_file}")
        input_file = json_file
    
    # Analyze sentiment
    print(f"Analyzing sentiment in {input_file}...")
    sentiment_results = analyze_sentiment(input_file)
    
    if sentiment_results:
        # Summarize the sentiment
        sentiment_summary = summarize_sentiment(sentiment_results)
        
        # Prepare output data
        output_data = {
            "sentiment_analysis": {
                "file": os.path.basename(input_file),
                "candidate_sentiment": sentiment_summary['candidate'],
                "interviewer_sentiment": sentiment_summary['interviewer']
            }
        }
        
        # Write results to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        # Print summary to console
        print("\nSentiment Analysis Results:")
        print(f"Candidate sentiment: {sentiment_summary['candidate']['overall_sentiment']}")
        print(f"  - Positive: {sentiment_summary['candidate']['positive_percentage']:.1f}%")
        print(f"  - Negative: {sentiment_summary['candidate']['negative_percentage']:.1f}%")
        print(f"  - Neutral: {sentiment_summary['candidate']['neutral_percentage']:.1f}%")
        print(f"  - Compound score: {sentiment_summary['candidate']['compound_score']:.2f}")
        
        print(f"\nInterviewer sentiment: {sentiment_summary['interviewer']['overall_sentiment']}")
        print(f"  - Positive: {sentiment_summary['interviewer']['positive_percentage']:.1f}%")
        print(f"  - Negative: {sentiment_summary['interviewer']['negative_percentage']:.1f}%")
        print(f"  - Neutral: {sentiment_summary['interviewer']['neutral_percentage']:.1f}%")
        print(f"  - Compound score: {sentiment_summary['interviewer']['compound_score']:.2f}")
        
        print(f"\nFull results saved to {output_file}")
    else:
        print("Sentiment analysis failed. Check the error messages above.")

if __name__ == "__main__":
    main() 