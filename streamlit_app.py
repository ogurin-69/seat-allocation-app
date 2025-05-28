import streamlit as st
import random
import pandas as pd

TOTAL_PEOPLE = 68
SEATS = {
    "A": 7, "B":7, "C":7, "D":7, "E":7,
    "F":6, "G":7, "H":6, "I":7, "J":7
}

def initialize_state():
    st.session_state.people = [f"Person {i}" for i in range(1, TOTAL_PEOPLE + 1)]
    st.session_state.seat_limits = SEATS.copy()
    st.session_state.assignments = {seat: [] for seat in SEATS.keys()}

# 初期化処理（初回起動またはリセット後）
if 'initialized' not in st.session_state:
    initialize_state()
    st.session_state.initialized = True

# リセットボタンの処理
if st.button("🔄 リセット"):
    # セッション状態を初期化しつつ初期化済みフラグを消す
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

def assign_next_person():
    if len(st.session_state.people) == 0:
        st.warning("もう割り当てる人がいません。")
        return
    next_person = random.choice(st.session_state.people)
    available_seats = [seat for seat, limit in st.session_state.seat_limits.items()
                       if len(st.session_state.assignments[seat]) < limit]
    if not available_seats:
        st.warning("割り当て可能な席がありません。")
        return
    chosen_seat = random.choice(available_seats)
    st.session_state.assignments[chosen_seat].append(next_person)
    st.session_state.people.remove(next_person)
    st.success(f"🎉 {next_person} さんを席 {chosen_seat} に割り当てました！")

st.title("🎲 席割りランダムくじ引きアプリ")

if len(st.session_state.people) > 0:
    if st.button("🎡 次の人を割り振る"):
        assign_next_person()
else:
    st.balloons()
    st.success("🎉 全員の割り当てが完了しました！")

assigned_count = sum(len(lst) for lst in st.session_state.assignments.values())
remaining = TOTAL_PEOPLE - assigned_count
st.info(f"🎯 残り割り当て人数：{remaining}人")

max_len = max(len(lst) for lst in st.session_state.assignments.values())
table_dict = {}
for seat, assigned_list in st.session_state.assignments.items():
    padded_list = assigned_list + [""] * (max_len - len(assigned_list))
    table_dict[seat] = padded_list

df = pd.DataFrame(table_dict)
st.subheader("📋 現在の割り当て状況（表形式）")
st.table(df)
