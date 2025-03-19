#!/usr/bin/env python3
"""
Combined Analysis Pipeline

This script processes transcript files through both sentiment and transcript analyzers,
and combines the results into a single CSV file.
"""

import argparse
import csv
import json
import os
import sys
import traceback
from sentiment_analyzer import analyze_sentiment, summarize_sentiment
from transcript_analyzer import analyze_transcript

def process_transcript(transcript_file, debug=False):
    """
    Process a single transcript file through both analyzers.
    
    Args:
        transcript_file: Path to the transcript file
        debug: Whether to print debug information
        
    Returns:
        Dictionary containing combined analysis results, or None if an error occurred
    """
    try:
        print(f"Processing {transcript_file}...")
        
        # Check if input is a text file that needs conversion
        if transcript_file.endswith('.txt'):
            try:
                # Import transcript converter
                from transcript_converter import process_file
                
                # Convert text to JSON
                print(f"Converting text transcript to JSON...")
                json_file, _ = process_file(transcript_file)
                print(f"Converted text transcript to JSON: {json_file}")
                transcript_file = json_file
            except Exception as e:
                print(f"ERROR during transcript conversion: {str(e)}")
                if debug:
                    traceback.print_exc()
                return None
        
        # Get the transcript filename without extension for reporting
        transcript_name = os.path.basename(transcript_file)
        
        # Run sentiment analysis
        print("Running sentiment analysis...")
        sentiment_results = analyze_sentiment(transcript_file)
        if not sentiment_results:
            print("Sentiment analysis failed.")
            return None
        
        sentiment_summary = summarize_sentiment(sentiment_results)
        
        # Run transcript analysis
        print("Running transcript analysis...")
        transcript_results = analyze_transcript(transcript_file)
        if "error" in transcript_results:
            print(f"Transcript analysis failed: {transcript_results['error']}")
            return None
        
        # Combine results
        combined_results = {
            'transcript_name': transcript_name,
            'pass_fail': transcript_results['pass_fail']
        }
        
        # Add sentiment results
        combined_results['candidate_sentiment'] = sentiment_summary['candidate']['overall_sentiment']
        combined_results['candidate_positive'] = sentiment_summary['candidate']['positive_percentage']
        combined_results['candidate_negative'] = sentiment_summary['candidate']['negative_percentage']
        combined_results['candidate_neutral'] = sentiment_summary['candidate']['neutral_percentage']
        combined_results['candidate_compound'] = sentiment_summary['candidate']['compound_score']
        
        combined_results['interviewer_sentiment'] = sentiment_summary['interviewer']['overall_sentiment']
        combined_results['interviewer_positive'] = sentiment_summary['interviewer']['positive_percentage']
        combined_results['interviewer_negative'] = sentiment_summary['interviewer']['negative_percentage']
        combined_results['interviewer_neutral'] = sentiment_summary['interviewer']['neutral_percentage']
        combined_results['interviewer_compound'] = sentiment_summary['interviewer']['compound_score']
        
        # Add transcript analysis scores
        for criterion, score in transcript_results['scores'].items():
            combined_results[f"score_{criterion.replace(' ', '_').lower()}"] = score
        
        return combined_results
    
    except Exception as e:
        print(f"ERROR processing transcript: {str(e)}")
        if debug:
            traceback.print_exc()
        return None

def process_all_transcripts(transcripts_dir, output_file, debug=False):
    """
    Process all transcript files in the specified directory and save results to CSV.
    
    Args:
        transcripts_dir: Directory containing transcript files
        output_file: Path to the output CSV file
        debug: Whether to print debug information
    """
    # Ensure the transcripts directory exists
    if not os.path.exists(transcripts_dir):
        print(f"ERROR: Transcripts directory '{transcripts_dir}' not found.")
        return 1
    
    # Get all transcript files in the directory
    transcript_files = []
    for f in os.listdir(transcripts_dir):
        file_path = os.path.join(transcripts_dir, f)
        if os.path.isfile(file_path) and (f.endswith('.txt') or f.endswith('.json')):
            transcript_files.append(file_path)
    
    if not transcript_files:
        print(f"No transcript files found in '{transcripts_dir}'.")
        return 1
    
    results = []
    
    # Process each transcript file
    for transcript_file in transcript_files:
        result = process_transcript(transcript_file, debug)
        if result:
            results.append(result)
    
    # Write results to CSV
    if results:
        # Get all unique keys from all result dictionaries to use as CSV headers
        fieldnames = set()
        for result in results:
            fieldnames.update(result.keys())
        fieldnames = sorted(list(fieldnames))
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
            
            print(f"Analysis complete. Results saved to {output_file}")
            return 0
        except Exception as e:
            print(f"ERROR writing to CSV: {str(e)}")
            if debug:
                traceback.print_exc()
            return 1
    else:
        print("No results to write to CSV.")
        return 1

def main():
    """Main function to parse arguments and run the pipeline."""
    parser = argparse.ArgumentParser(description='Process transcript files and generate combined analysis CSV.')
    parser.add_argument('--dir', help='Directory containing transcript files')
    parser.add_argument('--file', help='Process a single transcript file')
    parser.add_argument('--output', default='combined_analysis_results.csv',
                        help='Output CSV file path (default: combined_analysis_results.csv)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode for more detailed output')
    
    args = parser.parse_args()
    
    if not args.dir and not args.file:
        print("ERROR: Either --dir or --file must be specified.")
        return 1
    
    if args.file:
        # Process a single file
        if not os.path.isfile(args.file):
            print(f"ERROR: File '{args.file}' not found.")
            return 1
            
        result = process_transcript(args.file, args.debug)
        
        if result:
            # Write single result to CSV
            try:
                with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = sorted(list(result.keys()))
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow(result)
                
                print(f"Analysis complete. Results saved to {args.output}")
                return 0
            except Exception as e:
                print(f"ERROR writing to CSV: {str(e)}")
                if args.debug:
                    traceback.print_exc()
                return 1
        else:
            print("Analysis failed. No results to write.")
            return 1
    else:
        # Process all files in the directory
        return process_all_transcripts(args.dir, args.output, args.debug)

if __name__ == "__main__":
    sys.exit(main()) 