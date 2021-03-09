import string

from nltk.corpus import stopwords
import nltk


def create_context(text, nasari):
    """
    It creates a list of Nasari vectors (a list of {term:score}). Every vector
    is linked to one text term.
    :param text: the list of text's terms
    :param nasari: Nasari dictionary
    :return: list of Nasari's vectors.
    """

    tokens = aux_bag_of_word(text)
    vectors = []
    #per ogni parola pulita rimasta nel paragrafo
    for word in tokens:
        if word in nasari.keys():
            vectors.append(nasari[word])    #prendiamo il vettore associato alla parola

    return vectors


def get_title_topic(document, nasari):
    """
    Creates a list of Nasari vectors based on the document's title.
    :param document: input document
    :param nasari: Nasari dictionary
    :return: a list of Nasari vectors.
    """

    title = document[0]
    tokens = aux_bag_of_word(title)
    #print("Token: ", tokens)
    vectors = aux_create_vectors(tokens, nasari)
    #print("Vetors: ", vectors)
    return vectors


def aux_bag_of_word(text):
    """
    Support function, it returns the Bag of Word representation fo the given text.
    It applies lemmatization, removes the punctuation, the stop-words and duplicates.
    :param text: input text
    :return: Bag of Words representation of the text.
    """

    text = text.lower()
    stop_words = set(stopwords.words('english'))
    wnl = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    tokens = list(filter(lambda x: x not in stop_words and x not in string.punctuation, tokens))
    return set(wnl.lemmatize(t) for t in tokens)


def aux_create_vectors(topic, nasari):
    """
    Auxiliary function of get_title_topic().
    It creates a list of Nasari vectors (a list of {term:score}). Every vector
    is linked to one topic term.
    :param topic: the list of topic's terms
    :param nasari: Nasari dictionary
    :return: list of Nasari's vectors.
    """

    vectors = []
    for word in topic:
        if word in nasari.keys():
            vectors.append(nasari[word])

    return vectors
