import pandas as pd
from groq import Groq
import os
df= pd.read_csv("sales.csv")
total= df["Amount"].sum()
average = df["Amount"].mean()
highest= df["Amount"].max()
lowest= df["Amount"].min()

data_text= f"""
Total Sales= {total}
Average= {average}
Highest= {highest}
Lowest= {lowest}
"""
client= Groq(api_key=os.getenv("GROQ_API_KEY"))
response= client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system","content": "you are a helpful business assistant.Write short and clear summaries."},
        {"role": "user", "content": f"Write a short professional sales summary based on this data:\n{data_text}"}
    ]
)
ai_summary = response.choices[0].message.content

report = pd.DataFrame({
    "Matric": ["Total sales", "Average sale", "Highest sale","Lowest sale", "AI Summary"],
    "Value": [total, average, highest, lowest, ai_summary]
})
report.to_csv("AI_Sales_Report.csv", index=False)
print("AI Sales Report created successfully!")
