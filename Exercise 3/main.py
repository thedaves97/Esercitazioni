from pathlib import Path
from functions2 import *


def compute_overlap(topic, paragraph):
    """
    Support function used in Weighted Overlap's function below.
    :param topic: Vector representation of the topic
    :param paragraph: Vector representation of the paragraph
    :return: intesection between the given parameters
    """

    return topic & paragraph


def rank(vector, nasari_vector):
    """
    Computes the rank of the given vector.
    :param vector: input vector
    :param nasari_vector: input Nasari vector
    :return: vector's rank (position inside the nasari_vector)
    """

    for i in range(len(nasari_vector)):
        if nasari_vector[i] == vector:
            return i + 1


def weighted_overlap(topic_nasari_vector, paragraph_nasari_vector):
    """
    Implementation of the Weighted Overlap metrics
    :param topic_nasari_vector: Nasari vector representing the topic
    :param paragraph_nasari_vector: Nasari vector representing the paragraph
    :return: square-rooted Weighted Overlap if exist, 0 otherwise.
    """

    overlap_keys = compute_overlap(topic_nasari_vector.keys(),
                                   paragraph_nasari_vector.keys())
    #print("OK: ", overlap_keys)
    overlaps = list(overlap_keys)

    if len(overlaps) > 0:
        # sum 1/(rank() + rank())
        den = sum(1 / (rank(q, list(topic_nasari_vector)) +
                       rank(q, list(paragraph_nasari_vector))) for q in overlaps)
        #NB: num e den invertiti
        # sum 1/(2*i)
        num = sum(list(map(lambda x: 1 / (2 * x), list(range(1, len(overlaps) + 1)))))

        return den / num

    return 0


def get_nasari():
    """
    It takes the Nasari input file, and it converts into a Python dictionary.
    :return: a dictionary representing the Nasari input file. Fomat: {word: {term:score}}
    """

    nasari_dict = {}
    with open("utils/dd-small-nasari-15.txt", 'r', encoding="utf8") as file:
        for line in file.readlines():
            splits = line.split(";")
            vector_dict = {}

            for term in splits[2:]:
                k = term.split("_")
                if len(k) > 1:
                    vector_dict[k[0]] = k[1]

            nasari_dict[splits[1].lower()] = vector_dict

    return nasari_dict


def summarization(document, nasari_dict, percentage):
    """
    Applies summarization to the given document, with the given percentage.
    :param document: the input document
    :param nasari_dict: Nasari dictionary
    :param percentage: reduction percentage
    :return: document summarized.
    """

    topics = get_title_topic(document, nasari_dict)

    paragraphs = []
    i = 0
    # for each paragraph, except the title (document[0])
    for paragraph in document[1:]:
        context = create_context(paragraph, nasari_dict)
        #print(context)
        paragraph_wo = 0
        for word in context:
            #print(word)
            # Computing WO for each word inside the paragraph.
            topic_wo = 0
            for vet in topics:
                #print("Vector: ", vet)
                topic_wo = topic_wo + weighted_overlap(word, vet)
            if topic_wo != 0:
                topic_wo = topic_wo / len(topics)

            # Sum all words WO in the paragraph's WO
            paragraph_wo += topic_wo

        if len(context) > 0:
            paragraph_wo = paragraph_wo / len(context)

            paragraphs.append((i, paragraph_wo, paragraph))

        i += 1

    keep_lines = len(paragraphs) - int(round((percentage / 100) * len(paragraphs), 0))
    #print("PAR: ", paragraphs)

    new_doc = sorted(paragraphs, key=lambda x: x[1], reverse=True)[:keep_lines]
    #Restore the original order.
    #print("SCORE WISE ", new_doc)
    new_doc = sorted(new_doc, key=lambda x: x[0], reverse=True)
    #print("ROW WISE ", new_doc)

    new_doc = list(map(lambda x: x[2], new_doc))
    #print("FINAL ", new_doc)

    new_doc = [document[0]] + new_doc
    return new_doc


def parse_document(file):
    """
    It parse the given document.
    :param file: input document
    :return: a list of all document's paragraph.
    """

    document = []
    data = file.read_text(encoding='utf-8')
    lines = data.split('\n')

    for line in lines:
        if line != '' and '#' not in line:
            line = line[:-1]  # deletes the final "\n" character.
            document.append(line)

    return document


if __name__ == "__main__":

    percentage = int(input("Choose how much you want to reduce the file (10, 20, 30)%: "))
    print("Summarization.\nReduction %: ", percentage, " %")

    nasari_dict = get_nasari()

    #files_documents = ["Andy-Warhol", "Ebola-virus-disease", "Life-indoors", "Napoleon-wiki"]
    files = Path('Input/').glob('*.txt')

    for file in files:
        document = parse_document(file)

        summary = summarization(document, nasari_dict, percentage)

        with open("output/" + str(percentage) + '-' + file.name,
                  'w', encoding='utf-8') as out:
            for paragraph in summary:
                out.write(paragraph + '\n')
