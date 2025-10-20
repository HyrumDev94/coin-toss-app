import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Coin Toss App", page_icon="🪙", layout="centered")

st.title("🪙 Coin Toss Simulation")
st.write("Simulate repeated coin tosses and watch the probability stabilize around 50%.")

# Controls
cols = st.columns(3)
with cols[0]:
    n_flips = st.slider("Number of flips", min_value=10, max_value=5000, value=200, step=10)
with cols[1]:
    seed = st.number_input("Random seed (optional)", min_value=0, value=0)
with cols[2]:
    run = st.button("Run Simulation")

# Run simulation
if run:
    rng = np.random.default_rng(seed if seed else None)
    flips = rng.integers(0, 2, size=n_flips)  # 1=heads, 0=tails
    heads_cum = np.cumsum(flips)
    tails_cum = np.arange(1, n_flips + 1) - heads_cum
    prop_heads = heads_cum / np.arange(1, n_flips + 1)

    df = pd.DataFrame({
        "Flip": np.arange(1, n_flips + 1),
        "Heads (cumulative)": heads_cum,
        "Tails (cumulative)": tails_cum,
        "Proportion Heads": prop_heads
    })

    # Summary
    h, t = int(heads_cum[-1]), int(tails_cum[-1])
    st.subheader("Results")
    st.write(f"**Heads:** {h}  |  **Tails:** {t}  |  **Proportion Heads:** {prop_heads[-1]:.3f}")

    # Bar chart of final counts
    bar_df = pd.DataFrame({"Outcome": ["Heads", "Tails"], "Count": [h, t]})
    bar = alt.Chart(bar_df).mark_bar().encode(
        x=alt.X("Outcome:N", title=None),
        y=alt.Y("Count:Q", title="Count"),
        tooltip=["Outcome", "Count"]
    ).properties(height=240)
    st.altair_chart(bar, use_container_width=True)

    # Line chart of running proportion
    line = alt.Chart(df).mark_line().encode(
        x=alt.X("Flip:Q"),
        y=alt.Y("Proportion Heads:Q", scale=alt.Scale(domain=[0, 1])),
        tooltip=["Flip", alt.Tooltip("Proportion Heads:Q", format=".3f")]
    ).properties(height=280, title="Running Proportion of Heads")
    st.altair_chart(line, use_container_width=True)

else:
    st.info("Set the number of flips and click **Run Simulation** to start.")
