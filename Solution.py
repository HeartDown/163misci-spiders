
class Solution:
    def distinctSubseqII(self, S):
        """
        :type S: str
        :rtype: int
        """
        mod=10**9+7
        
        dp=[0 for _ in range(len(S))]
        dp[0]=2
        prev={S[0]:1}
        for i in range(1,len(S)):
            dp[i]=2*dp[i-1]-prev.get(S[i],0)
            dp[i]%=mod
            prev[S[i]]=dp[i-1]
        return dp[-1]%mod-1
    
s=Solution()
print(s.distinctSubseqII("blljuffdyfrkqtwfyfztpdiyktrhftgtabxxoibcclbjvirnqyynkyaqlxgyybkgyzvcahmytjdqqtctirnxfjpktxmjkojlvvrr"))
print(s.distinctSubseqII("aba"))
