"""
File: boggle.py
Name:Yipin
----------------------------------------
TODO:
"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'


def main():
	"""
	將輸入之字母每行為一list,四個list再存成list(rows)
	並將所有字存在list(all_letters)
	藉由read_dictionary()將字典裡長度大於4，並且單字裡沒有不在all_letters的字母，存成list(lst)
	藉由find_word()查找單字
	"""
	####################
	rows = []
	all_letters = []
	legal = True
	for i in range(1, 5):
		if legal:
			row = input(f"{i} row letter: ").lower().split()
			if len(row) == 4:
				for ch in row:
					if len(ch) != 1 or ch.isalpha() is False:
						legal = False
						break
				if legal:
					rows.append(row)
					all_letters += row
			else:
				legal = False
				break

	if not legal:
		print("Illegal input")
	else:
		start = time.time()
		print(rows)
		lst = read_dictionary(all_letters)
		find_word(lst, rows)
		end = time.time()
		print('----------------------------------')
		print(f'The speed of your boggle algorithm: {end - start} seconds.')
####################


def read_dictionary(all_letters):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	lst = []
	with open(FILE, 'r') as text:
		for word in text:
			word = word.strip()
			# 只存入長度大於等於4的單字
			if len(word) >= 4:
				for i in range(4):
					if word[i] not in all_letters:
						check = False
						break
					else:
						check = True
					if check:
						lst.append(word)
	return lst


def find_word(lst, rows):
	# 以4x4的的表格的row&column座標來選起始字母
	# 以find_helper()找起始字母與周圍8個字母的組合，藉由recursion串接字母
	words = []
	for row in range(4):
		for column in range(4):
			check_list = [(row, column)]
			find_helper(rows, lst, rows[row][column], words, row, column, check_list)
	print(f'There are {len(words)} words in total')


def find_helper(rows, lst, word, words, row, column, check_lst):
	"""
	:param rows: (list) 存所有輸入的字母
	:param lst: (list) 存有字典的單字
	:param word: (str)
	:param words: (list) 存有符合字典的單字
	:param row, column: (int) 4x4 row & column
	:param check_lst: (list) 為確保不會重複選字，將word內的字的所有row,column存入
	no return
	"""
	# 當word長度>=4,存在於字典，就存入words
	# 沒有base case
	if len(word) >= 4:
		if word in lst and word not in words:  # back case
			words.append(word)
			print(f'Found \'{word}\'')
	# 即使存入words後的word也須持續找符合的字母
	for i in range(-1, 2, 1):
		for j in range(-1, 2, 1):
			if 4 > row+i >= 0 and 4 > column+j >= 0 and (row+i, column+j) not in check_lst:
				# Choose
				word += rows[row+i][column+j]
				check_lst.append((row+i, column+j))
				if has_prefix(word, lst):
					# Explore
					find_helper(rows, lst, word, words, row+i, column+j, check_lst)
				# Un-choose
				word = word[:-1]
				check_lst.pop()


def has_prefix(sub_s, lst):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	for word in lst:
		if word.startswith(sub_s):
			return True
	return False


if __name__ == '__main__':
	main()
