import plotly.express as px
import pandas
import sys

results = pandas.read_csv(f"./data/incomes/incomes_predictions.csv")

num = sys.argv[1]

fig = px.line(
    results, x="quarter", y=f"prediction_S{num}", title="Предсказанные доходы"
)

fig.update_traces(line_color="#f50057")
fig.update_layout(
    xaxis=dict(
        showgrid=False,
    ),
    yaxis=dict(showgrid=False),
    plot_bgcolor="white",
)
print(fig.to_json())
