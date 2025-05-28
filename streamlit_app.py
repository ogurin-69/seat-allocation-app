import streamlit as st
import random
import pandas as pd

# 初期設定・状態保持
if 'people' not in st.session_state:
    # 参加者名（実名に変えてください）
    st.session_state.people = [f"Person {i+1}" for i in range(68)]
    random.shuffle(st.session_state.people)
    
if 'seat_limits' not in st.session_state:
    st.session_state.seat_limits = {
        'A': 7, 'B': 7, 'C': 7, 'D': 7, 'E': 7,
        'F': 6, 'G': 7, 'H': 6, 'I': 7, 'J': 7
    }

if 'seat_pool' not in st.session_state:
    seat_pool = []
    for seat, limit in st.session_state.seat_limits.items():
        seat_pool += [seat] * limit
    random.shuffle(seat_pool)
    st.session_state.seat_pool = seat_pool

if 'assignments' not in st.session_state:
    st.session_state.assignments = []

# タイトル
st.title("🎲 席割りルーレットアプリ")

st.write(f"残り割り当て人数：{len(st.session_state.people)}人")

# 「次の人を割り当て」ボタン
if st.button("🎯 次の人を割り当て"):
    if st.session_state.people and st.session_state.seat_pool:
        name = st.session_state.people.pop(0)
        seat = random.choice(st.session_state.seat_pool)
        st.session_state.seat_pool.remove(seat)
        st.session_state.assignments.append((name, seat))
        st.success(f"{name} さん → {seat} 席に決定！")
    else:
        st.warning("⚠️ 全員の割り当てが完了しました！")

# 割り当て表を席ごとに表示
seat_dict = {}
for name, seat in st.session_state.assignments:
    seat_dict.setdefault(seat, []).append(name)

# 最大人数に合わせて空白埋め
max_len = max(len(v) for v in seat_dict.values()) if seat_dict else 0
data = {
    seat: seat_dict.get(seat, []) + [""] * (max_len - len(seat_dict.get(seat, [])))
    for seat in sorted(st.session_state.seat_limits.keys())
}

df = pd.DataFrame(data)

st.write("## 割り当て一覧")
st.table(df)

import streamlit as st

# 任意：セッションに初期値を入れておく処理（必要に応じて編集）
if 'people' not in st.session_state:
    st.session_state.people = ["Alice", "Bob", "Charlie", "David"]
if 'seat_limits' not in st.session_state:
    st.session_state.seat_limits = {'A': 7, 'B': 7, 'C': 7}
if 'assignments' not in st.session_state:
    st.session_state.assignments = {'A': [], 'B': [], 'C': []}
if 'reset_triggered' not in st.session_state:
    st.session_state.reset_triggered = False

# 🔄 リセットボタン（クリック時、トリガーだけONに）
if st.button("🔄 リセット"):
    st.session_state.reset_triggered = True

# 実際のリセット処理（次回描画時に安全に実行）
if st.session_state.reset_triggered:
    for key in ['people', 'seat_limits', 'seat_pool', 'assignments']:
        st.session_state.pop(key, None)
    st.session_state.reset_triggered = False
    st.experimental_rerun()
