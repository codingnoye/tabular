def get_data(filename):
    size = 0
    minterms = []
    dontcares = []
    status = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line[0] == '!': status+=1
            elif status == 0: size = int(line)
            elif status == 1: minterms.append(int(line))
            else: dontcares.append(int(line))

    return size, minterms, dontcares

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

class implicant:
    def __init__(self, ones, minterms, binarr, combined):
        self.ones = ones
        self.minterms = minterms
        self.binarr = binarr
        self.combined = combined

def make_table(minterms, dontcares, size):
    return [
        implicant(get_ones(minterm, size), [minterm], to_binarr(minterm, size), False)
        for minterm in minterms+dontcares
    ]

def merge_imps(imp1, imp2):
    imp1.combined = True
    imp2.combined = True

    return implicant(
        min(imp1.ones, imp2.ones),
        imp1.minterms + imp2.minterms,
        [2 if imp1.binarr[i]!=imp2.binarr[i] else imp1.binarr[i] for i in range(len(imp1.binarr))],
        False
    )

def hamming_distance(imp1, imp2):
    dist = 0
    for i in range(len(imp1.binarr)): dist += 1 if imp1.binarr[i] != imp2.binarr[i] else 0

    return dist

def trinory(binarr):
    res = 0
    for i in range(len(binarr)):
        res += binarr[-i-1] * (3**i)

    return res

def make_PIs(table):
    if len(table) <= 1: return table
    newTable = []
    newTableChecked = set()
    table_ones = []

    for imp in table:
        if len(table_ones) <= imp.ones: table_ones.append([imp])
        else: table_ones[imp.ones].append(imp)

    for i in range(len(table_ones)-1):
        for imp1 in table_ones[i]:
            for imp2 in table_ones[i+1]:
                if hamming_distance(imp1, imp2) == 1:
                    merged = merge_imps(imp1, imp2)
                    tri = trinory(merged.binarr)
                    if tri not in newTableChecked:
                        newTable.append(merged)
                        newTableChecked.add(tri)

    res = []
    for imp in table:
        if not imp.combined: res.append(imp)

    return res + make_PIs(newTable) 

def find_EPIs(table, minterms, dontcares):
    minterm_count = {}
    EPIs = []
    EPIsCheck = set()

    for minterm in minterms:
        minterm_count[minterm] = 0

    for imp in table:
        for minterm in imp.minterms:
            if minterm in minterms:
                minterm_count[minterm] += 1

    for minterm in minterm_count:
        if minterm_count[minterm] == 1:
            for imp in table:
                if minterm in imp.minterms:
                    tri = trinory(imp.binarr)
                    if tri not in EPIsCheck:
                        EPIs.append(imp)
                        EPIsCheck.add(tri)
                    break
    
    return EPIs

if __name__ == '__main__':
    size, minterms, dontcares = get_data('input.txt')
    draw_line()
    print('step 0. 값 읽어오기')
    print(f'size : {size}')
    print(f'minterms : {minterms}')
    print(f'dontcares : {dontcares}')

    table = make_table(minterms, dontcares, size)
    table_PI = make_PIs(table)
    draw_line()
    print('step 1. PI 리스트 찾기')
    print(list(map(lambda imp: imp.minterms, table_PI)))

    EPIs = find_EPIs(table_PI, minterms, dontcares)
    draw_line()
    print('step 2. EPI 리스트 찾기')
    print(list(map(lambda imp: imp.minterms, EPIs)))