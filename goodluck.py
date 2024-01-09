# 记得导包
import pandas as pd
import requests

# API
base_url = "https://restapi.amap.com/v3/place/text"
township_url = "https://restapi.amap.com/v3/geocode/regeo"

# 定义params
# 把ffffffffff替换成你的key
# 高德开放平台 https://lbs.amap.com/ 里面有api详细的说明
params = {
    "key": "fffffffffff",
    "keywords": "输出你需要查找的内容",
    "types": "100000",
    "city": "南京",
    "children": "2",
    "offset": "25",
    "extensions": "base"
}

township_params = {
    "key": "fffffffffff",
    "poitype": "100000",
    "radius": "1",
    "extensions": "base",
    "roadlevel": "0"
}


# 用location查询街道
def gettownship(h_location):
    push_location = {"location": h_location}
    township_params.update(push_location)
    response_township = requests.get(township_url, params=township_params)
    town_data = response_township.json()
    township = town_data.get("regeocode", {}).get("addressComponent", {}).get("township", "")
    return township


hotel_data = []

for page in range(1, 10):  # 翻页，你要是只有一页就（1,1）
    params["page"] = str(page)

    # request
    response = requests.get(base_url, params=params)
    data = response.json()

    for poi in data["pois"]:
        name = poi.get("name", "")
        address = poi.get("address", "")
        adname = poi.get("adname", "")
        location = poi.get("location", "")
        township = gettownship(location)
        hotel_data.append(
            {"Name": name, "Address": address, "Adname": adname, "Location": location, "Township": township})
        print("Name", name, "Address", address, "Adname", adname, "Location", location, "Township", township)

df = pd.DataFrame(hotel_data)

# 写入
df.to_excel("output.xlsx", index=False)

# 你真幸运~
print("program over u are soo luck!!!")
