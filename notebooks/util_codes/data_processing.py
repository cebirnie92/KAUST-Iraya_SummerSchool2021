import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences

def remove_stopwords(text,stopwords_list):
    '''
    Remove commonly used words that doesn't add value/meaning to our text (ex."a","an","the") 
    '''
    text = text.lower()
    for word in stopwords_list:
        token = " "+word+" "
        text = text.replace(token," ")
        text = text.replace("  "," ")
    return text


def target_to_array(x,n_class):
    """
    transform categories to array
    """
    y = [0]*n_class
    y[x] = 1
    return y

def load_data(csv_file):
    """
    reads the csv file and transform the data to a pandas dataframe
    """
    target_dictionary = {'Geophysics':0,'Petrophysics':1,'Geology':2,'Geomodelling':3,'Production':4}
    df_data = pd.read_csv(csv_file,encoding ='utf8',engine='python')
    if 'classification' in list(df_data):
        n_class = len(set(df_data.classification.values))
        df_data['target'] = df_data['classification'].apply(lambda x: target_dictionary[x]) #change classification to int
        df_data['target_pred'] = df_data['target'].apply(lambda x: target_to_array(x,n_class)) #change int to one-hot encoding
        df_data = df_data[~(df_data['target']==-1)] # remove Nan classification
    return df_data

def featurize(dataframe,stopwords_list,tokenizer,max_len,trunc_type,padding_type):
    """
    converts text to vectors
    """
    dataframe['token']  = dataframe['doc_title'].apply(lambda x: remove_stopwords(x,stopwords_list))
    title_sequence = tokenizer.texts_to_sequences(dataframe.token)
    padded_vectors = pad_sequences(title_sequence,
                maxlen=max_len,
                truncating=trunc_type,
                padding=padding_type)
    dataframe['sequences'] = title_sequence
    dataframe['features'] = list(padded_vectors)
    if 'classification' in list(dataframe):
        return dataframe[['doc_index','features','classification','target_pred']]
    else:
        return dataframe[['doc_index','features']]