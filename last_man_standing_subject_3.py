#!/usr/bin/env python
# coding: utf-8

# In[10]:


"""程式邏輯題目: QA部門今天舉辦團康活動，有n個人圍成一圈，順序排號。從第一個人開始報數（從1到3報數），凡報到3的人退出圈子。
請利用一段程式計算出，最後留下的那位同事，是所有同事裡面的第幾順位?"""

def last_man_standing(n):
    if n == 0:
        return 0
    else:
        return (last_man_standing(n - 1) + 2) % n + 1

if __name__ == "__main__":
    n = int(input("請輸入同事的總數: "))
    print("最後留下的那位同事是所有同事裡面的第", last_man_standing(n), "順位。")
    


# In[ ]:





# In[ ]:





# In[8]:


5
1


# In[ ]:


7

