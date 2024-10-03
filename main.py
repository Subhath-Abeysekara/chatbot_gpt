import json
import sys
from io import BytesIO

from firebase import download_directory_from_firebase

sys.path.append('../../entities')
sys.path.append('../../enums')
sys.path.append('../../models')

from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel, GPT2TokenizerFast, GPT2Tokenizer

def load_model(model_path):
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return model


def load_tokenizer(tokenizer_path):
    tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
    return tokenizer

def generate_text(model_path, sequence, max_length):

    model = load_model(model_path)
    print("model")
    tokenizer = load_tokenizer(model_path)
    ids = tokenizer.encode(f'{sequence}', return_tensors='pt')
    final_outputs = model.generate(
        ids,
        do_sample=True,
        max_length=max_length,
        pad_token_id=model.config.eos_token_id,
        top_k=50,
        top_p=0.95,
    )
    print(tokenizer.decode(final_outputs[0], skip_special_tokens=True))
    return tokenizer.decode(final_outputs[0], skip_special_tokens=True)

def testing_api(event):
    try:
        body = event['body']
        model1_path = "models"
        sequence1 = "What is this Clothing Center? "
        def document_question(sequence):
            max_len = 50
            return generate_text(model1_path, sequence, max_len)
        document_question(sequence1)
        response = {
            'message': "success",
            "answer":"Hello",
            "body":body
        }
        print(response)
    except Exception as e:
        print(str(e))

event = {
    "body" : {
        "message":"body"
    }
}
download_directory_from_firebase("chatbot/")
testing_api(event)
