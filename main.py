import math
import matplotlib.pyplot as plt

NUM_OF_MESSAGES = 20
NUM_OF_LETTERS = 241
ALPHABET_SIZE = 87


def calc_poster_prob(prior_prob, letter, alphabet, task):
    poster_prob = []
    if task:
        for prob in prior_prob: poster_prob.append(prob)
    else:
        for i in range(ALPHABET_SIZE): poster_prob.append(prior_prob[i])
    for i in range(ALPHABET_SIZE): poster_prob[i] *= prob_letter_match(alphabet[i][1], letter)
    sum_poster_prob = sum(poster_prob)
    for i in range(ALPHABET_SIZE): poster_prob[i] /= sum_poster_prob
    return poster_prob


def prob_letter_match(coded, orig):
    prob = 1
    for i in range(len(coded)):
        if coded[i] == orig[i]: prob *= 0.884
        elif orig[i] == '-': prob *= 0.111
        else: prob *= 0.116
    return prob


def calc_info_for_letter(data, letter, prior_equal, alphabet, task):
    prior_prob = []
    conditional_prob = []
    terms = []
    poster_prob = []
    cond_entropy = 0
    amount_info = 0

    for i in range(ALPHABET_SIZE):
        if prior_equal: prior_prob.append(1 / ALPHABET_SIZE)
        else:
            first_step_prob = []
            with open('frequency_of_letters_in_Russian.txt', 'r', encoding='utf-8') as file:
                for line in file: first_step_prob.append(line.rstrip())
            prior_prob.append(float(first_step_prob[i]))

    for i in range(ALPHABET_SIZE): conditional_prob.append(prob_letter_match(alphabet[i][1], letter))
    for i in range(ALPHABET_SIZE): terms.append(conditional_prob[i] * prior_prob[i])
    sum_terms = sum(terms)
    for i in range(ALPHABET_SIZE): poster_prob.append(terms[i] / sum_terms)
    for i in poster_prob: cond_entropy += i * math.log(i, 2)
    for i in range(ALPHABET_SIZE): amount_info += poster_prob[i] * math.log(prior_prob[i], 2)
    amount_info -= cond_entropy

    if task:
        data[0].append(sum_terms)
        data[1].append(cond_entropy * -1)
        data[2].append(amount_info * -1)
    else:
        print(f'\nУсловная энтропия = {cond_entropy * -1}')
        print(f'Среднее количество информации = {amount_info * -1}')
        print(f'Средняя условная энтропия = {sum_terms * cond_entropy * -1}')
        print(f'Средняя взаимная информация = {sum_terms * amount_info * -1}')


def print_graph_task1(data_1, data_2):
    new_data = []
    for i in range(len(data_1)):
        new_data.append([])
        for j in range(len(data_1[i])):
            new_data[i].append((j, []))
            for k in range(len(data_1[i][j])): new_data[i][j][1].append(data_1[i][j][k])

    plt.style.use('seaborn-darkgrid')

    for i in range(NUM_OF_MESSAGES):
        fig, plot = plt.subplots(figsize=(7.5, 5), dpi=150)
        plot.plot([let_ind + 1 for let_ind in range(ALPHABET_SIZE)], new_data[i][0][1], color='blue')
        plt.title(f'График изменения апостериорного распределения вероятностей на примере первой буквы\n'
                  f'Сообщение №{i + 1}\n')
        plt.ylabel('Вероятность\n')
        plt.xlabel('\nНомер символа')
        plt.show()

    plt.title('График изменения условной энтропии H(X/yj)')
    plt.ylabel('Условная энтропия')
    plt.xlabel('Номер посылки')
    plt.plot([i + 1 for i in range(NUM_OF_MESSAGES)], data_2[1], label='Энтропия', color='blue')
    plt.legend()
    plt.show()

    plt.title('График изменения количества информации I(X/yj)')
    plt.ylabel('Количество информации')
    plt.xlabel('Номер посылки')
    plt.plot([i + 1 for i in range(NUM_OF_MESSAGES)], data_2[2], label='Информация', color='blue')
    plt.legend()
    plt.show()


def main():

    # ---task 1---------------------------------------------------------------------------------------------------------
    alphabet = []
    with open('alphabet.txt', 'r', encoding='utf-8') as file:
        for line in file: alphabet.append(line.rstrip().split('\t'))

    data = []
    with open('task_1_info_messages.txt', 'r') as file:
        for line in file.readlines()[1:]: data.append(line.rstrip().split(': ')[1].split(' '))

    prob_prior_equal = [[[1 / ALPHABET_SIZE for _ in range(ALPHABET_SIZE)]
                         for _ in range(NUM_OF_LETTERS)] for _ in range(NUM_OF_MESSAGES)]
    first_step_prob = open('frequency_of_letters_in_Russian.txt', 'r', encoding='utf-8').readlines()
    prob_prior_not_equal = [[[float(first_step_prob[i]) for i in range(ALPHABET_SIZE)]
                             for _ in range(NUM_OF_LETTERS)] for _ in range(NUM_OF_MESSAGES)]

    info_change_letter_prior_equal = []
    info_change_letter_prior_not_equal = []
    for i in range(3):
        info_change_letter_prior_equal.append([])
        info_change_letter_prior_not_equal.append([])

    messages_prior_equal = []
    messages_prior_not_equal = []

    for message in range(NUM_OF_MESSAGES):
        if message == 0:
            for ind_letter in range(NUM_OF_LETTERS):
                prob_prior_equal[message][ind_letter] = \
                    calc_poster_prob(prob_prior_equal[message][ind_letter],
                                     data[message][ind_letter], alphabet, True)
                prob_prior_not_equal[message][ind_letter] = \
                    calc_poster_prob(prob_prior_not_equal[message][ind_letter],
                                     data[message][ind_letter], alphabet, True)
        else:
            for ind_letter in range(NUM_OF_LETTERS):
                prob_prior_equal[message][ind_letter] = \
                    calc_poster_prob(prob_prior_equal[message - 1][ind_letter],
                                     data[message][ind_letter], alphabet, True)
                prob_prior_not_equal[message][ind_letter] = \
                    calc_poster_prob(prob_prior_not_equal[message - 1][ind_letter],
                                     data[message][ind_letter], alphabet, True)

        calc_info_for_letter(info_change_letter_prior_equal, data[message][0], True, alphabet, True)
        calc_info_for_letter(info_change_letter_prior_not_equal, data[message][0], False, alphabet, True)

        letter_prior_equal = f'\nСообщение №{message + 1}\n'
        letter_prior_not_equal = f'\nСообщение №{message + 1}\n'
        for letter_ind in range(NUM_OF_LETTERS):
            letter_prior_equal += \
                alphabet[prob_prior_equal[message][letter_ind].
                    index(max(prob_prior_equal[message][letter_ind]))][0]
            letter_prior_not_equal += \
                alphabet[prob_prior_not_equal[message][letter_ind].
                    index(max(prob_prior_not_equal[message][letter_ind]))][0]

        messages_prior_equal.append(letter_prior_equal)
        messages_prior_not_equal.append(letter_prior_not_equal)

    average_cond_entropy_prior_equal = 0
    average_cond_entropy_prior_not_equal = 0
    average_mutual_info_prior_equal = 0
    average_mutual_info_prior_not_equal = 0
    for i in range(NUM_OF_MESSAGES):
        average_cond_entropy_prior_equal += \
            info_change_letter_prior_equal[0][i] * info_change_letter_prior_equal[1][i]
        average_cond_entropy_prior_not_equal += \
            info_change_letter_prior_not_equal[0][i] * info_change_letter_prior_not_equal[1][i]

        average_mutual_info_prior_equal += \
            info_change_letter_prior_equal[0][i] * info_change_letter_prior_equal[2][i]
        average_mutual_info_prior_not_equal += \
            info_change_letter_prior_not_equal[0][i] * info_change_letter_prior_not_equal[2][i]

    print('\nПРИ РАВНОЙ ВЕРОЯТНОСТИ БУКВ:')
    for m_p_e in messages_prior_equal: print(m_p_e)

    for i in range(NUM_OF_MESSAGES):
        print(f'\nСообщение №{i + 1}:')
        print(f'Условные энтропия = {info_change_letter_prior_equal[1][i]}')
        print(f'Среднее количество информации = {info_change_letter_prior_equal[2][i]}')

    print(f"\nСредняя условная энтропия = {average_cond_entropy_prior_equal}")
    print(f"Средняя взаимная информация = {average_mutual_info_prior_equal}")

    print('\nПРИ РАЗНОЙ ВЕРОЯТНОСТИ БУКВ:')
    for m_p_n_e in messages_prior_not_equal: print(m_p_n_e)

    for i in range(NUM_OF_MESSAGES):
        print(f'\nСообщение №{i + 1}:')
        print(f'Условные энтропия = {info_change_letter_prior_equal[1][i]}')
        print(f'Среднее количество информации = {info_change_letter_prior_not_equal[2][i]}')

    print(f"\nСредняя условная энтропия = {average_cond_entropy_prior_not_equal}")
    print(f"Средняя взаимная информация = {average_mutual_info_prior_not_equal}")

    print_graph_task1(prob_prior_equal, info_change_letter_prior_equal)
    print_graph_task1(prob_prior_not_equal, info_change_letter_prior_not_equal)

    # ---task2----------------------------------------------------------------------------------------------------------
    data_task2 = []
    for i in range(NUM_OF_LETTERS):
        tmp = ''
        for j in range(NUM_OF_MESSAGES): tmp += data[j][i]
        data_task2.append(tmp)

    alphabet_task2 = []
    with open('alphabet_task2.txt', 'r', encoding='utf-8') as file:
        for line in file: alphabet_task2.append(line.rstrip().split('\t'))

    prob_prior_equal_task2 = [[1 / ALPHABET_SIZE for _ in range(ALPHABET_SIZE)] for _ in range(NUM_OF_LETTERS)]
    first_step_prob = open('frequency_of_letters_in_Russian.txt', 'r', encoding='utf-8').readlines()
    prob_prior_not_equal_task2 = \
        [[float(first_step_prob[i]) for i in range(ALPHABET_SIZE)] for _ in range(NUM_OF_LETTERS)]

    for ind_letter in range(NUM_OF_LETTERS):
        prob_prior_equal_task2[ind_letter] = \
            calc_poster_prob(prob_prior_equal_task2[ind_letter], data_task2[ind_letter], alphabet_task2, False)
        prob_prior_not_equal_task2[ind_letter] = \
            calc_poster_prob(prob_prior_not_equal_task2[ind_letter], data_task2[ind_letter], alphabet_task2, False)

    letter_prior_equal = ''
    letter_prior_not_equal = ''
    for letter_ind in range(NUM_OF_LETTERS):
        letter_prior_equal += \
            alphabet_task2[prob_prior_equal_task2[letter_ind].index(max(prob_prior_equal_task2[letter_ind]))][0]
        letter_prior_not_equal += \
            alphabet_task2[prob_prior_not_equal_task2[letter_ind].index(max(prob_prior_not_equal_task2[letter_ind]))][0]

    print('\nПРИ РАВНОЙ ВЕРОЯТНОСТИ БУКВ:\n')
    print(letter_prior_equal)
    calc_info_for_letter([], data_task2[0], True, alphabet_task2, False)

    print('\nПРИ РАЗНОЙ ВЕРОЯТНОСТИ БУКВ:\n')
    print(letter_prior_not_equal)
    calc_info_for_letter([], data_task2[0], False, alphabet_task2, False)

    plt.style.use('seaborn-darkgrid')
    fig, plot_p_e = plt.subplots(figsize=(7, 6), dpi=150)
    plot_p_e.plot([i + 1 for i in range(ALPHABET_SIZE)], prob_prior_equal_task2[0], color='blue')
    plt.title('График апостериорного распределения вероятностей на примере первой буквы\n')
    plt.ylabel('Вероятность\n')
    plt.xlabel('Номер символа')
    plt.show()

    fig, plot_p_n_e = plt.subplots(figsize=(7, 6), dpi=150)
    plot_p_n_e.plot([i + 1 for i in range(ALPHABET_SIZE)], prob_prior_not_equal_task2[0], color='blue')
    plt.title('График апостериорного распределения вероятностей на примере первой буквы\n')
    plt.ylabel('Вероятность\n')
    plt.xlabel('Номер символа')
    plt.show()


if __name__ == '__main__': main()
