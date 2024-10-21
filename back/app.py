import streamlit as st
import numpy as np
import pandas as pd

st.title("Roadtrip Inspiration")
st.write("Planning a roadtrip for your camper van has never been easier.")


map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)
with st.form:
