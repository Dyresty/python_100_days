import uiautomator2 as u2
import requests
from bs4 import BeautifulSoup
import time
import math
import cv2
import numpy as np
import os

# ==========================================
# 1. CONFIGURATION
# ==========================================
CENTER = (545, 1753)
TOP_POINT = (545, 1521)
SEARCH_URL = "https://wordcollectanswers.com/en/?letters={}"

# ==========================================
# 2. GEOMETRY ENGINE
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
# 3. ROBUST DETECTOR
# ==========================================
def is_wheel_visible(d):
    """
    Returns True if 3+ letters are visible.
    Saves 'debug_view.png' to help you see what the bot sees.
    """
    img = d.screenshot(format='opencv')
    
    # 1. PRE-PROCESS
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # LOWER THRESHOLD: 150 (was 180). Catches dimmer letters.
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    radius = math.sqrt((TOP_POINT[0]-CENTER[0])**2 + (TOP_POINT[1]-CENTER[1])**2)
    hit_angles = []

    # 2. SCAN
    for deg in range(0, 360, 4):
        rad = math.radians(deg)
        px = int(CENTER[0] + radius * math.cos(rad))
        py = int(CENTER[1] + radius * math.sin(rad))
        
        # WIDER CHECK BOX (15px instead of 10px)
        y1, y2 = max(0, py-15), min(img.shape[0], py+15)
        x1, x2 = max(0, px-15), min(img.shape[1], px+15)
        roi = binary[y1:y2, x1:x2]
        
        # Lower requirement for "white pixels" (20 instead of 30)
        if cv2.countNonZero(roi) > 20: 
            hit_angles.append(deg)

    # 3. DEBUG VISUALIZATION
    # Draw green dots where it sees letters
    debug_img = img.copy()
    for deg in hit_angles:
        rad = math.radians(deg)
        px = int(CENTER[0] + radius * math.cos(rad))
        py = int(CENTER[1] + radius * math.sin(rad))
        cv2.circle(debug_img, (px, py), 5, (0, 255, 0), -1)
    
    # Save this! If the bot gets stuck, open this image to see why.
    cv2.imwrite("debug_view.png", debug_img)

    # 4. DECISION
    if not hit_angles: return False
    
    clusters = 1
    for i in range(1, len(hit_angles)):
        if hit_angles[i] - hit_angles[i-1] >= 15:
            clusters += 1
            
    # If we see at least 3 distinct blobs, the wheel is there.
    return 3 <= clusters <= 8

# ==========================================
# 4. SOLVER
# ==========================================
def solve_online(letters_str):
    if len(letters_str) < 3: return []
    url = SEARCH_URL.format(letters_str)
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, 'html.parser')
        answers = []
        wc = soup.find('div', class_='words')
        if wc:
            for div in wc.find_all('div', recursive=False):
                w = div.get_text()
                clean = ''.join(filter(str.isalpha, w)).upper()
                if len(clean) >= 3: answers.append(clean)
        
        final_list = []
        from collections import Counter
        source_count = Counter(letters_str)
        for word in answers:
            word_count = Counter(word)
            if all(source_count[c] >= word_count[c] for c in word_count):
                final_list.append(word)
        return sorted(list(set(final_list)), key=len, reverse=True)
    except: return []

def swipe_words(d, words, chars, coords):
    print(f"   [Bot] Swiping {len(words)} words...")
    time.sleep(0.5)
    pt_list = [(p['x'], p['y']) for p in coords]
    
    for word in words:
        indices = []
        used = set()
        valid = True
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
                valid = False
                break
        
        if valid:
            path = [pt_list[indices[0]]]
            for i in range(len(indices)-1):
                curr, next_i = indices[i], indices[i+1]
                diff = abs(curr - next_i)
                is_neighbor = (diff == 1) or (diff == len(chars) - 1)
                
                if is_neighbor:
                    path.append(pt_list[next_i])
                else:
                    mx, my = (pt_list[curr][0]+pt_list[next_i][0])/2, (pt_list[curr][1]+pt_list[next_i][1])/2
                    wx = mx + (CENTER[0]-mx)*0.6 
                    wy = my + (CENTER[1]-my)*0.6
                    path.append((int(wx), int(wy)))
                    path.append(pt_list[next_i])
            
            d.swipe_points(path, 0.060) 
            time.sleep(0.27)

# ==========================================
# 5. MAIN LOOP (With Force Mode)
# ==========================================
if __name__ == "__main__":
    d = u2.connect()
    print(f"Connected to: {d.info.get('marketingName')}")
    print("Script Started. Check 'debug_view.png' if it gets stuck.")

    miss_counter = 0

    while True:
        # 1. CHECK VISIBILITY
        wheel_exists = is_wheel_visible(d)
        
        # 2. AUTO-NEXT LOGIC (With Fail-Safe)
        if not wheel_exists:
            miss_counter += 1
            print(f"   [State] No wheel ({miss_counter}/5). Clicking Center...", end='\r')
            
            # Click Center to skip "Level Complete" screens
            d.click(CENTER[0], CENTER[1])
            time.sleep(1.5) 
            
            # FAIL-SAFE: If we missed 5 times, Force the prompt
            if miss_counter >= 5:
                print("\n   [Warning] Detection failing? FORCING PROMPT.")
                miss_counter = 0 # Reset
                # Don't 'continue', just fall through to the input prompt below
            else:
                continue # Keep clicking center if under limit
        else:
            # We see the wheel! Reset counter
            miss_counter = 0

        # 3. PROMPT
        print("\n" + "="*30)
        user_in = input(">> ENTER LETTERS: ").strip().upper()
        
        if not user_in:
            print("   Skipped.")
            continue
            
        # 4. GENERATE & SOLVE
        num_letters = len(user_in)
        perfect_coords = get_perfect_coords(num_letters)
        chars_list = list(user_in)
        
        answers = solve_online(user_in)
        
        if answers:
            print(f"   [Solver] Found {len(answers)} words.")
            swipe_words(d, answers, chars_list, perfect_coords)
            print("   [Done] Level finished.")
            time.sleep(3) 
        else:
            print("   [Error] No answers found. Check spelling.")