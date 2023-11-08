def print_array(array):
    for el in array:
        print(el)


def get_delta(x, y):
    result = []
    for i in range(len(x)):
        result.append(x[i] - y[i])
    return result


def get_sigma_table(mx):
    sigma_table = [[get_sigma(get_delta(mx[i], mx[j])) for j in range(len(mx))] for i in range(len(mx))]
    print("Вектори знаків різниць оцінок")
    for i, row in enumerate(sigma_table, start=1):
        for j, col in enumerate(row, start=1):
            print(f'{i}-{j}: {col}')
    return sigma_table


def get_sigma(delta):
    result = []
    for i in range(len(delta)):
        if delta[i] > 0:
            result.append(1)
        elif delta[i] < 0:
            result.append(-1)
        else:
            result.append(0)
    return result


def get_pareto_result(array):
    print("Відношення Парето")
    sigma_table = get_sigma_table(array)
    r0 = [[0 if any(sigma < 0 for sigma in sigma_table[i][j]) else 1 for j in range(a_count)] for i in range(a_count)]
    print("r0")
    print_array(r0)
    return r0


def get_majoritar_result(array):
    print("Мажоритарний алгоритм")
    sigma_table = get_sigma_table(array)
    vector_sum_table = []
    for i in range(a_count):
        vector_sum_table.append([])
        for j in range(a_count):
            vector_sum = 0
            for index in range(len(sigma_table[i][j])):
                vector_sum = vector_sum + sigma_table[i][j][index]
            vector_sum_table[i].append(vector_sum)

    print("Таблиця сум векторів")
    print_array(vector_sum_table)
    rm = []
    for i in range(a_count):
        rm.append([])
        for j in range(a_count):
            if vector_sum_table[i][j] > 0:
                rm[i].append(1)
            else:
                rm[i].append(0)

    print("Rm")
    print_array(rm)

    return rm


def get_lexicolograph_result(array):
    print("Лексикографічний алгоритм")
    sigma_table = get_sigma_table(array)
    rl = []
    for i in range(a_count):
        rl.append([])
        for j in range(a_count):
            is_found = False
            check_sigma_vector = sigma_table[i][j]
            for k_index in range(len(str_order)):
                if check_sigma_vector[str_order[k_index]] < 0:
                    is_found = True
                    rl[i].append(0)
                elif check_sigma_vector[str_order[k_index]] > 0:
                    is_found = True
                    rl[i].append(1)
                if is_found:
                    break
            if not is_found:
                rl[i].append(0)
    print("rl")
    print_array(rl)

    return rl


def get_berezovski_result(array):
    print("Алгоритм Березовського")

    p_prev = []
    i_prev = []
    n_prev = []

    p = []

    for l in range(len(kvazi_groups)):
        index_array = kvazi_groups[l]
        kvazi_system = []
        for i in range(a_count):
            kvazi_system.append([])
            for j in range(len(index_array)):
                kvazi_system[i].append(array[i][index_array[j]])
        print(f"Ітерація {l + 1}")
        print_array(kvazi_system)

        sigma_table = get_sigma_table(kvazi_system)
        i_system = get_i(sigma_table)
        print(f"I0{l + 1} таблиця")
        print_array(i_system)

        p_system = get_p(sigma_table)
        print(f"P0{l + 1} таблиця")
        print_array(p_system)

        n_system = get_n(sigma_table)
        print(f"N0{l + 1} таблиця")
        print_array(n_system)

        if l == 0:
            i_prev = i_system
            n_prev = n_system
            p_prev = p_system
            continue

        pb = []
        for i in range(a_count):
            pb.append([])
            for j in range(a_count):
                if p_system[i][j] == 1 and (p_prev[i][j] == 1 or n_prev[i][j] == 1 or i_prev[i][j] == 1):
                    pb[i].append(1)
                elif i_system[i][j] == 1 and p_prev[i][j] == 1:
                    pb[i].append(1)
                else:
                    pb[i].append(0)

        i_b = []
        for i in range(a_count):
            i_b.append([])
            for j in range(a_count):
                if i_system[i][j] == 1 and i_prev[i][j] == 1:
                    i_b[i].append(1)
                else:
                    i_b[i].append(0)

        n_b = []
        for i in range(a_count):
            n_b.append([])
            for j in range(a_count):
                if not (pb[i][j] == 1 or pb[j][i] == 1 or i_b[i][j] == 1):
                    n_b[i].append(1)
                else:
                    n_b[i].append(0)

        print(f"RB{l + 1}")
        print_array(pb)

        print(f"NB{l + 1}")
        print_array(n_b)

        print(f"IB{l + 1}")
        print_array(i_b)

        n_prev = n_b
        i_prev = i_b
        p_prev = pb

    return pb


def get_p(array):
    result = []
    for i in range(len(array)):
        result.append([])
        for j in range(len(array)):
            sigma = array[i][j]
            is_greater = False
            is_lower = False
            for index in range(len(sigma)):
                if sigma[index] == 1:
                    is_greater = True
                elif sigma[index] == -1:
                    is_lower = True
            if is_greater and not is_lower:
                result[i].append(1)
            else:
                result[i].append(0)
    return result


def get_i(array):
    result = []
    for i in range(len(array)):
        result.append([])
        for j in range(len(array)):
            sigma = array[i][j]
            if all(v == 0 for v in sigma):
                result[i].append(1)
            else:
                result[i].append(0)
    return result


def get_n(array):
    result = []
    for i in range(len(array)):
        result.append([])
        for j in range(len(array)):
            sigma = array[i][j]
            is_greater = False
            is_lower = False
            for index in range(len(sigma)):
                if sigma[index] == 1:
                    is_greater = True
                elif sigma[index] == -1:
                    is_lower = True
            if is_greater and is_lower:
                result[i].append(1)
            else:
                result[i].append(0)
    return result


def get_podinovski_result(array):
    print("Алгоритм Подиновського")
    psi = get_vector_function(array)
    print("Вектор-функція")
    print_array(psi)
    rp = get_pareto_result(psi)
    return rp


def get_vector_function(array):
    result = []
    for i in range(a_count):
        result.append(sorted(array[i], reverse=True))
    return result


if __name__ == '__main__':
    kvazi_groups = [[1, 5, 8, 11], [3, 6], [0, 2, 4, 7, 9, 10]]  # для Березовського
    str_order = [10, 9, 5, 2, 8, 6, 1, 0, 7, 11, 3, 4]  # для лексикографічного
    a_count = 20  # кількість альтернатив

    mx_str = """ 
     4  1  5  3  2  5  5  8  5  1  8  5 
     3  1  5  3  2  5  5  3  1  1  7  5 
     2  1  4  3  2  1  2  3  1  1  6  3 
     6  2  5  8 10  3  3  3  3  2  7  5 
     4  1  5  3  2  2  3  2  3  1  4  5 
     8  9  6  9  8  2  3  3  5  6  5 10 
     6  2  4  8  8  2  3  2  3  2  1  2 
     9  2  4  9 10  6  8  3  3  3  2  5 
     6  2  4  8  8  2  3  2  3  2  1  1 
     6  2  9  8  8 10  8  2  6  5  8  1 
     9  6  9  9 10 10  8  8  6  7 10  5 
     6  6  4  4  1  2  8  6  1  2  6  3 
     3  2  2  4  1  2  3  3  1  2  2  2 
     3  2  2  4  1  2  3  3  1  1  2  1 
     3  1  1  3  1  2  3  3  1  1  2  1 
     3  6  6  9  8  4  6  3 10  7 10  5 
     6  6  7  9  8  4  8  4 10  7 10  6 
     6  6  6  3  8  1  4  4  1  7  2  3 
     3  5  2  3  3  1  4  3  1  2  2  3 
     9  5  5  3 10  4  6  3  2  7  6  7 
      """
    matrix = [[int(number) for number in line.split()] for line in mx_str.split('\n') if line.strip()]

    mx1 = get_pareto_result(matrix)
    mx2 = get_majoritar_result(matrix)
    mx3 = get_lexicolograph_result(matrix)
    mx4 = get_berezovski_result(matrix)
    mx5 = get_podinovski_result(matrix)

    with open('output.txt', 'w') as file:
        file.write('1\n')
        for row in mx1:
            file.write(f'{row}\n')
        file.write('2\n')
        for row in mx2:
            file.write(f'{row}\n')
        file.write('3\n')
        for row in mx3:
            file.write(f'{row}\n')
        file.write('4\n')
        for row in mx4:
            file.write(f'{row}\n')
        file.write('5\n')
        for row in mx5:
            file.write(f'{row}\n')


