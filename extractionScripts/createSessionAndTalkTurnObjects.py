from pyprojroot import here
import pdb
import re
import pickle

class TalkTurn:
    def __init__(self, speaker: str, content: str):
        """
        Initialize a TalkTurn instance.

        speaker: The identity of the person talking (e.g., "therapist" or "patient").
        content: The content of what they said.
        """
        self.speaker = speaker
        talking_content, annotations = split_bracketed_text(content)
        self.annotations = annotations
        self.content = talking_content
        self.num_words = len(talking_content.split())

    def __repr__(self):
        return f"TalkTurn(speaker='{self.speaker}', num_words={self.num_words}, content='{self.content[:30]}')"


class Transcript:
    def __init__(self, filepath: str):
        """
        Initialize a Transcript instance.

        filepath: The file path of the transcript.
        talkturns: A list of TalkTurn instances representing the conversation.
        """
        self.filepath = filepath
        #for line in open(filepath) make the talk turns then append them to list
        talk_turn_list = []

        with open(filepath, 'r', encoding = 'utf-8') as f:
            linenum = 0
            for line in f:
                line_rm_num = remove_leading_number(line)
                linestrip = line_rm_num.strip()
                if linestrip == "":
                	continue
                	linenum += 1
                if linestrip.startswith("T:") or linestrip.startswith("A:"):
                    speaker = "therapist"
                    talkturn_text = remove_leading_speakerID(linestrip)
                    talkturn_obj = TalkTurn(speaker, talkturn_text)
                    talk_turn_list.append(talkturn_obj)
                elif linestrip.startswith("P:"):
                    speaker = "patient"
                    talkturn_text = remove_leading_speakerID(linestrip)
                    talkturn_obj = TalkTurn(speaker, talkturn_text)
                    talk_turn_list.append(talkturn_obj)
                else:
                    print("no speaker identified in line {0}: {1}".format(linenum, linestrip))
                linenum += 1

        self.talkturns = talk_turn_list

        #self.talkturns = talkturns
        self.num_therapist_turns = sum(1 for turn in talk_turn_list if turn.speaker == 'therapist')
        self.num_patient_turns = sum(1 for turn in talk_turn_list if turn.speaker == 'patient')

    def __repr__(self):
        return (f"Transcript(filepath='{self.filepath}', num_therapist_turns={self.num_therapist_turns}, "
                f"num_patient_turns={self.num_patient_turns}, total_turns={len(self.talkturns)})")

def remove_leading_number(input_string: str) -> str:
    # Regex pattern to match a leading number followed by any whitespace
    pattern = r'^\d+\s*'
    
    # Substitute the pattern with an empty string, effectively removing it
    result = re.sub(pattern, '', input_string)
    
    return result

def remove_leading_speakerID(input_string: str) -> str:
    # Regex pattern to match a speaker annotation followed by any whitespace
    pattern = r'^(T:|A:|P:)\s*'
    
    # Substitute the pattern with an empty string, effectively removing it
    result = re.sub(pattern, '', input_string)
    
    return result

def split_bracketed_text(input_string: str):
    # Regex pattern to match text in brackets at the end of the string
    pattern = r'(.*?)(\[(.*?)\])?$'
    
    # Perform the regex search
    match = re.match(pattern, input_string)
    
    # Extract the non-bracketed part and the bracketed part (if any)
    non_bracketed_text = match.group(1).strip()
    bracketed_text = match.group(3) if match.group(3) else ""
    
    return non_bracketed_text, bracketed_text

# possible to do: create function to remove parenthetical from a string? e.g. (laughs)

# Example usage
if __name__ == "__main__":
 
    test_file = r"C:\Users\erk\Dropbox\Eric\Sinai\research\psychotherapy_process\sentiment_analysis\rawData\session_1.txt"

    transcript_obj = Transcript(test_file) 

    print(transcript_obj)

    for turn in transcript_obj.talkturns:
        print(turn)

    pdb.set_trace()

    # Open a file in binary write mode ('wb')

    #with open('my_object.pkl', 'wb') as file:
    #    # Dump the object into the file
    #    pickle.dump(my_object, file)