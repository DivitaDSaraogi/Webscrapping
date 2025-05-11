import pandas as pd
import zipfile
from io import BytesIO
import matplotlib.pyplot as plt

# Step 1: Load the ZIP file
zip_path = "names.zip"  # replace with your actual zip file path
all_data = []

with zipfile.ZipFile(zip_path) as z:
    # Extract only files that start with 'yob' and end with '.txt'
    data_files = [f for f in z.namelist() if f.startswith("yob") and f.endswith(".txt")]
    
    for file_name in data_files:
        year = int(file_name[3:7])
        df = pd.read_csv(BytesIO(z.read(file_name)), encoding='utf-8', engine='python', header=None)
        df.columns = ['Name', 'Sex', 'Births']
        df['Year'] = year
        all_data.append(df)

# Step 2: Combine all years into one DataFrame
data = pd.concat(all_data)

# Step 3: Visualize births by gender per year
gender_year = data.groupby(['Year', 'Sex'])['Births'].sum().unstack()
gender_year.plot(kind='line', figsize=(12, 6), title='Number of Male and Female Births Per Year')
plt.ylabel('Number of Births')
plt.grid(True)
plt.show()

# Step 4: Find Top 100 Baby Names (all years combined)
top_100 = data.groupby('Name')['Births'].sum().sort_values(ascending=False).head(100)
print("Top 10 Baby Names:\n", top_100.head(10))

# Optional: Visualize top 10 names
top_10 = top_100.head(10)
top_10.plot(kind='bar', figsize=(10, 5), title='Top 10 Most Popular Baby Names (1880–2022)', color='skyblue')
plt.ylabel('Total Births')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
