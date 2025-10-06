#!/usr/bin/env python3
"""
Алгоритма Нидлмана-Вунша.
"""

import time
import os


def clear_screen():
    """Очищает экран"""
    os.system('clear' if os.name == 'posix' else 'cls')


def print_matrix(seq1, seq2, dp, current_i=None, current_j=None, step_info=""):
    """
    Печатает матрицу с анимацией текущей ячейки
    """
    clear_screen()

    print("=" * 70)
    print("АЛГОРИТМ НИДЛМАНА-ВУНША - ПОШАГОВОЕ ЗАПОЛНЕНИЕ")
    print("=" * 70)
    print(f"Seq1: {seq1}")
    print(f"Seq2: {seq2}")
    if step_info:
        print(f"Шаг: {step_info}")
    print()

    # Заголовок
    print("     ", end="")
    for j in range(len(dp[0])):
        if j == 0:
            print("   ", end="")
        else:
            print(f"  {seq2[j-1]}", end="")
    print()

    # Строки матрицы
    for i in range(len(dp)):
        if i == 0:
            print("   ", end="")
        else:
            print(f" {seq1[i-1]} ", end="")

        for j in range(len(dp[0])):
            # Выделяем текущую ячейку
            if current_i == i and current_j == j:
                print(f"[{dp[i][j]:2}]", end="")
            else:
                print(f" {dp[i][j]:2} ", end="")
        print()

    print("=" * 70)


def needleman_wunsch(seq1, seq2, match=2, mismatch=-1, gap=-1):
    """
    Алгоритма Нидлмана-Вунша
    """
    n, m = len(seq1), len(seq2)


    dp = [[0] * (m+1) for _ in range(n+1)]

    for i in range(n+1):
        dp[i][0] = i * gap
    for j in range(m+1):
        dp[0][j] = j * gap

    print_matrix(seq1, seq2, dp, step_info="Инициализация")
    time.sleep(2)

    for i in range(1, n+1):
        for j in range(1, m+1):
            print_matrix(seq1, seq2, dp, current_i=i, current_j=j,
                                step_info=f"Заполнение ячейки ({i},{j})")

            match_score = dp[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            delete = dp[i-1][j] + gap
            insert = dp[i][j-1] + gap

            print(f"\nРасчет для {seq1[i-1]} vs {seq2[j-1]}:")
            print(f"↖ Совпадение: {dp[i-1][j-1]} + {match if seq1[i-1] == seq2[j-1] else '-1'} = {match_score}")
            print(f"↑ Удаление:   {dp[i-1][j]} + {gap} = {delete}")
            print(f"← Вставка:    {dp[i][j-1]} + {gap} = {insert}")

            dp[i][j] = max(match_score, delete, insert)

            print(f"Максимум: {dp[i][j]}")
            time.sleep(1.5)

    print_matrix(seq1, seq2, dp, step_info="Матрица заполнена")
    time.sleep(2)

    align1, align2 = "", ""
    i, j = n, m

    print("\nОБРАТНЫЙ ПРОХОД:")
    print("=" * 50)

    step = 1
    while i > 0 or j > 0:
        print(f"\nШаг {step}: Позиция ({i},{j})")

        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch):
            print(f"  ↖ Совпадение: {seq1[i-1]} = {seq2[j-1]}")
            align1 = seq1[i-1] + align1
            align2 = seq2[j-1] + align2
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + gap:
            print(f"  ↑ Удаление: {seq1[i-1]} → -")
            align1 = seq1[i-1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            print(f"  ← Вставка: - ← {seq2[j-1]}")
            align1 = "-" + align1
            align2 = seq2[j-1] + align2
            j -= 1

        print(f"  Выравнивание: {align1}")
        print(f"                {align2}")

        step += 1
        time.sleep(1)

    return align1, align2, dp


def main():
    """
    Демонстрация алгоритма
    """
    # Ваши последовательности
    seq1 = "GCATGCG"
    seq2 = "GATTACA"

    print("АЛГОРИТМ НИДЛМАНА-ВУНША")
    print("=" * 70)
    print(f"Последовательность 1: {seq1}")
    print(f"Последовательность 2: {seq2}")
    print("Параметры: match=2, mismatch=-1, gap=-1")
    print()

    result1, result2, matrix = needleman_wunsch(seq1, seq2)

    print("\n" + "=" * 70)
    print("ФИНАЛЬНЫЙ РЕЗУЛЬТАТ:")
    print("=" * 70)
    print(f"Выравнивание 1: {result1}")
    print(f"Выравнивание 2: {result2}")
    print(f"Общий score: {matrix[len(seq1)][len(seq2)]}")


if __name__ == "__main__":
    main()
