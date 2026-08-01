def parse_response(response_text):
    parts = response_text.split("Confidence:")
    
    answer = parts[0].strip()
    
    if len(parts) > 1:
        confidence_and_reasoning = parts[1].split("\n", 1)
        confidence_level = confidence_and_reasoning[0].strip()
        
        if len(confidence_and_reasoning) > 1:
            reasoning = confidence_and_reasoning[1].strip()
        else:
            reasoning = ""
    else:
        confidence_level = "UNKNOWN"
        reasoning = ""
    
    return answer, confidence_level, reasoning


if __name__ == "__main__":
    
    sample = """Here's the answer to your question about networking protocols.

                Confidence: HIGH
                I am confident because the context explicitly mentions these protocols."""
    
    answer, confidence_level, reasoning = parse_response(sample)
    
    print(f"ANSWER:\n{answer}\n")
    print(f"CONFIDENCE:\n{confidence_level}\n")
    print(f"REASONING:\n{reasoning}")