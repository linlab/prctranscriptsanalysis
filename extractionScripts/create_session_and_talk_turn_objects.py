from pyprojroot import here
import glob
import pdb
import re
import pickle
import os

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
        
        #self.therapist_id = "unknown"
        self.patient_id     = filepath.split(os.sep)[-1][0:2]
        self.session_number = int(filepath.split(os.sep)[-1][2:6])

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
                    print("no speaker identified in case {0} session {1}, line {2}: {3}".format(self.patient_id, self.session_number, linenum, linestrip))
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

# possible later to do: create function to remove parentheticals from within string? e.g. (laughs)

# Example usage
if __name__ == "__main__":
    root_dir = str(here())
    transcript_files = glob.glob(os.sep.join([root_dir,'rawData','case_A2','A2*.txt'])) 

    list_of_transcript_objs = []
    for f in transcript_files:
        transcript_obj = Transcript(f)
        list_of_transcript_objs.append(transcript_obj)

    # Open a file in binary write mode ('wb')
    with open(os.sep.join([root_dir,'extractedData','transcript_python_objects.pkl']), 'wb') as file:
        # Dump the object into the file
        pickle.dump(list_of_transcript_objs, file)

#    pdb.set_trace()