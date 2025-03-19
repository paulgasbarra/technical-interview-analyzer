import json

def analyze_transcript(transcript_file):
    """
    Analyzes a technical interview transcript based on predefined criteria.

    Args:
        transcript_file (str): Path to the JSON transcript file.

    Returns:
        dict: A dictionary containing the analysis results, including scores for each criterion and pass/fail status.
    """

    try:
        with open(transcript_file, 'r') as f:
            transcript_data = json.load(f)
            # Extract transcript text from the new JSON structure
            dialogue_entries = transcript_data.get('interview', {}).get('transcript', [])
            transcript_text = ""
            for entry in dialogue_entries:
                transcript_text += entry.get('dialogue', '') + " " # Concatenate dialogues, adding space for separation

    except FileNotFoundError:
        return {"error": "Transcript file not found."}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in transcript file."}

    if not transcript_text:
        return {"error": "No transcript text found in the JSON file."}

    scores = {}
    assessment = {} # To store detailed assessment for each criteria, can be used for more nuanced scoring later

    # --- Criterion Assessments ---
    # (Each criteria assessment will involve analyzing the transcript_text and assigning a score)

    # 1. Asks clarifying questions and incorporates hints
    clarifying_questions_keywords = ["clarify", "understand", "so if", "just to confirm", "could you explain"]
    hints_incorporation_keywords = ["based on your hint", "you mentioned", "following your suggestion"]
    clarifying_questions_count = sum(1 for keyword in clarifying_questions_keywords if keyword.lower() in transcript_text.lower())
    hints_incorporation_count = sum(1 for keyword in hints_incorporation_keywords if keyword.lower() in transcript_text.lower())

    if clarifying_questions_count + hints_incorporation_count >= 3:
        scores["Asks clarifying questions and incorporates hints"] = 4
        assessment["Asks clarifying questions and incorporates hints"] = "Exceptional: Multiple instances of clarifying questions and hint incorporation."
    elif clarifying_questions_count + hints_incorporation_count >= 1:
        scores["Asks clarifying questions and incorporates hints"] = 3
        assessment["Asks clarifying questions and incorporates hints"] = "Proficient: Asks clarifying questions and/or incorporates hints."
    elif clarifying_questions_count > 0 or hints_incorporation_count > 0:
        scores["Asks clarifying questions and incorporates hints"] = 2
        assessment["Asks clarifying questions and incorporates hints"] = "Developing: Minor attempts at clarifying questions or hint incorporation."
    elif clarifying_questions_count == 0 and hints_incorporation_count == 0:
        scores["Asks clarifying questions and incorporates hints"] = 1
        assessment["Asks clarifying questions and incorporates hints"] = "Not Demonstrated: No clarifying questions or hint incorporation."
    else:
        scores["Asks clarifying questions and incorporates hints"] = 'N/A' # Should not reach here, but for safety

    # 2. Verifies assumptions
    assumption_keywords = ["what if", "edge case", "handle", "consider", "input", "null", "empty", "size", "range", "boundary", "negative", "invalid"]
    assumption_questions_count = sum(1 for keyword in assumption_keywords if keyword.lower() in transcript_text.lower())

    if assumption_questions_count >= 3:
        scores["Verifies assumptions"] = 4
        assessment["Verifies assumptions"] = "Exceptional: Thoroughly verifies multiple assumptions and constraints."
    elif assumption_questions_count >= 2:
        scores["Verifies assumptions"] = 3
        assessment["Verifies assumptions"] = "Proficient: Verifies key assumptions and constraints."
    elif assumption_questions_count >= 1:
        scores["Verifies assumptions"] = 2
        assessment["Verifies assumptions"] = "Developing: Attempts to verify some assumptions."
    elif assumption_questions_count == 0:
        scores["Verifies assumptions"] = 1
        assessment["Verifies assumptions"] = "Not Demonstrated: No verification of assumptions."
    else:
        scores["Verifies assumptions"] = 'N/A'

    # 3. Demonstrates understanding w/ example inputs & outputs
    example_keywords = ["for example", "e.g.", "imagine if", "let's say", "input", "output", "result", "so if we give", "then we should get"]
    example_count = sum(1 for keyword in example_keywords if keyword.lower() in transcript_text.lower())

    if example_count >= 3:
        scores["Demonstrates understanding w/ example inputs & outputs"] = 4
        assessment["Demonstrates understanding w/ example inputs & outputs"] = "Exceptional: Provides multiple clear and insightful examples."
    elif example_count >= 2:
        scores["Demonstrates understanding w/ example inputs & outputs"] = 3
        assessment["Demonstrates understanding w/ example inputs & outputs"] = "Proficient: Demonstrates understanding with relevant example inputs and outputs."
    elif example_count >= 1:
        scores["Demonstrates understanding w/ example inputs & outputs"] = 2
        assessment["Demonstrates understanding w/ example inputs & outputs"] = "Developing: Attempts to use examples but may be unclear or insufficient."
    elif example_count == 0:
        scores["Demonstrates understanding w/ example inputs & outputs"] = 1
        assessment["Demonstrates understanding w/ example inputs & outputs"] = "Not Demonstrated: No use of examples to demonstrate understanding."
    else:
        scores["Demonstrates understanding w/ example inputs & outputs"] = 'N/A'

    # 4. Identifies multiple high-level approaches
    approach_keywords = ["approach", "strategy", "method", "way", "alternatively", "instead", "brute force", "efficient", "optimize", "different way"]
    approach_count = sum(1 for keyword in approach_keywords if keyword.lower() in transcript_text.lower())

    if approach_count >= 3:
        scores["Identifies multiple high-level approaches"] = 4
        assessment["Identifies multiple high-level approaches"] = "Exceptional: Clearly identifies and discusses multiple distinct approaches."
    elif approach_count >= 2:
        scores["Identifies multiple high-level approaches"] = 3
        assessment["Identifies multiple high-level approaches"] = "Proficient: Identifies and mentions more than one high-level approach."
    elif approach_count >= 1:
        scores["Identifies multiple high-level approaches"] = 2
        assessment["Identifies multiple high-level approaches"] = "Developing: Mentions a potential alternative approach but may not elaborate."
    elif approach_count == 0:
        scores["Identifies multiple high-level approaches"] = 1
        assessment["Identifies multiple high-level approaches"] = "Not Demonstrated: Only considers one approach or no approaches explicitly identified."
    else:
        scores["Identifies multiple high-level approaches"] = 'N/A'

    # 5. Determines time & space complexity of each high-level approach
    complexity_keywords = ["time complexity", "space complexity", "o(", "big o", "runtime", "memory", "efficiency", "faster", "slower"]
    complexity_count = sum(1 for keyword in complexity_keywords if keyword.lower() in transcript_text.lower())

    if complexity_count >= 4:
        scores["Determines time & space complexity of each high-level approach"] = 4
        assessment["Determines time & space complexity of each high-level approach"] = "Exceptional: Accurately and thoroughly analyzes time and space complexity for multiple approaches."
    elif complexity_count >= 2:
        scores["Determines time & space complexity of each high-level approach"] = 3
        assessment["Determines time & space complexity of each high-level approach"] = "Proficient: Determines time and space complexity for at least one approach."
    elif complexity_count >= 1:
        scores["Determines time & space complexity of each high-level approach"] = 2
        assessment["Determines time & space complexity of each high-level approach"] = "Developing: Attempts to discuss complexity but may be inaccurate or incomplete."
    elif complexity_count == 0:
        scores["Determines time & space complexity of each high-level approach"] = 1
        assessment["Determines time & space complexity of each high-level approach"] = "Not Demonstrated: No discussion of time or space complexity."
    else:
        scores["Determines time & space complexity of each high-level approach"] = 'N/A'

    # 6. Selects appropriate data structure(s) and/or programming approach
    data_structure_keywords = ["hashmap", "dictionary", "set", "list", "array", "stack", "queue", "tree", "graph", "heap", "linked list"]
    approach_selection_keywords = ["iterative", "recursive", "dynamic programming", "greedy", "divide and conquer"]
    justification_keywords = ["because", "since", "so", "therefore", "this allows", "for this reason", "efficient for"]

    ds_mention_count = sum(1 for keyword in data_structure_keywords if keyword.lower() in transcript_text.lower())
    approach_mention_count = sum(1 for keyword in approach_selection_keywords if keyword.lower() in transcript_text.lower())
    justification_count = sum(1 for keyword in justification_keywords if keyword.lower() in transcript_text.lower())

    if ds_mention_count + approach_mention_count >= 2 and justification_count >= 1:
        scores["Selects appropriate data structure(s) and/or programming approach"] = 4
        assessment["Selects appropriate data structure(s) and/or programming approach"] = "Exceptional: Selects and justifies appropriate data structures and/or approaches with clear reasoning."
    elif ds_mention_count + approach_mention_count >= 1 and justification_count >= 1:
        scores["Selects appropriate data structure(s) and/or programming approach"] = 3
        assessment["Selects appropriate data structure(s) and/or programming approach"] = "Proficient: Selects appropriate data structures and/or approaches and provides some justification."
    elif ds_mention_count + approach_mention_count >= 1:
        scores["Selects appropriate data structure(s) and/or programming approach"] = 2
        assessment["Selects appropriate data structure(s) and/or programming approach"] = "Developing: Mentions data structures or approaches but lacks justification or appropriateness is unclear."
    elif ds_mention_count == 0 and approach_mention_count == 0:
        scores["Selects appropriate data structure(s) and/or programming approach"] = 1
        assessment["Selects appropriate data structure(s) and/or programming approach"] = "Not Demonstrated: No explicit selection or discussion of data structures or approaches."
    else:
        scores["Selects appropriate data structure(s) and/or programming approach"] = 'N/A'


    # 7. Writes valid, concise, easy to read, and syntactically correct code for the full algorithm
    # Assumption: We cannot directly assess code validity/syntax from transcript *unless* code is transcribed.
    # For transcript analysis, we can assess based on descriptions of the code logic, clarity of explanation, and conciseness of description.
    # If code *is* in transcript, more detailed analysis is possible (not implemented here for simplicity based on prompt focusing on transcript analysis).
    # For now, let's assess based on description of logic and clarity.

    code_description_keywords = ["algorithm", "logic", "implement", "function", "method", "code", "steps", "process", "iterate", "loop", "condition", "variable"]
    clarity_keywords = ["clearly", "easy to understand", "straightforward", "concise", "simple", "readable"]

    code_description_count = sum(1 for keyword in code_description_keywords if keyword.lower() in transcript_text.lower())
    clarity_count = sum(1 for keyword in clarity_keywords if keyword.lower() in transcript_text.lower())

    if code_description_count >= 4 and clarity_count >= 2:
        scores["Writes valid, concise, easy to read, and syntactically correct code for the full algorithm"] = 4
        assessment["Writes valid, concise, easy to read, and syntactically correct code for the full algorithm"] = "Exceptional: Describes code logic clearly, concisely, and indicates a well-structured algorithm."
    elif code_description_count >= 3 and clarity_count >= 1:
        scores["Writes valid, concise, easy to read, and syntactically correct code for the full algorithm"] = 3
        assessment["Writes valid, concise, easy to read, and syntactically correct code for the full algorithm"] = "Proficient: Describes code logic and implies a reasonably clear and structured algorithm."
    elif code_description_count >= 2:
        scores["Writes valid, concise, easy to read, and syntactically correct code for the full algorithm"] = 2
        assessment["Writes valid, concise, easy to read, and syntactically correct code for the full algorithm"] = "Developing: Attempts to describe code logic but may be unclear, incomplete or lack structure."
    elif code_description_count < 2:
        scores["Writes valid, concise, easy to read, and syntactically correct code for the full algorithm"] = 1
        assessment["Writes valid, concise, easy to read, and syntactically correct code for the full algorithm"] = "Not Demonstrated: Minimal or no description of code logic or algorithm."
    else:
        scores["Writes valid, concise, easy to read, and syntactically correct code for the full algorithm"] = 'N/A' # Should not reach here, but for safety


    # 8. Uses proper indentation to make code readable - N/A from transcript unless code itself is transcribed and analyzed
    scores["Uses proper indentation to make code readable"] = 'N/A'
    assessment["Uses proper indentation to make code readable"] = "N/A: Cannot be assessed from transcript without code."

    # 9. Selects descriptive names for variables/functions that follow standard casing conventions - N/A unless names are explicitly mentioned in transcript
    scores["Selects descriptive names for variables/functions that follow standard casing conventions"] = 'N/A'
    assessment["Selects descriptive names for variables/functions that follow standard casing conventions"] = "N/A: Cannot be assessed from transcript unless variable/function names are mentioned."

    # 10. Manually tests code by verifying output for sample inputs
    testing_keywords = ["test", "example", "try", "run", "input", "output", "expect", "verify", "check", "let's see", "okay", "so if", "then"]
    testing_count = sum(1 for keyword in testing_keywords if keyword.lower() in transcript_text.lower())

    if testing_count >= 3:
        scores["Manually tests code by verifying output for sample inputs"] = 4
        assessment["Manually tests code by verifying output for sample inputs"] = "Exceptional: Thoroughly tests code with multiple sample inputs and verifies outputs."
    elif testing_count >= 2:
        scores["Manually tests code by verifying output for sample inputs"] = 3
        assessment["Manually tests code by verifying output for sample inputs"] = "Proficient: Manually tests code with at least one sample input and verifies output."
    elif testing_count >= 1:
        scores["Manually tests code by verifying output for sample inputs"] = 2
        assessment["Manually tests code by verifying output for sample inputs"] = "Developing: Attempts to test code but may be superficial or output verification is unclear."
    elif testing_count == 0:
        scores["Manually tests code by verifying output for sample inputs"] = 1
        assessment["Manually tests code by verifying output for sample inputs"] = "Not Demonstrated: No manual testing of code mentioned."
    else:
        scores["Manually tests code by verifying output for sample inputs"] = 'N/A'

    # 11. Able to track down bugs effectively without resorting to “guessing” what is wrong
    debugging_keywords = ["debug", "bug", "error", "wrong", "issue", "problem", "fix", "let's see", "check", "examine", "step through", "reason", "logic", "analyze", "investigate"]
    effective_debugging_keywords = ["it seems", "because of", "the issue is", "let's check", "step by step", "logical", "reasoning"]
    guessing_keywords = ["maybe", "perhaps", "guess", "try", "randomly", "just see what happens"]

    debugging_count = sum(1 for keyword in debugging_keywords if keyword.lower() in transcript_text.lower())
    effective_debugging_count = sum(1 for keyword in effective_debugging_keywords if keyword.lower() in transcript_text.lower())
    guessing_count = sum(1 for keyword in guessing_keywords if keyword.lower() in transcript_text.lower())

    if debugging_count >= 2 and effective_debugging_count >= 1 and guessing_count == 0:
        scores["Able to track down bugs effectively without resorting to “guessing” what is wrong"] = 4
        assessment["Able to track down bugs effectively without resorting to “guessing” what is wrong"] = "Exceptional: Demonstrates effective debugging with logical reasoning, avoids guessing."
    elif debugging_count >= 1 and effective_debugging_count >= 1 and guessing_count == 0:
        scores["Able to track down bugs effectively without resorting to “guessing” what is wrong"] = 3
        assessment["Able to track down bugs effectively without resorting to “guessing” what is wrong"] = "Proficient: Demonstrates debugging, shows some logical steps, and avoids guessing."
    elif debugging_count >= 1 and guessing_count == 0:
        scores["Able to track down bugs effectively without resorting to “guessing” what is wrong"] = 2
        assessment["Able to track down bugs effectively without resorting to “guessing” what is wrong"] = "Developing: Attempts debugging but might be somewhat haphazard or lacks clear reasoning."
    elif debugging_count == 0 or guessing_count > 0: # Consider guessing as low score even if debugging is mentioned
        scores["Able to track down bugs effectively without resorting to “guessing” what is wrong"] = 1
        assessment["Able to track down bugs effectively without resorting to “guessing” what is wrong"] = "Not Demonstrated: Limited or ineffective debugging, or resorts to guessing."
    else:
        scores["Able to track down bugs effectively without resorting to “guessing” what is wrong"] = 'N/A'

    # 12. Solution handles edge cases
    edge_case_keywords = ["edge case", "special case", "boundary condition", "corner case", "handle", "deal with", "account for", "what about", "if input is"]
    edge_case_count = sum(1 for keyword in edge_case_keywords if keyword.lower() in transcript_text.lower())

    if edge_case_count >= 3:
        scores["Solution handles edge cases"] = 4
        assessment["Solution handles edge cases"] = "Exceptional: Thoroughly considers and handles multiple edge cases."
    elif edge_case_count >= 2:
        scores["Solution handles edge cases"] = 3
        assessment["Solution handles edge cases"] = "Proficient: Identifies and addresses key edge cases."
    elif edge_case_count >= 1:
        scores["Solution handles edge cases"] = 2
        assessment["Solution handles edge cases"] = "Developing: Mentions edge cases but handling might be incomplete or unclear."
    elif edge_case_count == 0:
        scores["Solution handles edge cases"] = 1
        assessment["Solution handles edge cases"] = "Not Demonstrated: No explicit consideration of edge cases."
    else:
        scores["Solution handles edge cases"] = 'N/A'

    # 13. Verbalizes thought process throughout
    thought_process_keywords = ["because", "so", "therefore", "reasoning", "thinking", "my approach is", "my idea is", "plan is", "step", "next", "then", "first", "second", "initially", "now", "after that"]
    thought_process_count = sum(1 for keyword in thought_process_keywords if keyword.lower() in transcript_text.lower())

    if thought_process_count >= 15: # Adjust threshold based on typical transcript length and desired level
        scores["Verbalizes thought process throughout"] = 4
        assessment["Verbalizes thought process throughout"] = "Exceptional: Consistently and clearly verbalizes thought process throughout the entire interview."
    elif thought_process_count >= 8: # Adjust threshold
        scores["Verbalizes thought process throughout"] = 3
        assessment["Verbalizes thought process throughout"] = "Proficient: Regularly verbalizes thought process, providing good insight into their thinking."
    elif thought_process_count >= 3: # Adjust threshold
        scores["Verbalizes thought process throughout"] = 2
        assessment["Verbalizes thought process throughout"] = "Developing: Sometimes verbalizes thought process, but may be inconsistent or brief."
    elif thought_process_count < 3:
        scores["Verbalizes thought process throughout"] = 1
        assessment["Verbalizes thought process throughout"] = "Not Demonstrated: Minimal or no verbalization of thought process."
    else:
        scores["Verbalizes thought process throughout"] = 'N/A'

    # 14. Uses sufficient vocal volume - N/A from transcript
    scores["Uses sufficient vocal volume"] = 'N/A'
    assessment["Uses sufficient vocal volume"] = "N/A: Cannot be assessed from text transcript."

    # 15. Maintains positive tone and body language throughout - Tone is borderline assessable, body language N/A
    # Assessing tone from text is subjective and unreliable, especially without prosodic features.  Marking as N/A for now for simplicity and reliability.
    scores["Maintains positive tone and body language throughout"] = 'N/A'
    assessment["Maintains positive tone and body language throughout"] = "N/A: Body language and tone (reliably) cannot be assessed from text transcript."

    # 16. Utilizes all available whiteboard space, or includes ample comments if coding remotely - N/A from transcript unless explicitly mentioned
    scores["Utilizes all available whiteboard space, or includes ample comments if coding remotely"] = 'N/A'
    assessment["Utilizes all available whiteboard space, or includes ample comments if coding remotely"] = "N/A: Cannot be assessed from transcript unless explicitly mentioned."


    # --- Determine Pass/Fail ---
    pass_fail = "Pass"
    for criterion_score in scores.values():
        if criterion_score in [1, 2]:
            pass_fail = "Fail"
            break

    analysis_result = {
        "scores": scores,
        "assessment_details": assessment,
        "pass_fail": pass_fail
    }

    return analysis_result


if __name__ == "__main__":
    transcript_file_path = 'interview_transcript.json'  # Use the new transcript file name
    output_file_path = 'analysis_output.json'

    analysis_results = analyze_transcript(transcript_file_path)

    if "error" in analysis_results:
        print(f"Error during analysis: {analysis_results['error']}")
    else:
        with open(output_file_path, 'w') as outfile:
            json.dump(analysis_results, outfile, indent=4)
        print(f"Analysis completed and saved to {output_file_path}")
        print(json.dumps(analysis_results, indent=4)) # Optional: Print to console as well