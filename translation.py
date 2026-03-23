import requests, hashlib, random, re, time, os, json
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== 配置区域 ====================
#https://fanyi-api.baidu.com/manage/developer
APP_ID = "你的APP_ID"
SECRET_KEY = "你的密钥"

# 文件配置
INPUT_FILE = "qt_zh_CN.ts"
OUTPUT_FILE = "qt_zh_CN_translated.ts"
PROGRESS_FILE = "translation_progress.json"

# 性能配置
MAX_WORKERS = 10
SAVE_INTERVAL = 20
# ================================================

# 全局变量
interrupted = False
translated_map = {}
completed_indices = set()
results = {}
original_messages = []
content = ""

def signal_handler(signum, frame):
    """处理中断信号"""
    global interrupted
    if not interrupted:
        interrupted = True
        print("\n\n正在保存进度，请稍候...")
        save_all()
        print("进度已保存")
        sys.exit(0)

def save_all():
    """保存所有内容（进度文件 + 输出文件）"""
    global translated_map, completed_indices, results, original_messages
    
    # 保存进度文件
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "translated": translated_map,
                "completed_indices": list(completed_indices)
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存进度文件失败: {e}")
    
    # 生成并保存输出文件
    if original_messages and results:
        try:
            new_messages = []
            for i, msg in enumerate(original_messages):
                if i in results:
                    new_messages.append(results[i])
                else:
                    new_messages.append(msg)
            
            new_content = '\n'.join([f'<message>{msg}</message>' for msg in new_messages])
            
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"输出文件已保存: {OUTPUT_FILE}")
        except Exception as e:
            print(f"保存输出文件失败: {e}")

# 注册信号处理
signal.signal(signal.SIGINT, signal_handler)

def translate_text(text):
    """调用百度翻译API"""
    salt = random.randint(32768, 65536)
    sign = hashlib.md5(f"{APP_ID}{text}{salt}{SECRET_KEY}".encode()).hexdigest()
    
    for attempt in range(3):
        if interrupted:
            return text
        
        try:
            resp = requests.get("https://fanyi-api.baidu.com/api/trans/vip/translate",
                                params={"q": text, "from": "en", "to": "zh",
                                        "appid": APP_ID, "salt": salt, "sign": sign},
                                timeout=10)
            result = resp.json()
            
            if "trans_result" in result:
                return result["trans_result"][0]["dst"]
            else:
                error_msg = result.get("error_msg", "未知错误")
                if error_msg == "54003":
                    time.sleep(1)
                    continue
                return text
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
                continue
            return text
    return text

def load_progress():
    """加载进度"""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"translated": {}, "completed_indices": []}

def main():
    global translated_map, completed_indices, results, original_messages, content, interrupted
    
    print("=" * 60)
    print("百度翻译脚本")
    print("输入文件: " + INPUT_FILE)
    print("输出文件: " + OUTPUT_FILE)
    print("并发数: " + str(MAX_WORKERS))
    print("=" * 60)
    
    # 检查输入文件
    if not os.path.exists(INPUT_FILE):
        print("错误: 输入文件不存在 - " + INPUT_FILE)
        return
    
    # 读取文件
    print("\n读取文件: " + INPUT_FILE)
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取所有 message
    original_messages = re.findall(r'<message>(.*?)</message>', content, re.DOTALL)
    total = len(original_messages)
    print("共 " + str(total) + " 条 message")
    
    # 加载进度
    progress = load_progress()
    translated_map = progress.get("translated", {})
    completed_indices = set(progress.get("completed_indices", []))
    
    print("已完成: " + str(len(completed_indices)) + " 条")
    
    # 需要翻译的
    to_translate = []
    skip_empty = 0
    skip_chinese = 0
    skip_custom = 0
    
    for i, msg in enumerate(original_messages):
        if i in completed_indices:
            continue
        
        source_match = re.search(r'<source>(.*?)</source>', msg, re.DOTALL)
        trans_match = re.search(r'<translation[^>]*>(.*?)</translation>', msg, re.DOTALL)
        
        if source_match:
            source = source_match.group(1)
            translation = trans_match.group(1) if trans_match else ""
            
            # 判断是否需要翻译
            need_translate = False
            
            # 情况1: 翻译为空
            if not translation or translation.strip() == "":
                need_translate = True
                skip_empty += 1
            # 情况2: 翻译内容包含中文
            elif re.search(r'[\u4e00-\u9fff]', translation):
                # 已有中文，不需要翻译
                need_translate = False
                skip_chinese += 1
                completed_indices.add(i)
                translated_map[source] = translation
                print(f"跳过已有中文: [{i+1}] {source[:50]} -> {translation[:50]}")
            # 情况3: 翻译内容不为空，不包含中文，且与原文不同
            elif translation != source:
                # 自定义英文内容，不需要翻译
                need_translate = False
                skip_custom += 1
                completed_indices.add(i)
                translated_map[source] = translation
                print(f"跳过自定义内容: [{i+1}] {source[:50]} -> {translation[:50]}")
            # 情况4: 翻译内容与原文相同
            elif translation == source:
                need_translate = True
                skip_empty += 1
            
            if need_translate:
                to_translate.append((i, source, msg, translation))
    
    print(f"\n统计:")
    print(f"  空翻译或待翻译: {skip_empty} 条")
    print(f"  已有中文翻译: {skip_chinese} 条")
    print(f"  自定义内容: {skip_custom} 条")
    print(f"  需要翻译: {len(to_translate)} 条\n")
    
    if len(to_translate) == 0:
        print("没有需要翻译的条目")
        # 如果已经有结果，保存输出文件
        if results:
            save_all()
        return
    
    # 初始化 results 为已完成的条目
    for i in completed_indices:
        if i < len(original_messages):
            results[i] = original_messages[i]
    
    # 翻译函数
    def translate_item(item):
        idx, source, msg, old_trans = item
        
        if interrupted:
            return None
        
        chinese = translate_text(source)
        
        # 更新 message 内容
        if old_trans:
            new_msg = msg.replace('<translation>' + old_trans + '</translation>', 
                                  '<translation>' + chinese + '</translation>')
        else:
            new_msg = re.sub(
                r'<translation[^>]*>\s*</translation>',
                '<translation>' + chinese + '</translation>',
                msg,
                flags=re.DOTALL
            )
        
        return idx, new_msg, source, chinese
    
    # 并行翻译
    translated_count = 0
    start_time = time.time()
    
    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # 提交所有任务
            futures = {executor.submit(translate_item, item): item for item in to_translate}
            
            # 处理完成的任务
            for future in as_completed(futures):
                if interrupted:
                    # 取消未完成的任务
                    for f in futures:
                        f.cancel()
                    break
                
                try:
                    result = future.result(timeout=30)
                    if result is None:
                        continue
                    
                    idx, new_msg, source, chinese = result
                    results[idx] = new_msg
                    translated_map[source] = chinese
                    completed_indices.add(idx)
                    translated_count += 1
                    
                    # 计算速度
                    elapsed = time.time() - start_time
                    speed = translated_count / elapsed if elapsed > 0 else 0
                    
                    print("[" + str(idx+1) + "/" + str(total) + "] " + source[:50] + " -> " + chinese[:50] + " (速度: " + "{:.1f}".format(speed) + "条/秒)")
                    
                    # 定期保存进度和输出文件
                    if translated_count % SAVE_INTERVAL == 0:
                        save_all()
                        print("  [进度已保存] 已翻译 " + str(translated_count) + " 条")
                        
                except Exception as e:
                    print("  翻译失败: " + str(e))
                    continue
        
        # 最终保存
        if not interrupted:
            save_all()
        
    except KeyboardInterrupt:
        print("\n\n正在保存进度...")
        save_all()
        print("已保存 " + str(len(completed_indices)) + " 条翻译进度")
        print("输出文件已保存: " + OUTPUT_FILE)
        print("下次运行将从中断处继续")
        return
    
    if interrupted:
        print("\n翻译已中断，进度已保存")
        return
    
    # 清理进度文件
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    
    # 统计
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print("完成!")
    print("翻译条目: " + str(translated_count) + " 条")
    print("总耗时: " + "{:.1f}".format(elapsed) + " 秒 (" + "{:.1f}".format(elapsed/60) + " 分钟)")
    print("平均速度: " + "{:.1f}".format(translated_count/elapsed) + " 条/秒")
    print("输出文件: " + OUTPUT_FILE)
    print("=" * 60)

if __name__ == "__main__":
    main()