---
name: kling-image-generate
description: 可灵AI图像生成API工具。支持文生图、图生图、多图参考生成、图像Omni、扩图、虚拟试穿等功能。使用环境变量KLING_ACCESS_KEY和KLING_SECRET_KEY进行鉴权。当用户需要生成AI图像、图片编辑、图像扩展等任务时使用此技能。
---

# 可灵图像生成 API

可灵AI图像生成服务，提供多种图像生成和编辑能力。

## 环境变量配置

```bash
export KLING_ACCESS_KEY="your_access_key"
export KLING_SECRET_KEY="your_secret_key"
```

## 支持的图像API

### 1. 图像生成 (Image Generation)
标准文生图和图生图接口。

**接口：** `POST /v1/images/generations`

**主要参数：**
- `model_name`: 模型名称 (kling-v1, kling-v1-5, kling-v2, kling-v2-new, kling-v2-1, kling-v3)
- `prompt`: 正向提示词 (必填，最多2500字符)
- `negative_prompt`: 负向提示词
- `image`: 参考图片 (URL或Base64)
- `image_reference`: 图片参考类型 (subject/face)
- `image_fidelity`: 图片参考强度 [0,1]
- `human_fidelity`: 面部参考强度 [0,1] (仅subject类型)
- `element_list`: 主体参考列表
- `resolution`: 清晰度 (1k, 2k)
- `n`: 生成数量 [1,9]
- `aspect_ratio`: 宽高比 (16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9)
- `watermark_info`: 是否生成带水印图片
- `callback_url`: 回调通知地址
- `external_task_id`: 自定义任务ID

**查询任务：**
- 单个任务：`GET /v1/images/generations/{id}`
- 任务列表：`GET /v1/images/generations?pageNum=1&pageSize=30`

### 2. 图像Omni (Omni-Image)
支持多图参考、主体参考的高级图像生成。

**接口：** `POST /v1/images/omni-image`

**主要参数：**
- `model_name`: 模型名称 (kling-image-o1, kling-v3-omni)
- `prompt`: 提示词 (支持 `<<<image_1>>>` 格式引用图片)
- `image_list`: 参考图列表 (最多10张)
- `element_list`: 主体参考列表
- `resolution`: 清晰度 (1k, 2k, 4k)
- `result_type`: 结果类型 (single/series)
- `n`: 生成数量 [1,9] (series时无效)
- `series_amount`: 组图数量 [2,9] (series时有效)
- `aspect_ratio`: 宽高比
- `watermark_info`: 水印信息
- `callback_url`: 回调地址
- `external_task_id`: 自定义任务ID

**查询任务：**
- 单个任务：`GET /v1/images/omni-image/{id}`
- 任务列表：`GET /v1/images/omni-image?pageNum=1&pageSize=30`

### 3. 多图参考生图 (Multi Image to Image)
基于多张参考图生成图像。

**接口：** `POST /v1/images/multi-image-to-image`

### 4. 扩图 (Image Expansion)
智能扩展图像边界。

**接口：** `POST /v1/images/editing/expand`

**主要参数：**
- `image`: 参考图片 (必填，URL或Base64)
- `up_expansion_ratio`: 向上扩展比例 [0,2]，基于原图高度
- `down_expansion_ratio`: 向下扩展比例 [0,2]，基于原图高度
- `left_expansion_ratio`: 向左扩展比例 [0,2]，基于原图宽度
- `right_expansion_ratio`: 向右扩展比例 [0,2]，基于原图宽度
- `prompt`: 正向提示词
- `n`: 生成数量 [1,9]
- `watermark_info`: 水印信息
- `callback_url`: 回调地址
- `external_task_id`: 自定义任务ID

**限制：** 新图片整体面积不得超过原图片3倍

**查询任务：**
- 单个任务：`GET /v1/images/editing/expand/{id}`
- 任务列表：`GET /v1/images/editing/expand?pageNum=1&pageSize=30`

### 5. 智能补全主体图 (AI Multi Shot)
智能补全主体图像。

**接口：** `POST /v1/images/ai-multishot`

### 6. 虚拟试穿 (Virtual Try-On)
虚拟试穿功能。

**接口：** `POST /v1/images/virtual-try-on`

## 通用信息

### API端点
```
https://api-beijing.klingai.com
```

### 鉴权方式
使用 Access Key 和 Secret Key 生成 JWT Token。

**请求头：**
```
Authorization: Bearer <token>
Content-Type: application/json
```

### 任务状态
- `submitted`: 已提交
- `processing`: 处理中
- `succeed`: 成功
- `failed`: 失败

### 图片限制
- 格式：jpg, jpeg, png
- 大小：不超过10MB
- 尺寸：不小于300px
- 宽高比：1:2.5 ~ 2.5:1
- Base64：不要添加 `data:image/png;base64,` 前缀

## 使用脚本

技能包含以下脚本：

- `scripts/generate_image.py` - 图像生成（基础版）
- `scripts/generate_image_with_progress.py` - 图像生成（带进度估算，推荐）
- `scripts/generate_omni_image.py` - Omni图像生成
- `scripts/expand_image.py` - 图像扩图
- `scripts/query_task.py` - 查询任务状态
- `scripts/list_tasks.py` - 获取任务列表

## 使用示例

### 文生图（带进度显示）
```bash
python3 scripts/generate_image_with_progress.py \
  --prompt "一只可爱的猫咪，皮克斯风格" \
  --model kling-v3 \
  --n 2 \
  --aspect_ratio 1:1 \
  --resolution 2k \
  --wait
```

### 图生图（带进度显示）
```bash
python3 scripts/generate_image_with_progress.py \
  --prompt "保持原图风格，添加花朵装饰" \
  --image "https://example.com/image.png" \
  --image_reference subject \
  --image_fidelity 0.7 \
  --wait
```

**进度显示示例：**
```
==================================================
任务ID: 863816447528013833
任务类型: image2image
预计耗时: 35秒
==================================================

[11:47:23] 状态: SUBMITTED
[░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 5% 等待处理... 已等待 3秒

[11:47:28] 状态: PROCESSING  (耗时: 5秒)
[████████████████░░░░░░░░░░░░░░] 65% 处理中... 预计还需 15秒

[11:47:35] 状态: SUCCEED
[██████████████████████████████] 100%

==================================================
✅ 任务完成！
总耗时: 35秒
==================================================
```

### 基础版脚本（不带进度）
```bash
# 文生图
scripts/generate_image.py \
  --prompt "一只可爱的猫咪，皮克斯风格" \
  --model kling-v3 \
  --n 2 \
  --aspect_ratio 1:1

# 图生图
scripts/generate_image.py \
  --prompt "保持原图风格，添加花朵装饰" \
  --image https://example.com/image.png \
  --image_reference subject \
  --image_fidelity 0.7
```

### Omni多图生成
```python
scripts/generate_omni_image.py \
  --prompt "将<<<image_1>>>的风格应用到<<<image_2>>>的人物上" \
  --images "url1,url2" \
  --model kling-v3-omni \
  --resolution 2k
```

### 扩图
```python
scripts/expand_image.py \
  --image https://example.com/image.png \
  --up 0.15 \
  --down 0.15 \
  --left 0.65 \
  --right 0.65 \
  --prompt "扩展区域保持海洋风景" \
  --n 2
```

### 自动计算扩图比例
```python
scripts/expand_image.py \
  --image https://example.com/image.png \
  --auto_ratio \
  --width 1000 \
  --height 1000 \
  --area_multiplier 3.0 \
  --aspect_ratio 1.77
```

### 查询任务
```python
scripts/query_task.py --task_id "task_xxx"
```
