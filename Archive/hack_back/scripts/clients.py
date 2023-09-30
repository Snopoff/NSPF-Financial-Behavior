import plotly.express as px
import pandas
import sys

num = sys.argv[1]

qdata_0 = pandas.read_csv(f"./data/clients/number_of_clients_in_{num}.csv")

fig = px.line(qdata_0, x="quarter", y="clnt_id", title="Число клиентов")
fig.update_traces(line_color="#2196f3")
fig.update_layout(
    xaxis=dict(
        showgrid=False,
    ),
    yaxis=dict(showgrid=False),
    plot_bgcolor="white",
)
print(fig.to_json())
