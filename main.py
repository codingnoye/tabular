def get_data(filename):
    with open(filename, 'r') as f:
        data = list(map(int, f.readline().split()))
        return data

def draw_line():
    print("===============================")

def to_binarr(minterm, size):
    binarr = []
    for i in range(size):
        binarr = [minterm>>i&1] + binarr
    print(f'{minterm} -> {binarr}')
    return binarr

def get_ones(minterm, size):
    ones = 0
    for i in range(size):
        ones += minterm>>i&1
    print(f'{minterm} -> ones {ones}')
    return ones

def make_table(minterms, size):
    table = []
    for minterm in minterms:
        row = [
            get_ones(minterm), # number of 1's
            [minterm], # merged minterms
            to_binarr(minterm), # binarr, - is -1
            False # combined
        ]

if __name__ == '__main__':
    # step 1: read minterm data from file
    data = get_data('input.txt')
    size = data[0]
    minterms = data[1:]
    print(f'size : {size}')
    print(f'minterms : {minterms}')
    draw_line()
    to_binarr(5, size)
