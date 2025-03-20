import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

# OpenWeatherMapAPIから天気情報を取得
def get_weather(city):
    API_key = "2a821a2aa140e8a71e13cfbe23064b4c"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ja&units=metric&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("エラー", "都市が見つかりません")
        return None

    # 応答JSONを解析して天気情報を取得
    weather = res.json()
    print(weather)

    #try:    
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp']
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    # アイコンURLを取得して、全ての天気情報を返す
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)
    #except KeyError:
        #messagebox.showerror("エラー", "天気情報を取得できません")
        #return None

# 都市の天気を検索
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    # 都市が見つかったら、天気情報を解析する
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    # URLから天気アイコン画像を取得して、アイコンラベルを更新する
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # 気温と解説ラベルを更新
    temperature_label.configure(text=f"気温: {temperature:.2f}℃")
    description_label.configure(text=f"解説: {description}")

root = ttkbootstrap.Window(themename="vapor")
root.title("お天気アプリ")
root.geometry("400x400")

# ウィジェット起動 -> 都市名入力
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# ウィジェットボタン -> 天気情報の検索
search_button = ttkbootstrap.Button(root, text="検索", command=search, bootstyle="warning")
search_button.pack(pady=10)

# ウィジェットラベル -> 都市名/国名を表示
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# ウィジェットラベル -> 天気アイコンを表示
icon_label = tk.Label(root)
icon_label.pack()

# ウィジェットラベル -> 温度を表示
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack() 

# ウィジェットラベル -> 天気の解説を表示
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()