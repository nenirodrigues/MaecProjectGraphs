import inline as inline
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import json
from pandas.io.json import json_normalize
from networkx.classes.reportviews import NodeView
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import collections


with open('C:/Users/Luciene/PycharmProjects/app/templates/package_dynamic_triagem_example.json', "r") as read_file:
 file_content = json.load(read_file)
data = json_normalize(file_content)
print(data)

objects = data.maec_objects
objects[0], type(objects[0])

print(objects[0][1])
print(objects[0][7])

column_names = objects[0][1].keys()
print(column_names)

values = [row.values() for row in objects[0]]
print(values)

new_df = pd.DataFrame(values,columns=column_names)

plt.figure(figsize=(10, 60))
new_df.type.value_counts().plot.bar()
plt.ylabel('Frequency', fontsize=16)
plt.xlabel(' Maec Objects', fontsize=16)
plt.show()

# dictionary with all observable objects
results = file_content['observable_objects']
print(type(results))
print(results)

# iteraction through the results (dictionaty) and print each line
for key in results.keys():
    values = results.values()
    print(values)
    print(type(values))

    # creates a list to hold the type values
    typList = []
    # loop over the dictionary
    for eachValue in values:
        print(type(eachValue))
        print(eachValue)

        typeOb = eachValue['type'] # and takes the value type
        typList.append(typeOb) # and stores in the list

# creates the graph horizontal
print(typList)
resultCounterByType = collections.Counter(typList) # counts the frequency by type and stores in a variable
names = list(resultCounterByType.keys())
valuesList = list(resultCounterByType.values())

index = names
df = pd.DataFrame({'Frequency2': valuesList}, index=index)
ax = df.plot.barh()
plt.show()


class_relationship = data['relationships'].iloc[0]
class_dfRelationship = pd.DataFrame(class_relationship)
print(class_dfRelationship.source_ref)

plt.figure(figsize=(10, 60))
class_dfRelationship.relationship_type.value_counts().plot.bar()
plt.ylabel('Frequency', fontsize=16)
plt.xlabel('Relashionship type', fontsize=16)
plt.show()