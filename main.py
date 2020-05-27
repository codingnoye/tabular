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
    return binarr

def get_ones(minterm, size):
    ones = 0
    for i in range(size):
        ones += minterm>>i&1
    return ones

def make_table(minterms, size):
    table = []
    for minterm in minterms:
        row = [
            get_ones(minterm, size), # number of 1s
            [minterm], # merged minterms
            to_binarr(minterm, size), # binarr, - is 2
            False # combined
        ]
        table.append(row)
    return table

def merge_rows(row1, row2):
    row1[3] = True
    row2[3] = True
    return [
        min(row1[0], row2[0]),
        row1[1]+row2[1],
        [2 if row1[2][i]!=row2[2][i] else row1[2][i] for i in range(len(row1[2]))],
        False
        ]

def hamming_distance(binarr1, binarr2):
    dist = 0
    for i in range(len(binarr1)): dist += 1 if binarr1[i] != binarr2[i] else 0
    return dist

def trinory(binarr):
    res = 0
    for i in range(len(binarr)):
        res += binarr[-i-1] * (3**i)
    return res

def get_PIs(table):
    if len(table) <= 1: return table
    newTable = []
    newTableChecked = set()
    table_ones = []
    for row in table:
        if len(table_ones) <= row[0]: table_ones.append([row])
        else: table_ones[row[0]].append(row)
    for i in range(len(table_ones)-1):
        for row1 in table_ones[i]:
            for row2 in table_ones[i+1]:
                if hamming_distance(row1[2], row2[2]) == 1:
                    merged = merge_rows(row1, row2)
                    tri = trinory(merged[2])
                    if tri not in newTableChecked:
                        newTable.append(merged)
                        newTableChecked.add(tri)
    res = []
    for row in table:
        if not row[3]: res.append(row)
    return res + get_PIs(newTable) 

if __name__ == '__main__':
    # step 1: read minterm data from file
    data = get_data('input.txt')
    size = data[0]
    minterms = data[1:]
    print(f'size : {size}')
    print(f'minterms : {minterms}')
    draw_line()

    table = make_table(minterms, size)
    print(list(map(lambda row: row[1], get_PIs(table))))