

import os


def readfile(filename):
    lines = [line for line in open(filename, 'r').readlines()]

    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:

        if not line.strip():
            continue
        p = line.strip().split('\t')
        rownames.append(p[0])

        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def main():
    _ = '/path/to/corpus'
    corpus_path = os.path.normpath(os.path.abspath(_))
    if not os.path.isdir(corpus_path):
        raise ValueError(corpus_path)
    _file = os.path.normpath(os.path.join(corpus_path, os.listdir(_)[88]))

    rows, cols, data = readfile(_file)


if __name__ == "__main__":
    main()
