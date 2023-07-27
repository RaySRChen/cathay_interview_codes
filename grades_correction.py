#!/usr/bin/env python
# coding: utf-8

# In[7]:


"""程式邏輯題目: 國泰補習班中，有五位學生期中考的成績分別為[53, 64, 75, 19, 92]，
但是老師在輸入成績的時候看反了，把五位學生的成績改成了[35, 46, 57, 91, 29]，請用一個函數來將學生的成績修正。"""

def correct_grades(grades):
    corrected_grades = []
    for grade in grades:
        # 交換成績的個位數和十位數位置
        corrected_grade = int(str(grade)[1] + str(grade)[0])
        corrected_grades.append(corrected_grade)
    
    return corrected_grades

def main():
    original_grades = [35, 46, 57, 91, 29]
    corrected_grades = correct_grades(original_grades)
    print(f"修正前的成績: {original_grades}, 修正後的成績: {corrected_grades}")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:




