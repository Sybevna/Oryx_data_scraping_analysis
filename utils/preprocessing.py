import pandas as pd


def cleanup(sentence):
    garbage = [",", ":", "(", ")", "of which", "-"]
    for x in garbage:
        sentence = sentence.replace(x, "")
    return sentence.split()


def create_dfs(data):
    possible_states = ["destroyed", "damaged", "abandoned", "captured"]
    final = {"Russia": {}, "Ukraine": {}}  # Initialise dict
    country = "Russia"  # Start with russia first
    for x in data:  # iterate on the whole dataset given to the function
        i = 0
        while x[i].isnumeric() == False:  # check where the numeric character starts
            # everything before that is the name we'll want to join
            i += 1
        name = " ".join(x[:i])  # Join operation
        if (
            name == "Ukraine"
        ):  # Change case if we reach the point where ukraine data starts
            country = name
        final[country][name] = {"Total": int(x[i])}  # Add total + value to dic
        for state in possible_states:  # iterate on all possible states
            try:
                ind = x.index(state)  # check if the state is present in data
                final[country][name][state] = int(
                    x[ind + 1]
                )  # if it is, add the next values
            except:
                final[country][name][state] = 0  # if it's not, set to 0
    for x in final.keys():
        final[x] = pd.DataFrame(final[x]).T.rename(
            columns={
                "destroyed": "Destroyed",
                "damaged": "Damaged",
                "abandoned": "Abandoned",
                "captured": "Captured",
            },
            index={x: "All equipments"},
        )  # Turn into DFs

    return final
