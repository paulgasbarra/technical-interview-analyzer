#!/usr/bin/env python3
"""
Transcript Analysis Pipeline

This script processes transcript files from the transcripts folder,
runs them through both sentiment and transcript analyzers,
and combines the results into a CSV file.
"""

import os
import csv
import argparse
from pathlib import Path
from sentiment_analyzer import analyze_sentiment
from transcript_analyzer import analyze_transcript

def process_transcript(transcript_path):
    """
    Process a single transcript file through both analyzers.
    
    Args:
        transcript_path: Path to the transcript file
        
    Returns:
        Dictionary containing combined analysis results
    """
    # Read the transcript content
    with open(transcript_path, 'r', encoding='utf-8') as file:
        transcript_text = file.read()
    
    # Get the transcript filename without extension for reporting
    transcript_name = os.path.basename(transcript_path)
    
    # Run sentiment analysis
    sentiment_results = analyze_sentiment(transcript_text)
    
    # Run transcript analysis
    transcript_results = analyze_transcript(transcript_text)
    
    # Combine results
    combined_results = {
        'transcript_name': transcript_name,
        **sentiment_results,
        **transcript_results
    }
    
    return combined_results

def process_all_transcripts(transcripts_dir='transcripts', output_file='transcript_analysis_results.csv'):
    """
    Process all transcript files in the specified directory and save results to CSV.
    
    Args:
        transcripts_dir: Directory containing transcript files
        output_file: Path to the output CSV file
    """
    # Ensure the transcripts directory exists
    if not os.path.exists(transcripts_dir):
        print(f"Error: Transcripts directory '{transcripts_dir}' not found.")
        return
    
    # Get all .txt files in the transcripts directory
    transcript_files = [os.path.join(transcripts_dir, f) for f in os.listdir(transcripts_dir) 
                       if f.endswith('.txt') and os.path.isfile(os.path.join(transcripts_dir, f))]
    
    if not transcript_files:
        print(f"No transcript files found in '{transcripts_dir}'.")
        return
    
    results = []
    
    # Process each transcript file
    for transcript_file in transcript_files:
        print(f"Processing {transcript_file}...")
        result = process_transcript(transcript_file)
        results.append(result)
    
    # Write results to CSV
    if results:
        # Get all unique keys from all result dictionaries to use as CSV headers
        fieldnames = set()
        for result in results:
            fieldnames.update(result.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"Analysis complete. Results saved to {output_file}")
    else:
        print("No results to write to CSV.")

def main():
    """Main function to parse arguments and run the pipeline."""
    parser = argparse.ArgumentParser(description='Process transcript files and generate analysis CSV.')
    parser.add_argument('--dir', default='transcripts', 
                        help='Directory containing transcript files (default: transcripts)')
    parser.add_argument('--output', default='transcript_analysis_results.csv',
                        help='Output CSV file path (default: transcript_analysis_results.csv)')
    parser.add_argument('--file', help='Process a single transcript file instead of the entire directory')
    
    args = parser.parse_args()
    
    if args.file:
        # Process a single file
        if not os.path.isfile(args.file):
            print(f"Error: File '{args.file}' not found.")
            return
            
        result = process_transcript(args.file)
        
        # Write single result to CSV
        with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = sorted(list(result.keys()))
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(result)
            
        print(f"Analysis complete. Results saved to {args.output}")
    else:
        # Process all files in the directory
        process_all_transcripts(args.dir, args.output)

if __name__ == "__main__":
    main() 