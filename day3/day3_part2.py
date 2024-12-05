from pathlib import Path
import re

def read_input():
   return Path("input.txt").read_text(encoding="utf-8")
data = read_input()
# Pre-process string

def _find_str_in_str_indices(data, query):
   window_length = len(query)
   return_value = set()
   for index in range(len(data) - window_length):
       candidate = data[index:index+window_length]
       if candidate == query:
           return_value.add(index)
   return return_value


false_index = _find_str_in_str_indices(data, "don't()")
true_index = _find_str_in_str_indices(data, "do()")


new_data = ""
reading = True
for index in range(len(data)):
   if index in true_index:
       reading = True
   elif index in false_index:
       reading = False
   elif reading:
       new_data += data[index]
data = new_data

data = re.sub(r"(don't\(\).*?do\(\))", "", data)
result = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)
total = sum(int(a) * int(b) for a, b in result)
print(total)

