import re

def get_score(words, scores_dict):
    result = 0
    for word in words:
        result += scores_dict[word]
    return result

def get_matches(message, word_list):
    return re.findall(f'({"|".join(word_list)})', message)