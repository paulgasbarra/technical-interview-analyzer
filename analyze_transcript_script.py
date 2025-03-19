#!/usr/bin/env python3
"""
Transcript Analysis Script

This script takes a transcript file, processes it with the transcript analyzer,
and outputs the results.
"""

import argparse
import json
import os
import sys
import traceback
from transcript_analyzer import analyze_transcript

def main():
    """Main function to parse arguments and run the transcript analysis."""
    parser = argparse.ArgumentParser(description='Analyze a transcript file.')
    parser.add_argument('file', help='Path to the transcript file (text or JSON)')
    parser.add_argument('--output', help='Output JSON file path (default: transcript_analysis_results.json)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode for more detailed output')
    
    args = parser.parse_args()
    debug_mode = args.debug
    
    try:
        # Determine input file type and process accordingly
        input_file = args.file
        output_file = args.output or 'transcript_analysis_results.json'
        
        print(f"Starting analysis of: {input_file}")
        
        # Check if the input file exists
        if not os.path.exists(input_file):
            print(f"ERROR: Input file '{input_file}' does not exist.")
            return 1
        
        # Check if input is a text file that needs conversion
        if input_file.endswith('.txt'):
            try:
                # Import transcript converter
                from transcript_converter import process_file
                
                # Convert text to JSON
                print(f"Converting text transcript to JSON...")
                json_file, _ = process_file(input_file)
                print(f"Converted text transcript to JSON: {json_file}")
                input_file = json_file
            except Exception as e:
                print(f"ERROR during transcript conversion: {str(e)}")
                if debug_mode:
                    traceback.print_exc()
                return 1
        
        # Analyze transcript
        print(f"Analyzing transcript in {input_file}...")
        
        # Debug: Print the first few lines of the file
        if debug_mode:
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read(500)  # Read first 500 chars
                    print(f"\nFile content preview:\n{content}...\n")
            except Exception as e:
                print(f"Could not read file for preview: {str(e)}")
        
        analysis_results = analyze_transcript(input_file)
        
        if analysis_results is None:
            print("ERROR: analyze_transcript returned None")
            return 1
        
        if "error" in analysis_results:
            print(f"ERROR during analysis: {analysis_results['error']}")
            return 1
        
        # Write results to file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, indent=2)
            print(f"Results saved to: {output_file}")
        except Exception as e:
            print(f"ERROR saving results to file: {str(e)}")
            if debug_mode:
                traceback.print_exc()
        
        # Print summary to console
        print("\nTranscript Analysis Results:")
        print(f"Pass/Fail: {analysis_results['pass_fail']}")
        
        print("\nScores by Criterion:")
        for criterion, score in analysis_results['scores'].items():
            if score != 'N/A':
                print(f"  {criterion}: {score}/4")
            else:
                print(f"  {criterion}: N/A")
        
        print(f"\nFull results saved to {output_file}")
        return 0
        
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {str(e)}")
        if debug_mode:
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 