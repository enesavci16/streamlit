import streamlit as st

import psycopg2

import pandas as pd
import json

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
# Database connection parameters
db_params = {
    "database": "postgres",
    "user": "airflow",
    "password": "airflow",
    "host": "localhost",
    "port": "5433"
}

# Create a connection to the database
conn = psycopg2.connect(**db_params)

# Create a cursor object
cur = conn.cursor()

# Example SQL query
query = "SELECT * FROM dag_run"
cur.execute(query)

#**************
data = cur.fetchall()
df = pd.DataFrame(data, columns=[desc[0] for desc in cur.description])



# Convert the JSON strings to separate columns
additional_data_dict = df['x'].apply(lambda x: json.loads(x.replace("'", "\""))).apply(pd.Series)

# Display the resulting DataFrame

# print(additional_data_dict)

# additional_data_dict = pd.DataFrame(df["x"])


# # Convert the JSON strings to separate columns
# df = df['x'].apply(lambda x: json.loads(x.replace("'", "\""))).apply(pd.Series)

# # Display the resulting DataFrame
# additional_data_df = pd.DataFrame(additional_data_dict)

print(df)
# df = df.drop(["x","dt"], axis=1)
df=df.drop(["x"],axis=1)

df=df.drop(["dt"],axis=1)
concatenated_df = pd.concat([ additional_data_dict , df], axis=1)

# combined_df = pd.concat([df, additional_data_dict], join="inner", ignore_index=True)





# # combined_df = pd.concat([df, additional_data_df], ignore_index=True)

# # df = pd.DataFrame(data, columns=[desc[0] for desc in cur.description])

df=concatenated_df.copy()
# df['dt'] = pd.to_datetime(df['dt'])  # Convert 'dt' column to datetime
# df['x'] = df['x'].astype(str)  # Convert 'x' column to string
df['y'] = df['y'].astype(float)  # Convert 'y' column to integer

# # print(df.info())
df['pred'] = df['pred'].str.strip('[]').astype(float)
df.info()



# Streamlit app
st.title("Line Plot of 'y' and 'pred'")

# Create a line plot using Plotly with different colors for 'y' and 'pred'
fig = go.Figure()

# Add 'y' line
fig.add_trace(go.Scatter(x=df.index, y=df['y'], mode='lines', name='y', line=dict(color='blue')))

# Add 'pred' line
fig.add_trace(go.Scatter(x=df.index, y=df['pred'], mode='lines', name='pred', line=dict(color='red')))

fig.update_layout(title='Line Plot of "y" and "pred')
fig.update_xaxes(title='Index')
fig.update_yaxes(title='Value')

# Show the plot in Streamlit
st.plotly_chart(fig)


# Display the DataFrame using Streamlit

st.dataframe(df)
last_row = df.iloc[-1]
st.dataframe(last_row)

# Close the cursor and connection
cur.close()
conn.close()


#********************


# Fetch and display the results
# results = cur.fetchall()
# for row in results:
#     st.write(row)

# # Close the cursor and connection
# cur.close()
# conn.close()
