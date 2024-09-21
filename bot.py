import os
from openai import OpenAI
from booking import Booking, datetime_str

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

prompt="""
你是一個記帳機器人，當你看到輸入的文字跟金額，你要分析它屬於哪個主類別、子類別，並且把所有項目拆開記帳。

主類別:
- 食品酒水
- 居家物業
- 行車交通

食品酒水子類別:
- 早餐
- 午餐
- 晚餐

居家物業子類別:
- 日常用品
- 水電瓦斯

行車交通子類別:
- 公共交通費
- 計程車費

回傳的格式如下
['主類別', '子類別', '金額', '說明']

例如當我輸入 '早餐 50元, 捷運加值 100元' 請回傳

['食品酒水', '早餐', 50, '']
['行車交通', '公共交通費', 100, '捷運加值']

如果沒有看到明細與金額，你判斷內容跟記帳無關，那就回傳這個陣列 ['', '', 0, '']
"""

def analyze(message):
  chat_completion = client.chat.completions.create(
      messages=[
          {
              "role": "user",
              "content": prompt ,
          },
          {
              "role": "user",
              "content": message,
          }
      ],
      model="gpt-3.5-turbo",
  )

  return parse(chat_completion.choices[0].message.content)

def parse(result):
  bookings = []
  for row in result.split('\n'):
    d = eval(row)
    bookings.append(Booking(
      datetime=datetime_str(),
      main_cat=d[0],
      sub_cat=d[1],
      expense=int(d[2]),
      income=0,
      description=d[3]))
  return bookings

if __name__ == '__main__':
    print(analyze("我想要跟你說"))