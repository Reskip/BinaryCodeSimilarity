from os.path import join
from random import randint

DATADIR = "data/vector"
MODELDIR = "data/model/lstm_siam"
NEG_NUM = 3

def merge_vector():
    x86_embedding = open(join(DATADIR, "x86_embedding.tsv"))
    arm_embedding = open(join(DATADIR, "arm_embedding.tsv"))

    merged = open(join(MODELDIR, "wordvector.tsv"), "w")
    merged.write(x86_embedding.read())
    merged.write(arm_embedding.read())
    x86_embedding.close()
    arm_embedding.close()
    merged.close()
    return

def format(train_data):
    train_data = train_data.split("\n")
    train_data = [s.replace("\t", " ") for s in train_data]
    return train_data

def write_train(train, x, y, label):
    train.write("%s\t%s\t%d\n" % (x, y, label))
    return

def generate_train_data():
    x86_train = open(join(DATADIR, "x86_train.tsv")).read()
    arm_train = open(join(DATADIR, "arm_train.tsv")).read()

    train = open(join(MODELDIR, "train_data.tsv"), "w")
    x86_train = format(x86_train)
    arm_train = format(arm_train)
    for i in range(len(x86_train)):
        write_train(train, x86_train[i], arm_train[i], 1)
        neg_label = [randint(0, len(x86_train)-1) for i in range(NEG_NUM)]
        for neg in neg_label:
            if neg == i:
                continue
            write_train(train, x86_train[i], arm_train[neg], 0)
    train.close()
    return

if __name__ == "__main__":
    merge_vector()
    generate_train_data()