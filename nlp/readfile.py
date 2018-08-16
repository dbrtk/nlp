

import os


def readfile(filename):
    lines = [line for line in open(filename, 'r').readlines()]

    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:

        if not line.strip():
            print('das')
            continue
        p = line.strip().split('\t')
        rownames.append(p[0])

        print(p)
        print(len(p))
        print(p[1:])
        print('\n')
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def main():
    _ = '/home/dominik/Desktop/wiki/wikipedia/'
    corpus_path = os.path.normpath(os.path.abspath(_))
    if not os.path.isdir(corpus_path):
        raise ValueError(corpus_path)
    _file = os.path.normpath(os.path.join(corpus_path, os.listdir(_)[88]))

    rows, cols, data = readfile(_file)
    print('\n\n\n')
    print(rows)
    print(len(rows))
    # print(cols)
    print(data)

    print('done')


if __name__ == "__main__":
    main()
