from pyprojroot import here
from create_session_and_talk_turn_objects import TalkTurn, Transcript 
import pdb
import pickle
import os
from transformers import pipeline, AutoTokenizer

def check_talkturn_token_size(talkturn_text, tokenizer):
    encoded_talkturn = tokenizer(talkturn_text, return_tensors='pt')
    num_tokens = encoded_talkturn['input_ids'].shape[1]
    return num_tokens

def trim_talkturn_token_size(talkturn_text, tokenizer, max_token_size = 511):
    if check_talkturn_token_size(talkturn_text, tokenizer) <= max_token_size:
        return talkturn_text
    else:
        reduced_talkturn = " ".join(talkturn_text.split(" ")[2:]) # remove first two words and try again (get recursion depth errors in some transcripts if only doing 1)
        return trim_talkturn_token_size(reduced_talkturn, tokenizer, max_token_size)
    

if __name__ == "__main__":
    root_dir = str(here())
    pickle_file = os.sep.join([root_dir,'extractedData','transcript_python_objects.pkl'])

    with open(pickle_file, 'rb') as file:
        data = pickle.load(file)

    sentiment_analysis_model = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(sentiment_analysis_model)
    # https://arxiv.org/abs/2202.03829

    sentiment_task = pipeline("sentiment-analysis", model=sentiment_analysis_model)
 
    #data is a list of Transcript objects
    for transcript_obj in data:
        print("starting " + transcript_obj.filepath)
        for talkturn_obj in transcript_obj.talkturns:
            talkturn_content = trim_talkturn_token_size(talkturn_obj.content, tokenizer)
            #add sentiment analysis result to talkturn
            #print(talkturn_content)
            result = sentiment_task(talkturn_content)
            #print(result)
            talkturn_obj.sentiment_analysis_result = result

    with open(os.sep.join([root_dir,'extractedData','transcript_python_objects_with_sentiment.pkl']), 'wb') as file:
        # Dump the object into the file
        pickle.dump(data, file)

    pdb.set_trace()