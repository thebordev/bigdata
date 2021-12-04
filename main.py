from pyspark import SparkContext
import string
from string import digits
sc=SparkContext("local","PySpark")

RDD_file=sc.textFile("test.txt")
data_file=RDD_file.collect()
existing_items=[]

#Removing Punctuations
for i in data_file:
    items = str(i)

    aux_words = string.punctuation
    existing_items.append(items.translate(None,digits).translate(None,aux_words).lower().replace("  "," ").strip())

print (existing_items)
RDD_file=sc.parallelize(existing_items)


#Function for word pair in same line
def sample(items):
    condition=[]
    output=[]
    for i in range(len(items)):
        if items[i] not in condition:
            condition.append(items[i])
            for j in range(len(items)):
                if i!=j:
                    output.append((items[i],items[j]))
    return output

#Mapping and Reducing
result=(
    RDD_file.filter(lambda line:line!="")
    .map(lambda word:word.split(" "))
    .flatMap(lambda word:sample(word))
    .filter(lambda value:value[0]!="")
    .map(lambda pair:(pair,1))
    .reduceByKey(lambda a,b:a+b).collect()
)
print(len(result))
print (result)


with open("kasi_output.txt","w") as file_name:
    file_name.write("[")
    for t in result:
        file_name.write(' '.join(str(s) for s in t)+",")
    file_name.write("]")
    file_name.close()
