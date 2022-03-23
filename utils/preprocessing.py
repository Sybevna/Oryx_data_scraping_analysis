from gc import garbage


def cleanup(sentence):
    garbage = [",", ":", "(", ")"]
    for x in garbage:
        sentence = sentence.replace(x, "")
    return sentence.split()
