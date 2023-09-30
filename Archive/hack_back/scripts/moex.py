import plotly.express as px
import pandas

qdata_0 = pandas.read_csv(f"./data/other/df_moex")

fig = px.line(
    qdata_0, x="quarter", y="VALUE", title="Индекс мосбиржи", width=600, height=300
)

fig.update_traces(line_color="#2196f3")
fig.update_layout(
    xaxis=dict(
        showgrid=False,
    ),
    yaxis=dict(showgrid=False),
    plot_bgcolor="white",
)
print(fig.to_json())
