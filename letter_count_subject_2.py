#!/usr/bin/env python
# coding: utf-8

# In[13]:


"""程式邏輯題目: 國泰銀行要慶祝六十周年，需要買字母貼紙來布置活動空間，文字為"Hello welcome to Cathay 60th year anniversary"，
請寫一個程式計算每個字母(大小寫視為同個字母)出現次數; 
預期輸出: 
0 1
6 1
A 4
C 2
E 5
H 3
....(繼續印下去)"""


def count_letters(text):
    letter_count = {}
    # 將文字中的空白字元去除
    text = text.replace(" ", "")
    # 將文字轉換為大寫
    upper_text = text.upper()
    # 將字母加入字典，如果不存在則加入新的字母並設置為1
    for char in upper_text:
        if char.isalpha():
            letter_count[char] = letter_count.get(char, 0) + 1

    return letter_count

def main():
    text = "Hello welcome to Cathay 60th year anniversary"
    letter_count = count_letters(text)
    
    # 加入 0 和 6 這兩個字元到字母計算中
    for char in "06":
        letter_count[char] = text.count(char)
    
    # 使用 sorted 函式進行排序
    for letter, count in sorted(letter_count.items()):
        print(f"{letter} {count}")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




