from pyprojroot import here
from create_session_and_talk_turn_objects import TalkTurn, Transcript 
import pdb
import pickle
import os


if __name__ == "__main__":
    root_dir = str(here())
    pickle_file = os.sep.join([root_dir,'extractedData','transcript_python_objects_with_sentiment.pkl'])
    output_file = os.sep.join([root_dir,'extractedData','all_talkturns_with_sentiment_scores.tsv'])

    with open(pickle_file, 'rb') as file:
        data = pickle.load(file)


    #data is a list of Transcript objects
    with open(output_file, 'w') as fout:
        fout.write('\t'.join(['treatment_ID', 'session_number', 'patient_or_therapist', 'talkturn_sentiment_label', 'talkturn_sentiment_score', 'talkturn_content', 'talkturn_num_words'])+'\n')

        for transcript_obj in data:
            for talkturn_obj in transcript_obj.talkturns:
                fout.write('\t'.join(map(str, [transcript_obj.patient_id, transcript_obj.session_number, talkturn_obj.speaker, talkturn_obj.sentiment_analysis_result[0]['label'], talkturn_obj.sentiment_analysis_result[0]['score'], talkturn_obj.content, talkturn_obj.num_words]))+'\n')

