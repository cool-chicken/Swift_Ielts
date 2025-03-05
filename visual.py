import pandas as pd
from datetime import datetime

def record_user_info(user_id, essay_score, time_spent):
    data = {
        "User ID": [user_id],
        "Essay Score": [essay_score],
        "Time Spent (minutes)": [time_spent],
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    df = pd.DataFrame(data)
    df.to_excel("user_records.xlsx", index=False, mode='a', header=not os.path.exists("user_records.xlsx"))

# 示例调用
user_id = "user123"
essay_score = 7.5
time_spent = 30
record_user_info(user_id, essay_score, time_spent)