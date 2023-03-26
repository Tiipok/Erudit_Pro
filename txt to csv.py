import pandas as pd

df = pd.read_csv('dictionary.txt', sep='-')
writer.writerows(lines)
df.to_csv('dictionary.csv')