#!/usr/bin/env python3
"""
测试可灵图生图 - 赛博朋克风格转换 (修正时间戳)
"""

import os
import json
import time
import base64
import hmac
import hashlib
import requests
from datetime import datetime, timedelta

API_BASE = "https://api-beijing.klingai.com"
ACCESS_KEY = "A4rGGPTLAtK9aB3LERL4f4d8bnA4mPbL"
SECRET_KEY = "eHLQN4nahrYeYAMrmkYQnPbmGdrKHdDG"


def base64url_encode(data: bytes) -> str:
    """Base64URL编码"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def generate_jwt_token(access_key: str, secret_key: str) -> str:
    """生成JWT鉴权Token (原生实现，使用当前UTC时间)"""
    
    # Header
    header = json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(',', ':'))
    header_b64 = base64url_encode(header.encode())
    
    # Payload - 使用当前时间
    now = int(time.time())  # 使用time.time()获取UTC时间戳
    payload = json.dumps({
        "iss": access_key,
        "iat": now,
        "nbf": now - 60,  # 提前60秒生效，避免时间偏差
        "exp": now + 3600  # 1小时后过期
    }, separators=(',', ':'))
    payload_b64 = base64url_encode(payload.encode())
    
    # Signature
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    signature_b64 = base64url_encode(signature)
    
    token = f"{message}.{signature_b64}"
    print(f"生成的Token: {token[:50]}...")
    print(f"当前时间戳: {now}")
    return token


def create_image_to_image_task(image_base64: str, prompt: str):
    """创建图生图任务"""
    
    token = generate_jwt_token(ACCESS_KEY, SECRET_KEY)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model_name": "kling-v3",
        "prompt": prompt,
        "image": image_base64,
        "image_reference": "subject",
        "image_fidelity": 0.6,
        "resolution": "2k",
        "n": 1,
        "aspect_ratio": "1:1"
    }
    
    url = f"{API_BASE}/v1/images/generations"
    
    print(f"发送请求到: {url}")
    print(f"提示词: {prompt}")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        print(f"状态码: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


def query_task(task_id: str):
    """查询任务状态"""
    
    token = generate_jwt_token(ACCESS_KEY, SECRET_KEY)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = f"{API_BASE}/v1/images/generations/{task_id}"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"查询失败: {e}")
        return None


def wait_for_task(task_id: str, timeout: int = 300):
    """等待任务完成"""
    print(f"\n等待任务完成，任务ID: {task_id}")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        result = query_task(task_id)
        
        if not result:
            print("查询失败，重试中...")
            time.sleep(5)
            continue
        
        if result.get("code") != 0:
            print(f"查询失败: {result.get('message')}")
            return result
        
        task_data = result.get("data", {})
        status = task_data.get("task_status")
        
        print(f"当前状态: {status}")
        
        if status == "succeed":
            print("\n✅ 任务完成！")
            images = task_data.get("task_result", {}).get("images", [])
            for img in images:
                print(f"生成图片URL: {img.get('url')}")
            return result
        elif status == "failed":
            print(f"\n❌ 任务失败: {task_data.get('task_status_msg', '未知错误')}")
            return result
        
        time.sleep(5)
    
    print("\n⏱️ 等待超时")
    return None


def main():
    # 读取图片
    image_path = "/Users/admin/.openclaw/qqbot/downloads/6468642F95938263E9F207DFEFF18A27_1773978082891.png"
    print(f"读取图片: {image_path}")
    
    with open(image_path, 'rb') as f:
        img_data = f.read()
        image_base64 = base64.b64encode(img_data).decode('utf-8')
    
    print(f"图片Base64长度: {len(image_base64)} 字符")
    
    # 赛博朋克风格提示词
    prompt = "将原图转换为赛博朋克风格，霓虹灯光，未来科技感，蓝紫色色调，发光元素，科幻氛围，高对比度"
    
    # 创建任务
    result = create_image_to_image_task(image_base64, prompt)
    
    if not result:
        print("创建任务失败")
        return
    
    print(f"\n创建任务响应:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get("code") != 0:
        print(f"创建任务失败: {result.get('message')}")
        return
    
    task_data = result.get("data", {})
    task_id = task_data.get("task_id")
    
    if task_id:
        # 等待任务完成
        final_result = wait_for_task(task_id)
        if final_result:
            print("\n最终结果:")
            print(json.dumps(final_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
