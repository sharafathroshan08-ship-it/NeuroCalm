import pandas as pd
data = pd.Series([1,6,11,777])
data[0]
data[1:4]
data = pd.Series([10,20,30,40],index = ['a','b','c','d'])
print(data)
print(data.values)
print(data.index)
students_dict = {'Ramu':991,'Shyam':992,'Arun':993}
students = pd.Series(students_dict)
print(students)
list1 = [['Ramu',1],['Shyam',2],['Arun',3]]
df = pd.DataFrame(list1,columns = ['Name','Roll.No'])
print(df)