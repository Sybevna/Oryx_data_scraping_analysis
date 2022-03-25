from gc import garbage


def cleanup(sentence):
    garbage = [",", ":", "(", ")", "of which", "-"]
    for x in garbage:
        sentence = sentence.replace(x, "")
    return sentence.split()


def create_dfs(data):
    possible_states = ["destroyed", "damaged", "abandoned", "captured"]
    final = {"Russia": {}, "Ukraine": {}}
    country = "Russia"
    for x in data:
        i = 0
        while x[i].isnumeric() == False:
            i += 1
        name = " ".join(x[:i])
        if name == "Ukraine":
            country = name
        final[country][name] = {"total": int(x[i])}
        for state in possible_states:
            try:
                ind = x.index(state)
                final[country][name][state] = int(x[ind + 1])
            except:
                final[country][name][state] = 0
    for x in final.keys():
        final[x] = pd.DataFrame(final[x]).T
    return final
