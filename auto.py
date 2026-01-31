import uiautomator2 as u2
import requests
from bs4 import BeautifulSoup
import time
import math
import cv2
import numpy as np
import easyocr
import keyboard
import re
import warnings
from collections import Counter

# --- SILENCE WARNINGS ---
warnings.filterwarnings("ignore", category=UserWarning) 

# ==========================================
# 1. CONFIGURATION
# ==========================================
CENTER = (545, 1753)
TOP_POINT = (545, 1521)

# Geometry Calculations
RADIUS = int(math.sqrt((TOP_POINT[0]-CENTER[0])**2 + (TOP_POINT[1]-CENTER[1])**2))
NEXT_BTN_Y = CENTER[1] + RADIUS - 50 
NEXT_BTN_AREA = (CENTER[0], NEXT_BTN_Y)
SKIP_BTN_AREA = (545, 1870) 

# Solver URLs
URL_RAIDERS = "https://wordraiders.com/wordfinder-results/"
URL_COLLECT = "https://wordcollectanswers.com/en/?letters={}"

OCR_ALLOWLIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Shared Session for networking
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Origin': 'https://wordraiders.com',
    'Referer': 'https://wordraiders.com/'
})

# ==========================================
# 2. HELPER: STRICT GAME STATE DETECTION
# ==========================================
def get_game_state(d):
    """ Returns 'PLAYING', 'LEVEL_END', or 'UNKNOWN' """
    try:
        img = d.screenshot(format='opencv')
        
        # --- CHECK 1: NEXT BUTTON (Orange/Yellow) ---
        ny, nx = NEXT_BTN_AREA[1], NEXT_BTN_AREA[0]
        if ny < img.shape[0] and nx < img.shape[1]:
            pixel_btn = img[ny, nx]
            bb, gg, rr = int(pixel_btn[0]), int(pixel_btn[1]), int(pixel_btn[2])
            is_orange_btn = (rr > 180) and (gg > 130) and (bb < 100)
        else:
            is_orange_btn = False

        # --- CHECK 2: CENTER PIXEL (The Wheel) ---
        cy, cx = CENTER[1], CENTER[0]
        pixel_center = img[cy, cx]
        b, g, r = int(pixel_center[0]), int(pixel_center[1]), int(pixel_center[2])
        
        brightness = r + g + b
        is_bright_popup = brightness > 400 
        is_dark_green = (g > r + 15) and (g > b + 15) and (brightness < 350)

        if is_orange_btn or is_bright_popup:
            return 'LEVEL_END'
        elif is_dark_green:
            return 'PLAYING'
        else:
            return 'UNKNOWN'
    except:
        return 'UNKNOWN'

# ==========================================
# 3. GEOMETRY ENGINE
# ==========================================
def get_perfect_coords(num_letters):
    cx, cy = CENTER
    tx, ty = TOP_POINT
    radius = math.sqrt((tx - cx)**2 + (ty - cy)**2)
    start_angle = math.atan2(ty - cy, tx - cx)
    
    points = []
    for i in range(num_letters):
        angle = start_angle + i * (2 * math.pi / num_letters)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append({'x': int(x), 'y': int(y)})
    return points

# ==========================================
# 4. OCR ENGINE
# ==========================================
def detect_letters_string(d, reader):
    print("   [OCR] Scanning wheel (Fixing N/V & Sorting)...")
    img = d.screenshot(format='opencv')
    if img is None: return ""
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    mask = np.zeros_like(binary)
    cv2.circle(mask, CENTER, int(RADIUS * 1.5), 255, -1)
    masked_img = cv2.bitwise_and(binary, binary, mask=mask)

    contours, _ = cv2.findContours(masked_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    letter_blobs = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 500 < area < 18000:
            M = cv2.moments(cnt)
            if M["m00"] == 0: continue
            
            cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            dist_from_center = math.sqrt((cx - CENTER[0])**2 + (cy - CENTER[1])**2)
            
            if not (RADIUS * 0.7 < dist_from_center < RADIUS * 1.4):
                continue
            
            # Angle Calculation
            angle = math.degrees(math.atan2(cy - CENTER[1], cx - CENTER[0]))
            normalized_angle = (angle + 115) % 360 
            
            x, y, w, h = cv2.boundingRect(cnt)
            letter_blobs.append({
                'x': x, 'y': y, 'w': w, 'h': h,
                'angle': normalized_angle,
                'is_likely_I': (float(h) / w) > 2.2
            })

    if not letter_blobs:
        print("   [OCR] No letters found.")
        time.sleep(1.5)
        return "???" 

    letter_blobs.sort(key=lambda k: k['angle'])
    
    full_text_str = ""
    for blob in letter_blobs:
        if blob['is_likely_I']:
            full_text_str += "I"
            continue

        pad = 20 # More padding for better context
        y1, y2 = max(0, blob['y']-pad), min(img.shape[0], blob['y']+blob['h']+pad)
        x1, x2 = max(0, blob['x']-pad), min(img.shape[1], blob['x']+blob['w']+pad)
        
        crop = gray[y1:y2, x1:x2]
        crop_zoom = cv2.resize(crop, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
        
        # --- FIX N vs V: Morphological Closing ---
        # This fills in the gaps in the letter N so it doesn't look like a V
        _, th = cv2.threshold(crop_zoom, 145, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel) 

        result = reader.readtext(th, allowlist=OCR_ALLOWLIST, detail=0)
        full_text_str += result[0].upper() if result else "N" # Default to N if unsure

    print(f"   [OCR Result] {full_text_str}")
    return full_text_str
# ==========================================
# 5. MERGED SOLVERS
# ==========================================
def fetch_wordraiders(letters_str):
    """Source 1: WordRaiders.com (From Script A)"""
    words_found = set()
    payload = {
        'letters': letters_str,
        'words_tool': 'unscramble', 'dictionary': 'all', 'word_set': 'all',
        'word_set_origin': 'user', 'sort_order': 'A_Z', 'search_mode': 'scrabble',
        'match_type': 'any', 'group': 'on'
    }
    try:
        r = session.post(URL_RAIDERS, data=payload, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Base words
        for li in soup.select('li.single-word'):
            if li.find('sub'): li.find('sub').decompose()
            words_found.add(li.get_text().strip().upper())

        # Handle "Show More" buttons
        show_more_btns = soup.select('button.show-more.cta-btn')
        for btn in show_more_btns:
            target_len = btn.get('data-length')
            # Only fetch if counts look truncated (simple check)
            parent = btn.find_parent('div', class_='scrabble-btn-outer')
            needs_fetch = True
            if parent:
                count_div = parent.select_one('.showing-count')
                if count_div:
                    nums = [int(s) for s in re.findall(r'\b\d+\b', count_div.get_text())]
                    if len(nums) >= 2 and nums[0] >= nums[1]: needs_fetch = False
            
            if needs_fetch and target_len:
                p_len = payload.copy()
                p_len['length'] = target_len
                r_len = session.post(URL_RAIDERS, data=p_len, timeout=5)
                soup_len = BeautifulSoup(r_len.text, 'html.parser')
                for li in soup_len.select('li.single-word'):
                    if li.find('sub'): li.find('sub').decompose()
                    words_found.add(li.get_text().strip().upper())
                    
    except Exception as e:
        print(f"   [Raiders Error] {e}")
    
    return words_found

def fetch_wordcollect(letters_str):
    """Source 2: WordCollectAnswers.com (From Script B)"""
    words_found = set()
    try:
        url = URL_COLLECT.format(letters_str)
        r = session.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        wc = soup.find('div', class_='words')
        if wc:
            for div in wc.find_all('div', recursive=False):
                w = div.get_text()
                clean = ''.join(filter(str.isalpha, w)).upper()
                if len(clean) >= 3: 
                    words_found.add(clean)
    except Exception as e:
        print(f"   [Collect Error] {e}")
    
    return words_found

def solve_merged(letters_str):
    if "?" in letters_str or len(letters_str) < 3: return []
    print(f"   [Solver] Requesting: {letters_str} from both sources...")

    # 1. Fetch from both
    set_a = fetch_wordraiders(letters_str)
    set_b = fetch_wordcollect(letters_str)

    # 2. Merge
    combined_set = set_a.union(set_b)
    print(f"   [Solver] Raw counts -> Raiders: {len(set_a)}, Collect: {len(set_b)}, Total: {len(combined_set)}")

    # 3. Validation (Ensure words can actually be formed by letters)
    source_count = Counter(letters_str)
    validated_list = []
    
    for word in combined_set:
        if len(word) < 3: continue
        word_count = Counter(word)
        # Check if we have enough letters
        if all(source_count[c] >= word_count[c] for c in word_count):
            validated_list.append(word)

    # 4. Sort (Longest first)
    validated_list.sort(key=len, reverse=True)
    
    print(f"   [Solver] Valid words to swipe: {len(validated_list)}")
    return validated_list

# ==========================================
# 6. SWIPER (STRICT CHECK)
# ==========================================
def swipe_words_custom(d, words, chars, coords):
    print(f"   [Action] Swiping {len(words)} words...")
    pt_list = [(p['x'], p['y']) for p in coords]
    
    for word in words:
        if keyboard.is_pressed('r'): return 
        if keyboard.is_pressed('q'): exit()
        
        # Removed the 'get_game_state' check from here to prevent premature stopping

        indices = []
        used = set()
        valid_word = True
        
        for char in word:
            found_idx = -1
            for i, c in enumerate(chars):
                if c == char and i not in used:
                    found_idx = i
                    break
            if found_idx != -1:
                indices.append(found_idx)
                used.add(found_idx)
            else:
                valid_word = False
                break
        
        if valid_word:
            path = [pt_list[indices[0]]]
            for i in range(len(indices)-1):
                curr, next_i = indices[i], indices[i+1]
                diff = abs(curr - next_i)
                is_neighbor = (diff == 1) or (diff == len(chars) - 1)
                
                if is_neighbor:
                    path.append(pt_list[next_i]) 
                else:
                    mx = (pt_list[curr][0] + pt_list[next_i][0]) / 2
                    my = (pt_list[curr][1] + pt_list[next_i][1]) / 2
                    wx = mx + (CENTER[0] - mx) * 0.6 
                    wy = my + (CENTER[1] - my) * 0.6
                    path.append((int(wx), int(wy)))
                    path.append(pt_list[next_i])
            
            try: d.swipe_points(path, 0.080)
            except: pass
            time.sleep(0.45)
    
    # NEW: Click skip button area after all words are swiped
    print(f"   [Action] All words attempted. Clicking Skip/Next area.")
    d.click(SKIP_BTN_AREA[0], SKIP_BTN_AREA[1])
# ==========================================
# 7. MAIN LOOP (Optimized)
# ==========================================
if __name__ == "__main__":
    d = u2.connect()
    print("Loading OCR Model (GPU)...")
    reader = easyocr.Reader(['en'], gpu=True)
    print(f"Ready. Press 'q' to quit.")

    while True:
        if keyboard.is_pressed('q'): break

        state = get_game_state(d)
        
        if state == 'LEVEL_END':
            print("   [State] Level Complete. Clicking Next...", end='\r')
            d.click(NEXT_BTN_AREA[0], NEXT_BTN_AREA[1])
            time.sleep(1.2)
            continue
            
        elif state == 'PLAYING':
            print("\n   [State] PLAYING! Scanning board...")
            letters_str = detect_letters_string(d, reader)
            
            # --- ERROR CORRECTIONS ---
            if any(x in letters_str for x in ["LEVEL", "NEXT", "TEXT"]):
                d.click(NEXT_BTN_AREA[0], NEXT_BTN_AREA[1])
                time.sleep(1.0)
                continue

            valid_letters = letters_str.replace("?", "")
            
            if len(valid_letters) > 9:
                d.click(SKIP_BTN_AREA[0], SKIP_BTN_AREA[1])
                time.sleep(2.0)
                continue

            if len(valid_letters) < 3:
                d.click(NEXT_BTN_AREA[0], NEXT_BTN_AREA[1])
                time.sleep(1.0)
                continue
            
            # --- SOLVE & SWIPE ---
            perfect_coords = get_perfect_coords(len(letters_str))
            answers = solve_merged(letters_str)
            
            if answers:
                swipe_words_custom(d, answers, list(letters_str), perfect_coords)
                time.sleep(0.5)
            else:
                print("   [Error] No words found. Skipping level.")
                d.click(SKIP_BTN_AREA[0], SKIP_BTN_AREA[1])
                time.sleep(1)