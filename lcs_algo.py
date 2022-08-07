
def lcs(setA, setB):

    dp = [[0 for i in range(len(setB)+1)] for j in range(len(setA)+1)]

    for i in range(1, len(setA)+1):
        for j in range(1, len(setB)+1):
            if setA[i-1] == setB[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
    i=len(setA)
    j=len(setB)
    res=[]

    while i > 0 and j > 0:
        if setA[i-1] == setB[j-1]:
            res=[setB[j-1]]+res
            j-=1
            i-=1
        else:
            if dp[i-1][j] > dp[i][j-1]:
                i-=1
            else:
                j-=1

    return [dp[len(setA)][len(setB)] , res]

setA = list("AGGTAB")
setB = list("GXTXAYB")

res = lcs(setA, setB)

print(res)