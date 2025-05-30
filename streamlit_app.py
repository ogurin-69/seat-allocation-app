import streamlit as st
import random
import pandas as pd

# 人数と席設定
TOTAL_PEOPLE = 68
SEATS = {
    "A": 6, "B": 6, "C": 6, "D": 6,
    "E": 6, "F": 6, "G": 6, "H": 6,
    "I": 5, "J": 5, "K": 5, "L": 5
}

# 初期化関数
def initialize_state():
    st.session_state.people = [f"Person {i}" for i in range(1, TOTAL_PEOPLE + 1)]
    st.session_state.seat_limits = SEATS.copy()
    st.session_state.assignments = {seat: [] for seat in SEATS.keys()}

# 初回のみ初期化
if 'initialized' not in st.session_state:
    initialize_state()
    st.session_state.initialized = True

# リセット処理
if st.button("🔄 リセット"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# 割り当て処理
def assign_next_person():
    if len(st.session_state.people) == 0:
        st.warning("もう割り当てる人がいません。")
        return
    next_person = random.choice(st.session_state.people)
    available_seats = [
        seat for seat, limit in st.session_state.seat_limits.items()
        if len(st.session_state.assignments[seat]) < limit
    ]
    if not available_seats:
        st.warning("割り当て可能な席がありません。")
        return
    chosen_seat = random.choice(available_seats)
    st.session_state.assignments[chosen_seat].append(next_person)
    st.session_state.people.remove(next_person)
    st.success(f"🎉 {next_person} さんを席 {chosen_seat} に割り当てました！")

# タイトル
st.title("🎲 席割りランダムくじ引きアプリ")

# 割り当てボタン
if len(st.session_state.people) > 0:
    if st.button("🎡 次の人を割り振る"):
        assign_next_person()
else:
    st.balloons()
    st.success("🎉 全員の割り当てが完了しました！")

# 残り人数表示
assigned_count = sum(len(lst) for lst in st.session_state.assignments.values())
remaining = TOTAL_PEOPLE - assigned_count
st.info(f"🎯 残り割り当て人数：{remaining}人")

# 表形式の割り当て状況表示（横スクロール対応）
max_len = max(len(lst) for lst in st.session_state.assignments.values())
table_dict = {}
for seat, assigned_list in st.session_state.assignments.items():
    padded_list = assigned_list + [""] * (max_len - len(assigned_list))
    table_dict[seat] = padded_list

df = pd.DataFrame(table_dict)
st.subheader("📋 現在の割り当て状況（表形式）")
st.dataframe(df, use_container_width=True)
