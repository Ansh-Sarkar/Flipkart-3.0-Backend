def get_local_variables():
    file = open("LOCAL.abx")
    d = {}
    temp_data = file.readlines()
    temp_pure = []
    for token in temp_data:
        if token == '':
            continue
        token = token.strip()
        token = token.split(":")
        d[token[0].strip()] = ''.join(token[1:]).strip()
    return d


def update_local_variables(LOCAL_VARS, CHANGE_IN_LOCAL_VARIABLES):
    if CHANGE_IN_LOCAL_VARIABLES:
        file = open("LOCAL.abx", "w")
        for variable in LOCAL_VARS:
            file.write("{variable} : {value}\n".format(
                variable=variable, value=LOCAL_VARS[variable]))
        file.close()
    return 'updated'
