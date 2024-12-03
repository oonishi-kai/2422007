import requests
import flet as ft
from datetime import datetime

# 地域リストのURL
AREA_LIST_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
# 地域ごとの天気情報URLフォーマット
FORECAST_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"

REGIONS = {
    "北海道地方": ["011000","012000","013000","014030","014100","015000","016000","017000"],
    "東北地方": ["020000", "030000", "040000", "050000", "060000", "070000"],
    "関東甲信地方": ["080000","090000","100000","110000","120000","130000","140000","190000","200000"],
    "東海地方": ["210000","220000","230000","240000"],
    "北陸地方": ["150000","160000","170000","180000"],
    "近畿地方": ["250000","260000","270000","280000","290000","300000"],
    "中国地方": ["310000","320000","330000","340000"],
    "四国地方": ["360000","370000","380000","390000"],
    "九州地方": ["400000","410000","420000","430000","440000","450000","460000","470000"],
    "沖縄地方": ["471000","472000","473000","474000"]
}

# 地域リストを取得
def get_area_list():
    response = requests.get(AREA_LIST_URL)
    response.raise_for_status()
    area_data = response.json()
    areas = []

    # 地域リストを生成
    for region_code, region_info in area_data['offices'].items():
        areas.append((region_code, region_info['name']))
    return areas

def get_weather_forecast(region_code):
    forecast_url = FORECAST_URL_TEMPLATE.format(region_code)
    response = requests.get(forecast_url)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
        return [{"date": "N/A", "weather": "取得エラー", "tempMax": "N/A", "tempMin": "N/A"}]

    forecast_data = response.json()

    weather_data = []

    try:
        area_forecasts = forecast_data[0]['timeSeries'][0]['areas']
        date_series = forecast_data[0]['timeSeries'][0]['timeDefines']

        # 温度データの取得
        temp_max_series = None
        temp_min_series = None
        for time_series in forecast_data:
            for series in time_series['timeSeries']:
                if 'tempsMax' in series['areas'][0]:
                    temp_max_series = series['areas'][0]['tempsMax']
                if 'tempsMin' in series['areas'][0]:
                    temp_min_series = series['areas'][0]['tempsMin']

        for i in range(3):  # 3日分のデータを取得
            date = datetime.strptime(date_series[i], "%Y-%m-%dT%H:%M:%S%z").date()
            weather = area_forecasts[0]['weathers'][i]
            temp_max = temp_max_series[i] if temp_max_series and len(temp_max_series) > i else "N/A"
            temp_min = temp_min_series[i] if temp_min_series and len(temp_min_series) > i else "N/A"
            weather_data.append({
                "date": date,
                "weather": weather,
                "tempMax": temp_max,
                "tempMin": temp_min
            })

    except (IndexError, KeyError) as e:
        print(f"Data Error: {e}")
        return [{"date": "N/A", "weather": "データ取得エラー", "tempMax": "N/A", "tempMin": "N/A"}]

    return weather_data

def main(page: ft.Page):
    region_dropdown = ft.Dropdown(
        label="地方を選択してください",
        hint_text="地方を選択",
        options=[ft.dropdown.Option(key=region, text=region) for region in REGIONS.keys()]
    )

    prefecture_dropdown = ft.Dropdown(label="県を選択してください", hint_text="県")

    weather_info = ft.Row(wrap=True, spacing=10)

    def on_region_select(e):
        selected_region = region_dropdown.value
        prefecture_options = [
            ft.dropdown.Option(key=code, text=name)
            for code, name in get_area_list()
            if any(code.startswith(region_code) for region_code in REGIONS[selected_region])
        ]
        prefecture_dropdown.options = prefecture_options
        prefecture_dropdown.update()

    def on_prefecture_select(e):
        region_code = prefecture_dropdown.value
        print(f"Selected region code: {region_code}")
        if region_code:
            weather_info.controls.clear()
            forecast = get_weather_forecast(region_code)
            for day in forecast:
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(f"日付: {day['date']}"),
                                ft.Text(f"天気: {day['weather']}"),
                                ft.Text(f"最高気温: {day['tempMax']}"),
                                ft.Text(f"最低気温: {day['tempMin']}"),
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=10,
                    ),
                    elevation=5,
                )
                weather_info.controls.append(card)
            page.update()

    region_dropdown.on_change = on_region_select
    prefecture_dropdown.on_change = on_prefecture_select

    page.add(
        ft.Column(
            [
                ft.Text("天気予報", size=24, weight="bold"),
                region_dropdown,
                prefecture_dropdown,
                weather_info
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)