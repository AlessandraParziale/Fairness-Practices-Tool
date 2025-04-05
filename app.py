from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

def load_and_label_data(filename, label):
    df = pd.read_csv(filename, sep=';')
    df['source'] = label
    return df

df_classification = pd.read_csv('Classification.csv')
df_clustering = pd.read_csv('Clustering.csv')
df_regression = pd.read_csv('Regression.csv')

df_classification['source'] = 'Classification'
df_clustering['source'] = 'Clustering'
df_regression['source'] = 'Regression'

df = pd.concat([df_classification, df_clustering, df_regression], ignore_index=True)

dataset_names = {
    "Communities and Crime": "Crime",
    "German Credit": "Finance",
    "Bank Marketing": "Marketing",
    "Adult": "Economics",
    "Compas": "Recidivism Prediction"
}


df["dataset"] = df["dataset"].replace(dataset_names)
contexts = df[['dataset']].dropna().drop_duplicates()
contexts = [f"{row['dataset']}" for _, row in contexts.iterrows()]


def get_attributes_and_tasks_for_context(context):
    filtered_df = df[df['dataset'] == context]
    attributes = filtered_df['attribute'].dropna().unique().tolist()
    tasks = filtered_df['task'].dropna().unique().tolist()
    return attributes, tasks


@app.route('/')
def index():
    return render_template('index.html', contexts=contexts)


@app.route('/get_attributes_and_tasks', methods=['POST'])
def get_attributes_and_tasks():
    data = request.json
    if 'context' not in data:
        return jsonify({'error': 'Missing context'}), 400

    selected_context = data['context']
    attributes, tasks = get_attributes_and_tasks_for_context(selected_context)

    return jsonify({'attributes': attributes, 'tasks': tasks})


@app.route('/update_practices', methods=['POST'])
def update_practices():
    selected_context = request.form.get('context')
    selected_source = request.form.get('source')
    selected_attribute = request.form.get('attribute')
    selected_task = request.form.get('task')

    if not selected_context or not selected_attribute or not selected_task:
        return jsonify({'error': 'Missing required fields'}), 400

    filtered_df = df[
        (df['dataset'] == selected_context) &
        (df['attribute'] == selected_attribute) &
        (df['task'] == selected_task)
    ]

    if selected_source:
        filtered_df = filtered_df[filtered_df['source'] == selected_source]

    filtered_df = filtered_df[(filtered_df['costEffectiveness'] >= -1) & (filtered_df['costEffectiveness'] <= 1)]
    sorted_df = filtered_df.sort_values(by='costEffectiveness', key=lambda x: abs(x))
    best_practices = sorted_df.head(5)

    performance_metrics = {
        "clustering": ["silohouette"],
        "classification": ["Precision", "Recall", "Accuracy", "F1"],
        "regression": ["MSE", "MAD"]
    }

    fairness_metrics = {
        "clustering": ["ae", "me", "aw", "mw"],
        "classification": ["AAOD", "FDRD", "DI"],
        "regression": ["independence", "separation", "sufficiency"]
    }

    normalized_task = selected_task.split()[0].lower()

    selected_practices = []
    for _, row in best_practices.iterrows():
        practice_data = {
            'title': row['practice'],
            'metrics': {
                'costEffectiveness': row['costEffectiveness'],
                'performance': {metric: (row[metric] if not pd.isna(row[metric]) else None)
                                for metric in performance_metrics.get(normalized_task, [])},
                'fairness': {metric: (row[metric] if not pd.isna(row[metric]) else None)
                             for metric in fairness_metrics.get(normalized_task, [])}
            }
        }
        selected_practices.append(practice_data)

    return render_template('practices.html',
                           selected_practices=selected_practices,
                           selected_context=selected_context,
                           selected_source=selected_source,
                           selected_attribute=selected_attribute,
                           selected_task=selected_task)




@app.route('/get_practices_graph', methods=['POST'])
def get_practices_graph():
    data = request.json
    if 'context' not in data or 'attribute' not in data or 'task' not in data:
        return jsonify({'error': 'Missing context, attribute, or task'}), 400

    selected_context = data['context']
    selected_attribute = data['attribute']
    selected_task = data['task']

    filtered_df = df[
        (df['dataset'] == selected_context) &
        (df['attribute'] == selected_attribute) &
        (df['task'] == selected_task)
    ]

    nodes = [{'id': selected_context, 'label': selected_context, 'color': '#d4aaff'}]
    edges = []

    for _, row in filtered_df.iterrows():
        practice = row['practice']
        cost_effectiveness = row['costEffectiveness']

        # Determina il colore in base a costEffectiveness
        if -1 <= cost_effectiveness <= 1:
            node_color = '#AAEAAA'
        else:
            node_color = '#d4aaff'

        if practice not in [node['id'] for node in nodes]:
            nodes.append({'id': practice, 'label': practice, 'color': node_color})
        edges.append({'from': selected_context, 'to': practice})

    return jsonify({'nodes': nodes, 'edges': edges})

if __name__ == '__main__':
    app.run(debug=True)
