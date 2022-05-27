def combine(m, n):
    num_of_var = len(m)
    com = ''
    count = 0
    for i in range(num_of_var):
        if(m[i] == n[i]):
            com += m[i]
        elif(m[i] != n[i]):
            com += '-'
            count += 1

    if(count > 1):
        return None
    else:
        return com

def find_EPI(pi, minterm_bin):
    EPI = []

    prob_of_epi = []

    index_of_hyphen = []
    for i in pi:
        index = []
        tmp = []
        tmp.append(i)
        for j in range(len(i)):
            if i[j] == '-':
                tmp.append(j)
        index_of_hyphen.append(tmp)
        tmp = []

    combined_mt = []
    for i in range(len(index_of_hyphen)):
        tmp = []
        for k in minterm_bin:
            ch = k
            for j in range(1, len(index_of_hyphen[i])):
                l = list(ch)
                l[index_of_hyphen[i][j]] = '-'
                ch = "".join(l)
            tmp.append(ch)

        tmp_2 = []
        tmp_2.append(index_of_hyphen[i][0])
        for q in range(len(tmp)):
            if tmp[q] == index_of_hyphen[i][0]:
                tmp_2.append(minterm_bin[q])
        combined_mt.append(tmp_2)


    if len(combined_mt) == 1:
        return pi

    ch_list = []
    for i in range(len(combined_mt)):
        tmp = []
        appended = False
        check = True
        for j in range(1, len(combined_mt[i])):
            a = combined_mt[i][j]
            for k in range(len(combined_mt)):
                if i == k: continue
                for l in range(1, len(combined_mt[k])):
                    b = combined_mt[k][l]
                    if a == b:
                        check = True
                        break
                    else:
                        check = False
                if check == True:
                    break
            if check == False:
                EPI.append(combined_mt[i][0])
    # print(f'EPI = {set(EPI)}')
    # print(f"cpmbined_mt = {combined_mt}")
    return EPI, combined_mt

def find_PI(minterm_bin):
    num_of_minterm = len(minterm_bin)
    PI = []
    implicant = []
    implicant_2 = []
    m = 0
    combined_mark = [0] * num_of_minterm

    for i in range(num_of_minterm):
        for j in range(i+1, num_of_minterm):
            com = combine(minterm_bin[i], minterm_bin[j])
            if(com != None):
                implicant.append(com)
                combined_mark[i] = 1
                combined_mark[j] = 1

    check_unuse = [False] * len(implicant)

    for i in range(len(implicant)):
        for j in range(i+1, len(implicant)):
            if(i != j and check_unuse[j] == False):
                if(implicant[i] == implicant[j]):
                    check_unuse[j] = 1

    for i in range(len(implicant)):
        if(check_unuse[i] == False):
            implicant_2.append(implicant[i])

    for i in range(num_of_minterm):
        if(combined_mark[i] == 0 ):
            PI.append(str(minterm_bin[i]) )
            m = m+1

    if(m == num_of_minterm or num_of_minterm == 1):
        return PI
    else:
        return PI + find_PI(implicant_2)

def PI_sort(PI):
    dic = {}
    result = []
    for i in PI:
        tmp = i
        tmp_replace = tmp.replace('-', '2')
        dic[tmp_replace] = tmp

    dic = sorted(dic.items())
    for i in dic:
        result.append(i[1])
    return result

def row_dominance(list_mt, combined_mt, EPI, minterm):
    for i in range(len(combined_mt)):
        if combined_mt[i][0] in EPI:
            del combined_mt[i]

    print('\nrow_dominance start')
    list_row = []
    len_mt = 0
    mt_pos = []
    for i in range(len(list_mt)):
        if len(list_mt[i]) != 0:
            len_mt = len(list_mt[i])
            mt_pos.append(i)

    print('\t', end='')
    for i in mt_pos:
        print('{:>7}'.format(minterm[i]), end='')
    print()
    for i in range(len_mt):
        tmp = []
        tmp.append(combined_mt[i][0])
        for j in mt_pos:
            tmp.append(list_mt[j][i])
        list_row.append(tmp)

    for i in list_row:
        print(i)

    second_EPI = []
    for i in range(len(list_row)):
        for j in range(len(list_row)):
            if i == j: continue
            if list_row[i].count(True) > list_row[j].count(True): continue
            count = 0
            for k in range(1, len(list_row[i])):
                if (list_row[i][k] == True) and (list_row[j][k] == True):
                    count += 1
            if count == 0: continue
            if count < list_row[i].count((True)) and list_row[i][0] not in second_EPI and list_row[j][0] not in second_EPI:
                second_EPI.append(list_row[i][0])

    print('\n\t', end='')
    for i in mt_pos:
        print('{:>7}'.format(minterm[i]), end='')
    print()
    for i in second_EPI:
        for j in range(len(list_row)):
            if list_row[j][0] == i:
                print(list_row[j])


def dominance(minterm, combined_mt, EPI):
    print("====================PI====================")
    list_mt = []
    for i in range(len(minterm)):
        tmp = []
        for j in range(len(combined_mt)):
            tmp.append(False)
        list_mt.append(tmp)
    for i in range(len(minterm)):
        for j in range(len(combined_mt)):
            for k in range(1, len(combined_mt[j])):
                if int(combined_mt[j][k],2) == minterm[i]:
                    list_mt[i][j] =True


    print('   ', end='')
    for i in range(len(combined_mt)):
        print('{:>7}'.format(combined_mt[i][0]), end='')
    print()
    for i in range(len(list_mt)):
        print('{:>3}'.format(minterm[i]), list_mt[i])

    print("\n====================Extrude EPI====================")
    epi_pos = []
    for i in range(len(combined_mt)):
            if combined_mt[i][0] in EPI:
                epi_pos.append(i)

    for i in range(len(epi_pos)):
        for j in range(len(list_mt)):
            if len(list_mt[j]) == 0: continue
            if list_mt[j][epi_pos[i]] == True:
                list_mt[j] = []
            else:
                del list_mt[j][epi_pos[i]]

    print('   ', end='')
    for i in range(len(combined_mt)):
        if combined_mt[i][0] in EPI:
            continue
        print('{:>7}'.format(combined_mt[i][0]), end='')
    print()
    for i in range(len(list_mt)):
        if len(list_mt[i]) != 0:
            print('{:>3}'.format(minterm[i]), list_mt[i])
        else:
            continue

    row_dominance(list_mt, combined_mt, EPI, minterm)

    return 0

def solution(minterm):
    num_of_var = minterm[0]
    num_of_minterm = minterm[1]
    minterms = minterm[2:]
    minterms.sort()
    minterm_bin = []
    for i in range(num_of_minterm):
        minterm_bin.append(format(minterms[i], 'b').zfill(num_of_var))

    answer = find_PI(minterm_bin)
    answer = PI_sort(answer)
    EPI, combined_mt = find_EPI(answer, minterm_bin)
    EPI = PI_sort(EPI)
    answer.append('EPI')
    dominance(minterms, combined_mt, EPI)

    if len(EPI) != 0:
        for i in EPI:
            answer.append(i)
    return answer

test = [4, 8, 0, 4, 8, 10, 11, 12, 13, 15]

print('\nANSWER\nPI : ',solution(test))