#!/usr/bin/env python3
"""
Transcript to JSON Converter
----------------------------
A script that converts text transcripts into a structured JSON format.
"""

import json
import re
import argparse
import os
from datetime import datetime


def parse_transcript_line(line, pattern=None):
    """
    Parse a single line of transcript according to specified pattern.
    Returns a dictionary with speaker, time (if available), and dialogue.
    """
    if not pattern:
        # Default pattern: Speaker [Time]: Dialogue
        # Also handles Speaker: Dialogue format
        patterns = [
            r'^(.*?)\s*\[([^\]]+)\]:\s*(.*)$',  # Speaker [Time]: Dialogue
            r'^(.*?):\s*(.*)$'                   # Speaker: Dialogue
        ]
        
        for p in patterns:
            match = re.match(p, line.strip())
            if match:
                if len(match.groups()) == 3:
                    return {
                        "speaker": match.group(1).strip(),
                        "time": match.group(2).strip(),
                        "dialogue": match.group(3).strip()
                    }
                elif len(match.groups()) == 2:
                    return {
                        "speaker": match.group(1).strip(),
                        "dialogue": match.group(2).strip()
                    }
        
        # If no pattern matches, treat the entire line as dialogue
        return {"dialogue": line.strip()}
    else:
        # Use custom regex pattern
        match = re.match(pattern, line.strip())
        if match:
            result = {}
            if 'speaker' in pattern.groupindex:
                result["speaker"] = match.group('speaker').strip()
            if 'time' in pattern.groupindex:
                result["time"] = match.group('time').strip()
            if 'dialogue' in pattern.groupindex:
                result["dialogue"] = match.group('dialogue').strip()
            return result
        
        # If custom pattern doesn't match, treat as dialogue only
        return {"dialogue": line.strip()}


def process_file(file_path, pattern=None, output_path=None, metadata=None):
    """
    Process a transcript file and convert it to JSON.
    """
    # Ensure output_path exists
    if not output_path:
        output_path = os.path.splitext(file_path)[0] + ".json"

    # Initialize the structure
    result = {}
    if metadata:
        result.update(metadata)
    else:
        result["interview"] = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "transcript": []
        }

    # Read and process the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()
    
    # Filter out empty lines and process each line
    transcript_data = []
    for line in lines:
        if line.strip():
            entry = parse_transcript_line(line, pattern)
            if entry:
                transcript_data.append(entry)
    
    # Determine where to place the transcript data
    if "interview" in result and "transcript" in result["interview"]:
        result["interview"]["transcript"] = transcript_data
    else:
        result["transcript"] = transcript_data
    
    # Write the JSON output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    return output_path, len(transcript_data)


def process_json_file(file_path, output_path=None):
    """
    Process a JSON file that may need restructuring.
    """
    # Ensure output_path exists
    if not output_path:
        output_path = os.path.splitext(file_path)[0] + "_processed.json"
    
    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Determine if the file already has the right structure
    if "interview" in data and "transcript" in data["interview"]:
        # Already in the right format
        if file_path != output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        return output_path, len(data["interview"]["transcript"])
    
    # Try to find transcript data in the file
    transcript_data = None
    if "transcript" in data:
        transcript_data = data["transcript"]
    else:
        # Search for transcript arrays in nested structures
        for key, value in data.items():
            if isinstance(value, dict) and "transcript" in value and isinstance(value["transcript"], list):
                transcript_data = value["transcript"]
                break
    
    if transcript_data:
        # Create the proper structure
        result = {
            "interview": {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "transcript": transcript_data
            }
        }
        
        # Copy other metadata if present
        if "interview" in data:
            for key, value in data["interview"].items():
                if key != "transcript":
                    result["interview"][key] = value
        
        # Write the JSON output
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        return output_path, len(transcript_data)
    
    raise ValueError("Could not find transcript data in the JSON file")


def main():
    parser = argparse.ArgumentParser(description='Convert text transcripts to JSON format.')
    parser.add_argument('file', help='The transcript file to process')
    parser.add_argument('-o', '--output', help='Output file path (default: same as input with .json extension)')
    parser.add_argument('-p', '--pattern', help='Custom regex pattern for parsing lines')
    parser.add_argument('-m', '--metadata', help='JSON file with metadata to include')
    args = parser.parse_args()
    
    file_path = args.file
    output_path = args.output
    pattern = args.pattern
    
    # Load metadata if provided
    metadata = None
    if args.metadata:
        with open(args.metadata, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    
    try:
        # Check if the input is already JSON
        if file_path.lower().endswith('.json'):
            output_file, entry_count = process_json_file(file_path, output_path)
            print(f"Processed JSON file with {entry_count} transcript entries.")
            print(f"Output saved to: {output_file}")
        else:
            # Process as a text transcript
            output_file, entry_count = process_file(file_path, pattern, output_path, metadata)
            print(f"Processed {entry_count} transcript lines.")
            print(f"JSON output saved to: {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())