import tensorflow as tf
import os


path = os.path.join('./data', "model")  

def recommendation(user_id: str):
    loaded = tf.saved_model.load(path)
    id = int(user_id)
    scores, titles = loaded([id])
 
    return titles.numpy().tolist()
    