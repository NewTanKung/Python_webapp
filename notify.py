from flask import Flask , render_template, request,redirect, url_for, flash
from connection import connection_database, execute_data, execute_data_insert
import requests
import json

def add_noti(cus_prefix, cus_name, cus_tel, pro_name):
    url = "https://api.line.me/v2/bot/message/push"  # ใส่ URL ของ LINE Messaging API
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer QZff12kpZutrqF6xjBKbASKEuCokCgdaJjQkG8hoNzz"

    }

    message_text = {
        "type": "flex",
        "altText": "มีการเพิ่มสินค้าใหม่!",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ร้านคงเดชอวียวะ", "weight": "bold", "size": "xl"},
                    {
                        "type": "box",
                        "layout": "baseline",
                        "margin": "md",
                        "contents": [
                            {"type": "text", "text": "มีการเพิ่มสินค้า", "size": "sm", "color": "#999999"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {"type": "text", "text": "👦🏻 ลูกค้า", "color": "#aaaaaa", "size": "sm", "flex": 2},
                                    {"type": "text", "text": f"{cus_prefix} {cus_name}", "color": "#666666", "size": "sm", "flex": 5}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {"type": "text", "text": "📞 เบอร์", "color": "#aaaaaa", "size": "sm", "flex": 2},
                                    {"type": "text", "text": f"{cus_tel}", "color": "#666666", "size": "sm", "flex": 5}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {"type": "text", "text": "📦 สินค้า", "color": "#aaaaaa", "size": "sm", "flex": 2},
                                    {"type": "text", "text": f"{pro_name}", "color": "#666666", "size": "sm", "flex": 5}
                                ]
                            }
                        ]
                    }
                ]
            },
            "footer": {
                
            }
        }
    }

    # ห่อ Flex Message ให้ถูกต้อง
    payload = {
        "to": "USER_ID",
        "messages": [message_text]
    }

    res = requests.post(url, headers=headers, json=payload)

    # ตรวจสอบผลลัพธ์
    if res.status_code == 200:
        print("✅ ส่งแจ้งเตือนสำเร็จ!")
    else:
        print(f"❌ ส่งแจ้งเตือนไม่สำเร็จ: {res.text}")