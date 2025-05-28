import streamlit as st
import random

# 定数・初期値
TOTAL_PEOPLE = 68
SEATS = {
    "A": 7, "B":7, "C":7, "D":7, "E":7,
    "F":6, "G":7, "H":6, "I":7, "J":7
}

# 初期の参加者リスト（例：名前を1〜68までの数字で作成）
if "people" not in st.session_state:
    st.session_state.people = [f"Person {i}" for i in range(1, TOTAL_PEOPLE + 1)]

# 割り当て可能な席の枠数
if "seat_limits" not in st.session_state:
    st.session_state.seat_limits = SEATS.copy()

# 割り当て済みの辞書（席: 割り当てられた名前リスト）
if "assignments" not in st.session_state:
    st.session_state.assignments = {k: [] for k in st.session_state.seat_limits.keys()}

# リセットフラグ（ボタン押されたときに初期化用）
if "reset_done" not in st.session_state:
    st.session_state.reset_done = False

st.title("🎲 席割りくじ引きアプリ")

# リセットボタン処理
if st.button("🔄 リセット"):
    st.session_state.people = [f"Person {i}" for i in range(1, TOTAL_PEOPLE + 1)]
    st.session_state.seat_limits = SEATS.copy()
    st.session_state.assignments = {k: [] for k in SEATS.keys()}
    st.session_state.reset_done = True

if st.session_state.reset_done:
    st.success("✅ リセットしました！")
    st.session_state.reset_done = False

# 残り人数計算
assigned_count = sum(len(v) for v in st.session_state.assignments.values())
remaining = TOTAL_PEOPLE - assigned_count
st.info(f"🎯 残り割り当て人数：{remaining}人")

# くじ引きボタン（1人ずつ割り当て）
if remaining > 0:
    if st.button("🎡 次の人を割り振る"):
        # 残ってる参加者からランダムに1人選ぶ
        next_person = random.choice(st.session_state.people)

        # 割り当て可能な席のリスト（残り枠がある席のみ）
        available_seats = [
            seat for seat, limit in st.session_state.seat_limits.items()
            if len(st.session_state.assignments[seat]) < limit
        ]

        if not available_seats:
            st.warning("⚠️ 割り当て可能な席がありません！")
        else:
            # ランダムに席を1つ選ぶ
            chosen_seat = random.choice(available_seats)
            # 割り当てリストに追加
            st.session_state.assignments[chosen_seat].append(next_person)
            # 割り当てた人を未割り当てリストから削除
            st.session_state.people.remove(next_person)
            st.success(f"✨ {next_person} さんを席 {chosen_seat} に割り当てました！")

else:
    st.balloons()
    st.success("🎉 全員割り当て完了しました！")

# 割り当て状況を席ごとに表示
st.subheader("📋 現在の割り当て状況")
for seat, assigned_list in st.session_state.assignments.items():
    st.markdown(f"**席 {seat} （定員{st.session_state.seat_limits[seat]}人）**")
    if assigned_list:
        for p in assigned_list:
            st.write(f"- {p}")
    else:
        st.write("（未割り当て）")
