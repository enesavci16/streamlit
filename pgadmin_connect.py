import streamlit as st

import psycopg2

import pandas as pd

# streamlit_app.py



# Initialize connection.
conn = st.connection("postgresql", type="sql")

# # Perform query.
# df = conn.query('SELECT * FROM dag_run limit 20;',)

# # Print results.
# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")

# # ttl="10m"

# data=pd.DataFrame(row)
# st.table(data)