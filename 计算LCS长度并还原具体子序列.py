def lcs_full(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 1. 构建 DP 表格
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 2. 逆向回溯，提取具体子序列
    lcs_str = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            # 如果字符相同，说明它是 LCS 的一部分，加入结果并移到左上角
            lcs_str.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            # 否则向值更大的方向移动（优先向上）
            i -= 1
        else:
            # 向左移动
            j -= 1

    # 因为是从后往前找的，所以需要反转列表
    lcs_str.reverse()
    return dp[m][n], "".join(lcs_str)


if __name__ == '__main__':
    s1 = "ABCBDAB"
    s2 = "BDCABA"

    length, sequence = lcs_full(s1, s2)
    print(f"LCS 长度: {length}")
    print(f"具体子序列: {sequence}")
