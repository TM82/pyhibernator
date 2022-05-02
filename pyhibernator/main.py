from __future__ import annotations

import itertools 

import numpy as np
import pandas as pd


class AdjustedGiniCoefficient: 
    """
    Based on Li, J., Shi, D., Zhao, S. X., & Fred, Y. Y. (2014). A study of the “heartbeat spectra” for “sleeping beauties”. Journal of informetrics, 8(3), 493-502.
    """
    
    @staticmethod
    def score(c:list[int]) -> float:
        """
        Parameters: 
        ----------
        c : list
            Citation history, c[0] is the citation of publication year.

        Returns:
        ----------
        float:
            Score of Adjusted Gini Coefficient
        """


        C = sum(c)
        n = len(c)
        if C==0:
            return 1.0
        elif n<2:
            return 0.0
        else:
            Gs = (n/(n-1))*(1 - ((2*sum([c[t]*(n-t) for t in range(n)])-C)/(n*C)))
            return Gs


class Average:
    """
    Based on van Raan, A. F. (2021). Sleeping beauties gain impact in overdrive mode. Scientometrics, 126(5), 4311-4332.
    """
    
    @staticmethod
    def extract(c:list[int], s:int, cs:int, a:int, ca:int) -> bool:
        """
        Parameters: 
        ----------
        c: list
            Citation history, c[0] is the citation of publication year.
        s: int    
            Sleep length
        cs: int
            Depth of sleep
        a: int
            Awake length
        ca: int
            Awake intensity

        Returns:
        ----------
        bool:
            whether the paper is hibernator or not
        """

        c_average = sum(c[:s+1])/(s+1)
        ca_average = sum(c[s+1:s+a+1])/(a)
        if (c_average<=cs) and (ca_average >= ca):
            return True
        return False


class BeautyCoefficient:
    """
    Based on Ke, Q., Ferrara, E., Radicchi, F., & Flammini, A. (2015). Defining and identifying sleeping beauties in science. Proceedings of the National Academy of Sciences, 112(24), 7426-7431.
    """
    
    @staticmethod
    def score(c:list[int]) -> float:
        """
        Parameters: 
        ----------
        c : list
            Citation history, c[0] is the citation of publication year.

        Returns:
        ----------
        float:
            Score of Beauty Coefficient
        """

        def _get_c0_tm_ctm(c:list[int]) -> (int,int,int):
            """
            Get parameters for calculating Beauty Coefficient
            """
            c0 = c[0]
            tm = np.argmax(c)
            ctm = np.max(c)
            return c0,tm,ctm

        def _calcB(ctm:int, c0:int, tm:int, ct:int, max_ct:int, t:int) -> float:
            '''
            Calculate Beauty Coefficient
            '''
            return ((ctm - c0)*t/tm + c0 - ct)/max_ct

        if np.sum(c) == 0:
            return 0
        else:
            c0,tm,ctm = _get_c0_tm_ctm(c)
            if tm == 0:
                return 0
            else:
                return sum([_calcB(ctm,c0,tm,c[t],max(1,c[t]),t) for t in range(tm+1)])


class BeautyCoefficientCumulativePercentage:
    """
    Based on Du, J., & Wu, Y. (2018). A parameter-free index for identifying under-cited sleeping beauties in science. Scientometrics, 116(2), 959-971.
    """
    
    @staticmethod
    def score(c:list[int]) -> float:
        """
        Parameters: 
        ----------
        c : list
            Citation history, c[0] is the citation of publication year.

        Returns:
        ----------
        float:
            Score of Beauty Coefficient Cumulative Percentage
        """

        def _get_c0_tm_ctm(c:list[int]) -> (int,int,int):
            """
            Get parameters for calculating Beauty Coefficient
            """
            c0 = c[0]
            tm = np.argmax(c)
            ctm = np.max(c)
            return c0,tm,ctm

        def _calcBcp(ctm:int, c0:int, tm:int, ct:int, t:int) -> float:
            '''
            Calculate Beauty Coefficient Cumulative Percentage
            '''
            return (1 - c0)*t/tm + c0 - ct

        if np.sum(c) == 0:
            return 0
        else:
            c_relative = np.cumsum(c)/np.sum(c)
            c0,tm,ctm = _get_c0_tm_ctm(c_relative)
            return sum([_calcBcp(ctm,c0,tm,c_relative[t],t) for t in range(tm+1)])


class CitationAngle:
    """
    Based on Ye, F. Y., & Bornmann, L. (2018). “Smart girls” versus “sleeping beauties” in the sciences: The identification of instant and delayed recognition by using the citation angle. Journal of the Association for Information Science and Technology, 69(3), 359-367.
    """
    
    @staticmethod
    def extract(c:list[int], c_before_average:float, c_peak:float, angle_after:float, span:float) -> bool:
        """
        Parameters: 
        ----------
        c : list
            Citation history, c[0] is the citation of publication year.
        c_before_average: float
            threshold for determining average citation before half years as low
            For "Typical SB" in original paper, c_before_average is 2
        c_peak: float
            threshold for determining peak citation as high
            For "Typical SB" in original paper, c_peak is 20
        angle_after: float
            threshold for citation angle
            For "Typical SB" in original paper, angle_after is 5
        span: float
            threshold for span between peak year before half years and peak year after half years
            For "Typical SB" in original paper, span is 10

        Returns:
        ----------
        bool:
            whether the paper is hibernator or not
        """


        if len(c)<=10: #As original, papers have to sleep at least 5 years which requires 10 years after submission.
            return False
        else:
            th = int(len(c)/2)
            t1 = np.argmax(c[:th])
            ac1 = np.average(c[:th])
            t2 = th + np.argmax(c[th:])
            peak2 = np.max(c[th:])
            angle2 = np.degrees(np.arctan(peak2/t2))
            return (peak2>c_peak) & (angle2>angle_after) & (ac1<=c_before_average) & (t2-t1>=span)


class CitationDelay:
    """
    Based on Wang, J., Thijs, B., & Glänzel, W. (2015). Interdisciplinarity and impact: Distinct effects of variety, balance, and disparity. PloS one, 10(5), e0127298.
    """
    
    @staticmethod
    def score(c:list[int]) -> float:
        """
        Parameters: 
        ----------
        c : list
            Citation history, c[0] is the citation of publication year.

        Returns:
        ----------
        float:
            Score of Citation Delay
        """
        return 1 - np.sum((np.cumsum(c)/np.sum(c))[:-1])/(len(c)-1)


class DNIC:
    """
    Based on Bornmann, L., Ye, A. Y., & Ye, F. Y. (2018). Identifying “hot papers” and papers with “delayed recognition” in large-scale datasets by using dynamically normalized citation impact scores. Scientometrics, 116(2), 655-674.
    """

    @staticmethod
    def get_ekj(c_list:list[list[int]], subjs_list: list[list[str]], year_list:list[int]) -> dict:
        """
        Get the average citation of each subject and year

        Parameters: 
        ----------
        c_list: list[list[int]]
            Citation history for all papers
        subjs_list: list[list[str]]
            Subject list for all papers
        year_list: list[int]
            Publication year for all papers

        Returns:
        ----------
        dict:
            Average citation of each subject and year
        """
        ekj_dic = dict()
        df = pd.DataFrame([c_list,subjs_list,year_list],index=['c','subjs','year']).T

        for year in set(year_list):
            for subj in set(list(itertools.chain.from_iterable(subjs_list))):
                targets = df[(df['year']<=year)&(df['subjs'].map(lambda x: subj in x))]
                if len(targets):
                    citations_kj = targets.apply(lambda row: row['c'][year-row['year']],axis=1)
                    N_kj = (citations_kj>=1).sum()
                    if N_kj == 0:
                        ekj_dic[(subj,year)] = -1
                    else:
                        ekj_dic[(subj,year)] = citations_kj.sum()/N_kj
        return ekj_dic

    @staticmethod
    def extract(c:list[int], subjs:list[str], year:int, ekj_dic:dict, c_peak:float, c_before_peak:float) -> bool:
        """
        Parameters: 
        ----------
        c: list
            Citation history, c[0] is the citation of publication year.
        subjs: list[str]
            Subject list
        year: int
            Publication year
        ekj_dic: dict
            Average citation of each subject and year
        c_peak: float
            threshold for determining peak DNIC as high
        c_before_peak: float
            threshold for determining max DNIC before peak as low
            
        Returns:
        ----------
        bool:
            whether the paper is hibernator or not
        """
        t_h = int(len(c)/2)
        t_peak_v = np.argmax(c) 
        y_peak_v = year + t_peak_v
        c_peak_v = c[t_peak_v]
        if t_h < t_peak_v:
            for subj in subjs: #at least 1 subject meet a requirement, the paper is regarded as hibernator
                if c_peak_v/ekj_dic[(subj,y_peak_v)] > c_peak:
                    if max([c[i-year]/ekj_dic[(subj,i)] for i in range(year,y_peak_v-2)]) < c_before_peak:
                        return True
        return False


class ExponentialQuartile:
    """
    Based on Li, J., & Shi, D. (2016). Sleeping beauties in genius work: When were they awakened?. Journal of the Association for Information Science and Technology, 67(2), 432-440.
    """

    @staticmethod
    def extract(c:list[int], k:int) -> bool:
        """
        Requires cw>4cs, nw ~ ns/4, cw > √k*ns

        Parameters: 
        ----------
        c : list
            Citation history, c[0] is the citation of publication year.
        k: int
            hyperparameter、smaller k means shorter sleep
            
        Returns:
        ----------
        bool:
            whether the paper is hibernator or not
        """

        n = len(c)
        nw = int(n * 0.2)
        ns = n - nw
        cs = np.max(c[:ns])
        cw = np.max(c[ns:])
        return (cw > 4*cs) & (cw>(np.sqrt(k*ns)))


class KValue:
    """
    Based on Teixeira, A. A., Vieira, P. C., & Abreu, A. P. (2017). Sleeping beauties and their princes in innovation studies. Scientometrics, 110(2), 541-580.
    """

    @staticmethod
    def score(c:list[int]) -> float:
        """
        Parameters: 
        ----------
        c : list
            Citation history, c[0] is the citation of publication year.
            
        Returns:
        ----------
        float:
            Score of K Value
        """
        
        c20 = c[:21]
        if sum(c20) == 0:
            return 0.0
        K =  np.sqrt(sum([i**2 * ct for i,ct in enumerate(c20)])/sum(c20)) / 20
        return K


class Naive:
    """
    Based on Glänzel, W., Schlemmer, B., & Thijs, B. (2003). Better late than never? On the chance to become highly cited only beyond the standard bibliometric time horizon. Scientometrics, 58(3), 571-586.
    """

    @staticmethod
    def extract(c:list[int], s:int, cs:int, ca:int) -> bool:
        """
        Parameters: 
        ----------
        c: list[int]
            Citation history, c[0] is the citation of publication year.
        s: int
            Sleep length
        cs: int
            Depth of sleep
        ca: int
            Today's minimum citation
            
        Returns:
        ----------
        bool:
            whether the paper is hibernator or not
        """
        
        c_sum = sum(c[:s+1])
        c_now = sum(c)
        if (c_sum<=cs) and (c_now >= ca):
            return True
        return False


class Quartile:
    """
    Based on Costas, R., van Leeuwen, T. N., & van Raan, A. F. (2010). Is scientific literature subject to a ‘Sell‐By‐Date’? A general methodology to analyze the ‘durability’of scientific documents. Journal of the American Society for Information Science and Technology, 61(2), 329-339.
    """

    @staticmethod
    def get_c50(c:list[int]) -> int:
        """
        Get an year which the paper reach the half number of its current citation

        Parameters: 
        ----------
        c : list[int]
            Citation history, c[0] is the citation of publication year.
            
        Returns:
        ----------
        int:
            Year which the paper reach the half number of its current citation
        """
        if np.sum(c)  == 0:
            return 0
        try:
            return np.min(np.where(np.cumsum(c)/np.sum(c) >= 0.5))
        except:
            print(c)
            raise

    @staticmethod
    def get_c_dic(c50_list:list[int], subjs_list: list[list[str]], year_list:list[int], rate:float) -> dict:
        """
        Get an year which XX% of papers in each subject and year obtain the half number of its current citation

        Parameters: 
        ----------
        c50_list: list[int]
            List of years which all papers reach the half number of its current citation
        subjs_list: list[list[str]]
            Subject list for all papers
        year_list: list[int]
            Publication year for all papers
        rate:
            Rate of the number of papers
            
        Returns:
        ----------
        dict:
            Year which (rate)% of papers in each subject and year obtain the half number of its current citation
        """

        c_dic = dict()
        df = pd.DataFrame([c50_list,subjs_list,year_list],index=['c50','subjs','year']).T

        for year in set(df['year']):
            for subj in set(list(itertools.chain.from_iterable(df['subjs']))):
                targets = df[(df['year']==year)&(df['subjs'].map(lambda x: subj in x))]
                if len(targets):
                    c_dic[(subj,year)] = targets.sort_values('c50').iloc[int(len(targets)*rate)]['c50']
        return c_dic

    @staticmethod
    def extract(c50:int, subjs:list[str], year:int, c_dic_before:dict, c_dic_after:dict) -> bool:
        """
        Parameters: 
        ----------
        c50: int
            Citation history, c[0] is the citation of publication year.
        subjs: list[str]
            Subject list
        year: int
            Publication year
        c_dic_before:
            Dictionaries of the year in which the 50% citation achievement is fast, i.e., the score is 1. The key is (subj,year)
        c_dic_after: 
            Dictionaries of the year in which the 50% citation achievement is slow, i.e., the score is 3. The key is (subj,year)
            
        Returns:
        ----------
        bool:
            whether the paper is hibernator or not
        """

        scores = [1 if c50 < c_dic_before[(subj,year)] else 3 if c50 > c_dic_after[(subj,year)] else 2 for subj in subjs]
            
        return np.mean(scores) >= 2.5