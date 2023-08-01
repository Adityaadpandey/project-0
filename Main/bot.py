from transformers import AutoModelForCausalLM, AutoTokenizer
import torch 

# padding_side='left',

tokenizer = AutoTokenizer.from_pretrained("DingleyMaillotUrgell/homer-bot")
model = AutoModelForCausalLM.from_pretrained("DingleyMaillotUrgell/homer-bot")

# Let's chat for 5 lines
def chatbot(intpt):
    for step in range(50):
        # step = 50
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(intpt + tokenizer.eos_token, return_tensors='pt')
    
        # padding_side='left'
        # append the new user input tokens to the chat history
        # bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) 
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(
            bot_input_ids, 
            max_length=10000,               
            pad_token_id=tokenizer.eos_token_id,  
            no_repeat_ngram_size=3,
            do_sample=True, 
            top_k=100, 
            top_p=0.7,
            temperature = 0.9
        )

        
        # print last outpput tokens from bot
        respond = ("Homer: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
        return respond

while True:
    intpt = input("You: ")
    print(chatbot(intpt))