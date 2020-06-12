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

    return size, set(minterms), set(dontcares)

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
        self.temp_minterms = set()
        self.name = ''

def make_table(minterms, dontcares, size):
    return [
        implicant(get_ones(minterm, size), {minterm}, to_binarr(minterm, size), False)
        for minterm in minterms | dontcares
    ]

def merge_imps(imp1, imp2):
    imp1.combined = True
    imp2.combined = True

    return implicant(
        min(imp1.ones, imp2.ones),
        imp1.minterms | imp2.minterms,
        [2 if imp1.binarr[i]!=imp2.binarr[i] else imp1.binarr[i] for i in range(len(imp1.binarr))],
        False
    )

def hamming_distance(imp1, imp2):
    dist = 0
    for i in range(len(imp1.binarr)): dist += 1 if imp1.binarr[i] != imp2.binarr[i] else 0

    return dist

def trinary(binarr):
    res = 0
    for i in range(len(binarr)):
        res += binarr[-i-1] * (3**i)

    return res

def make_PIs(table):
    if len(table) <= 1: return table
    newTable = []
    newTableChecked = set()
    table_ones = [[] for i in range(len(table[0].binarr)+1)]
    for imp in table:
        table_ones[imp.ones].append(imp)
    for i in range(len(table_ones)-1):
        for imp1 in table_ones[i]:
            for imp2 in table_ones[i+1]:
                if hamming_distance(imp1, imp2) == 1:
                    merged = merge_imps(imp1, imp2)
                    tri = trinary(merged.binarr)
                    if tri not in newTableChecked:
                        newTable.append(merged)
                        newTableChecked.add(tri)

    res = []
    for imp in table:
        if not imp.combined:
            res.append(imp)

    return res + make_PIs(newTable) 

def binarr_str(binarr):
    res = ''
    for i in binarr:
        res += f'{i if i!=2 else "-"}, '
    return res[:-2]

def draw_PIs(table, minterms, dontcares = set()):
    th = '%-27s' % 'Prime Implecants'
    terms = minterms | dontcares
    for term in terms:
        th += '| %-4s ' % term if term in minterms else '| %-4s ' % f'({term})'
    print(th)
    
    for imp in table:
        tr = '%-27s' % f'{imp.name} = {binarr_str(imp.binarr)}'
        for term in terms:
            tr += '| %-4s ' % ('V' if term in imp.minterms else ' ')
        print(tr)

def find_EPIs(table, minterms, dontcares = set()):
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
                    tri = trinary(imp.binarr)
                    if tri not in EPIsCheck:
                        EPIs.append(imp)
                        EPIsCheck.add(tri)
                    break
    
    return EPIs

def row_dominance(table, minterms):
    minterm_set = set(minterms)
    for imp in table:
        imp.temp_minterms = imp.minterms & minterm_set
    for i in range(len(table)):
        if table[i].combined:
            continue
        for j in range(i+1, len(table)):
            if table[j].combined:
                continue
            if table[i].temp_minterms.issubset(table[j].temp_minterms):
                table[i].combined = True
            elif table[j].temp_minterms.issubset(table[i].temp_minterms):
                table[j].combined = True
    return list(filter(lambda imp: not imp.combined, table))

def column_dominance(table, minterms):
    minterm_sets = dict()
    lminterms = list(minterms)
    for minterm in minterms:
        minterm_sets[minterm] = [set(), False]
    for imp in table:
        for minterm in imp.minterms:
            if minterm in minterms:
                minterm_sets[minterm][0].add(imp.name)
    for i in range(len(minterms)):
        if minterm_sets[lminterms[i]][1]:
            continue
        for j in range(i+1, len(minterms)):
            if minterm_sets[lminterms[j]][1]:
                continue
            if minterm_sets[lminterms[i]][0].issubset(minterm_sets[lminterms[j]][0]):
                minterm_sets[lminterms[j]][1] = True
            elif minterm_sets[lminterms[j]][0].issubset(minterm_sets[lminterms[i]][0]):
                minterm_sets[lminterms[i]][1] = True
    minterms_alive = set(filter(lambda minterm: not minterm_sets[minterm][1], minterm_sets))
    return minterms_alive

if __name__ == '__main__':
    size, minterms, dontcares = get_data(input('input file name: '))
    result = []
    draw_line()
    print('step 0. 값 읽어오기')
    print(f'size : {size}')
    print(f'minterms : {minterms}')
    print(f'dontcares : {dontcares}')

    table = make_table(minterms, dontcares, size)
    table = make_PIs(table)

    i = 1
    for imp in table:
        imp.name = 'P'+str(i)
        i += 1

    draw_line()
    print('step 1. PI 찾기')
    print(list(map(lambda imp: imp.minterms, table)))
    draw_line()
    print('step 1-1. PI 테이블')
    draw_PIs(table, minterms, dontcares)

    last_len = 0
    origin_minterms = minterms
    while last_len != len(table):
        last_len = len(table)
        EPIs = find_EPIs(table, minterms, dontcares)
        draw_line()
        print('step 2. EPI 찾기')
        result.extend(EPIs)
        print(*map(lambda imp: f'{imp.name}:{imp.minterms}', EPIs))
        if len(EPIs) == len(table):
            print("NEPI가 남아있지 않으므로 종료합니다.")
            break
        draw_line()

        minterms_of_EPIs = set()
        for EPI in EPIs:
            minterms_of_EPIs.update(EPI.minterms)
        table = list(filter(lambda imp:imp not in EPIs, table))
        minterms = set(filter(lambda m: m not in minterms_of_EPIs, minterms))
        if len(minterms) == 0:
            print("모든 minterm이 커버되었으므로 종료합니다.")
            break

        print('step 2-1. EPI가 제거된 PI 테이블')
        draw_PIs(table, minterms)
        draw_line()

        print('step 3. column dominance')
        minterms = column_dominance(table, minterms)
        print(f'column dominance 후 남은 minterms: {minterms}')
        draw_PIs(table, minterms)
        draw_line()
        print('step 4. row dominance')
        table = row_dominance(table, minterms)
        draw_PIs(table, minterms)
        draw_line()
        print('step 5. 변화가 있다면 부분적으로 다시 시작합니다.')
        print(f'이전 테이블 row 수: {last_len}, 현재 테이블 row 수: {len(table)}')
    else:
        draw_line()
        print('변화가 없으므로 중단합니다.')
        print('Patrick method는 구현되지 않았습니다.')
        print('남은 PIs:')
        draw_PIs(table, minterms)
        print('남은 PIs(full):')
        draw_PIs(table, origin_minterms)
    draw_line()
    print('산출된 EPIs:')
    draw_PIs(sorted(result, key=lambda x:x.name), origin_minterms)