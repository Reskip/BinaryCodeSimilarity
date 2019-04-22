import sql_utils

def process():
    sql = sql_utils.SQL.instance()
    num = sql.get_train_num()
    arm_train = open("data/vector/arm_train.tsv", "w")
    x86_train = open("data/vector/x86_train.tsv", "w")

    offset = 0
    while offset < num:
        train = sql.fetch_train(100, offset)
        offset += 100
        for sample in train:
            x86_train.write(sample[2].replace("\n", "\t") + "\n")
            arm_train.write(sample[3].replace("\n", "\t") + "\n")

    arm_train.close()
    x86_train.close()
    return