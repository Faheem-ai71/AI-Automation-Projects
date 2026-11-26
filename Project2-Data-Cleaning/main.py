import pandas as pd
from groq import Groq
import os
df= pd.read_csv("lead_cleaner.csv")
df= df.dropna(how= 'all')
df= df.fillna("not Available")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
score = []
reason= []

for index, row in df.iterrows():
    lead_info = f"Name: {row['Name']}, Email: {row['Email']}, City: {row['City']},Interst:{row['Interst']}"

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role":"system","content":"you are a sales expert. Score the lead as Hot ,Warm or Cold and give a short reason."},
            {"role":"user","content":f"Score this lead:{lead_info}"}
        ]
    )
    ai_reply = response.choices[0].message.content
    score.append(ai_reply.split()[0])
    reason.append(ai_reply)
df["AI_Score"]= score
df["AI_Reason"]=reason

df.to_csv("scored_leads.csv",index=False)
print("complete")
