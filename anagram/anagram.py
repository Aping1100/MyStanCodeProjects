"""
File: anagram.py
Name:Yipin
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time                   # This file allows you to calculate the speed of your algorithm
import tkinter
# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop

lst = []    # list 由字典內收尋到之單字組成


def main():
    """
    藉由read_dictionary()將字典內的單字存成list
    以find_anagrams(s)先查找字串的排序組合，再查詢符合字典的字串
    """
    make_gui()


def make_gui():
    top = tkinter.Tk()  # 視窗標題
    top.wm_title('Find Anagram')
    label = tkinter.Label(top, text="Word",font=18)
    label.grid(row=0, column=0, sticky='w')  # row,column 卡位非座標
    entry = tkinter.Entry(top, width=40, name='entry', borderwidth=2)  # 輸入視窗
    entry.grid(row=0, column=1, sticky='w')  # stick='w'--靠向west (E,W)
    entry.focus()  # 視窗開啟時會自動focus的欄位

    label2 = tkinter.Label(top, text="Anagrams",font=18)
    label2.grid(row=1, column=0, sticky='w')
    ans_out = tkinter.Text(top, height=8, width=40, name='ans out', borderwidth=2)
    ans_out.grid(row=1, column=1, sticky='w')

    entry.bind("<Return>", lambda event: find_anagrams(entry,ans_out))  # 按下enter="<Return>"

    top.update()
    tkinter.mainloop()


def read_dictionary(s):
    global lst
    lst = []
    with open(FILE, 'r') as text:
        for word in text:
            word = word.strip()
            if len(word) == len(s):  # 只存取長度一樣的單字加速查詢
                for letter in word:  # 存取有相同字母的單字
                    if letter not in s:
                        check = False
                        break
                    else:
                        check = True
                if check:
                    lst.append(word)


def find_anagrams(entry,ans_out):
    """
    :param s: 使用者輸入之字串
    """
    s = entry.get().strip().lower()
    read_dictionary(s)
    anagrams = []
    start = time.time()
    find_helper(s, '', anagrams)
    print(f'{len(anagrams)} anagrams: {anagrams}')

    # Show results in GUI
    ans_out.delete('1.0', 'end')  # 清除前一次的搜尋結果
    for word in anagrams:
        ans_out.insert('end', word+'\n')
    end = time.time()
    ans_out.insert('end', f'Time spent: {round((end - start), 4)} seconds') #只取到小數點後第四位
    print(f'The speed of your anagram algorithm: {end - start} seconds.')



def find_helper(s, anagram, anagrams):
    """
    :param s: 使用者輸入之字串
    :param anagram: 存在字典之字串
    :param anagram: 字串組合之list
     """
    if len(s) == 0:  # base case
        if anagram not in anagrams:
            anagrams.append(anagram)
            print(f"Found:   {anagram}")
            print("Searching...")
    else:
        for i in range(len(s)):
            # Choose
            anagram += s[i]
            if has_prefix(anagram) is True:  # 字首查詢，提前濾掉
                # Explore
                find_helper(s[0:i] + s[i+1:], anagram, anagrams)  # 將取過的字母移除
            # Un_choose
            anagram = anagram[:-1]


def has_prefix(sub_s):
    """
    :param sub_s: current anagram
    :return: bool, True:存在於lst, False:不存在
    """
    global lst
    for word in lst:
        if word.startswith(sub_s):
            return True
    return False


if __name__ == '__main__':
    main()
