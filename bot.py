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
- 交流通訊
- 休閒娛樂
- 進修學習
- 人情往來
- 醫療保健
- 金融保險
- 其他雜項

食品酒水子類別:
- 早餐
- 午餐
- 晚餐
- 菸酒茶飲料
- 水果零食
- 吃餐廳
- 吃點心

居家物業子類別:
- 日常用品
- 水電瓦斯
- 房租房貸
- 買衣服
- 大型家電
- 剪頭髮

行車交通子類別:
- 公共交通費
- 計程車費
- 汽機車加油費
- 火車飛機費
- 停車費
- 租車
- 汽機車保養
- 其他

交流通訊子類別:
- 電話費
- 手機費
- 網路費
- 有線電視費

休閒娛樂子類別:
- 運動健身
- 朋友聚餐
- 休閒玩樂
- 寵物寶貝
- 旅遊度假
- 奢侈敗家
- 藝文展演
- 看電影
- Karaoke

進修學習子類別:
- 書報雜誌
- 上課進修
- 網上學習
- 報名考試
- 寒暑期營隊

人情往來子類別:
- 送禮請客
- 尊親費用
- 慈善捐款

醫療保健子類別:
- 生病醫療
- 勞健保費
- 保險費用
- 健康食品
- 美容養生
- 健康檢查

金融保險子類別:
- 銀行手續
- 投資損益
- 分期付款
- 稅捐支出
- 賠償罰款
- 儲蓄
- 保險費用

其他雜項子類別:
- 其他支出
- 遺失拾獲
- 呆帳遺失

回傳的格式如下
['主類別', '子類別', '支出金額', '收入金額', '說明']

例如當我輸入 '早餐 50元, 捷運加值 100元' 請回傳

['食品酒水', '早餐', 50, 0, '']
['行車交通', '公共交通費', 100, 0, '捷運加值']

當你判斷這是一筆收入，例如當我輸入 '收入 60,000' 請回傳

['家用收入', '薪水收入', 0, 60000, '']

如果沒有看到明細與金額，你判斷內容跟記帳無關，那就回傳這個陣列 ['', '', 0, 0, '']
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

  result = chat_completion.choices[0].message.content
  print(result)
  return parse(result)

def parse(result):
  bookings = []
  for row in result.split('\n'):
    d = eval(row)
    bookings.append(Booking(
      datetime=datetime_str(),
      main_cat=d[0],
      sub_cat=d[1],
      expense=int(d[2]),
      income=int(d[3]),
      description=d[4],
      owner='',
      )
    )
  return bookings

if __name__ == '__main__':
    print(analyze("收入 1000000元"))