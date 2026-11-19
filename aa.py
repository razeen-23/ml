import pandas as pd
df = pd.read_csv("Housee.csv")
# print(df.isnull())
# print(df.isnull().sum())
# print(df.isna().sum())
# df.fillna(0)
# asd= df["Bedrooms"].mean()
# df["Bedrooms"] = df["Bedrooms"].fillna(asd)

# print(df["Bedrooms"].isnull())
# print(df.fillna(0))
# df['Bedrooms'].to_numeric('errors=coerce')

# df['Bedrooms'] = df['Bedrooms'].astype(int)
df['Bedrooms'] = df['Bedrooms'].replace({
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5'
})

df['Bedrooms'] = pd.to_numeric(df['Bedrooms'], errors='coerce')

df['Bedrooms'] = df['Bedrooms'].fillna(df['Bedrooms'].median()).astype(int)

print(df['Bedrooms'].unique())


df.fillna(0)
print(df)