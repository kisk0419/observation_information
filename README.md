# 群馬県雨量／水位観測情報取得アプリ サンプル

## 概要

群馬県水位雨量情報システムHPから雨量と水位をスクレイピングして取得するアプリである。  
取得したデータはJSON形式で取得することができる。

## 環境
### 開発言語
Python 3.7.4
### 必要ライブラリ
requests, beautiful soup, pytest

## サンプル起動方法

### ライブラリインストール
```
> pip install requests
> pip install bs4
> pip install pytest
```

### サンプルアプリ実行
```
> python main.py
```
## アプリ組み込み方法
### 雨量一覧取得
```
from controller.rainfall.factory.rainfall_list_factory import RainfallListFactory

factory = RainfallListFactory('scraping')
c = factory.create_controller()
json_data = c.get()
```
### 雨量経過取得
```
from controller.rainfall.factory.rainfall_factory import RainfallFactory

factory = RainfallFactory('scraping')
c = factory.create_controller()
json_data = c.get()
```
### 水位一覧取得
```
from controller.waterlevel.factory.waterlevel_list_factory import WaterlevelListFactory

factory = WaterlevelListFactory('scraping')
c = factory.create_controller()
json_data = c.get()
```
### 水位経過取得
```
from controller.waterlevel.factory.waterlevel_factory import WaterlevelFactory

factory = WaterlevelFactory('scraping')
c = factory.create_controller()
json_data = c.get()
```

## JSONフォーマット
### 雨量一覧取得
```
{
    "rainfall_summaries": [
        {
            "observation_name": "四万川ダム", 
            "amount_10m": "0.0", 
            "amount_60m": "", 
            "amount_1h": "", 
            "amount_3h": "", 
            "amount_6h": "", 
            "amount_24h": "", 
            "amount_total": "7.0", 
            "start_time": "10月09日 11時10分", 
            "office_name": "中之条土木", 
            "city_name": "中之条町"
        }
    ]
}
```

### 雨量経過取得
```
{
    "rainfalls": [
        {
            "unit": "10", 
            "observation_name": "四万川ダム", 
            "start_time": "10/09 11:10", 
            "timelines": [
                {
                    "datetime": "10/09 15:10", 
                    "unit_amount": "0.0", 
                    "total_amount": "5.0"
                }, 
            ]
        }
    ]
}
```

### 水位一覧取得
```
{
    "waterlevel_summaries": [
        {
            "observation_name": "市城", 
            "waterlevel": "0.68", 
            "level_mark": "→", 
            "stage_lv1": "3.20", 
            "stage_lv2": "4.50", 
            "stage_lv3": "-", 
            "stage_lv4": "-", 
            "stage_lv8": "-", 
            "office_name": "中之条土木", 
            "river_name": "吾妻川", 
            "city_name": "中之条町"
        }
    ]
}
```

### 水位経過取得
```
{
    "waterlevels": [
        {
            "unit": "10", 
            "observation_name": "市城", 
            "stage_lv1": "3.20", 
            "stage_lv2": "4.50", 
            "stage_lv3": "-", 
            "stage_lv4": "-", 
            "stage_lv8": "-", 
            "river_name": "河川名", 
            "timelines": [
                {
                    "datetime": "10/09 15:10", 
                    "waterlevel": "0.63", 
                    "level_mark": "↑"
                }
            ]
        }
    ]
}
```

## 制限事項

- URLなどべた書きハードコーディング
- 日付、時刻が未処理
  
