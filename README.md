# Fairness-Aware Practices Recommender

This web-based tool suggests **fairness-aware practices** based on the dataset, context, attribute, and task selected by the user. It leverages a knowledge base computed through 5940 experiments to return the top practices that balance **performance** and **fairness** based on your specific use case.

## Features

- Simple web interface to select context, attribute, and task.
- Returns the best fairness-aware data preparation practices ranked by cost-effectiveness.
- Visualizes the relationship between practices and contexts.
- Supports classification, regression, and clustering tasks.

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/fairness-practices-tool.git
cd fairness-practices-tool
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the required packages
```bash 
pip install flask pandas
```

##  Run the App
```bash
python app.py
```

The tool will be available at http://127.0.0.1:5000/

This tool helps you identify fairness-aware data preparation practices that best suit your context, attribute, and task. It uses a dataset of practices and ranks them based on cost-effectiveness and relevant performance/fairness metrics.

### 1. Select a Context
- On the homepage, you’ll see a dropdown menu of available **contexts** (e.g., *Finance*, *Economics*, *Marketing*, etc.).
- These are derived from well-known datasets like *German Credit*, *Adult*, *Bank Marketing*, etc.

### 2. Retrieve Attributes and Tasks
- Once a context is selected, the app automatically fetches and displays:
  - **Attributes**: sensitive or relevant features (e.g., *age*, *gender*)
  - **Tasks**: the type of machine learning problem (e.g., *classification*, *regression*, *clustering*)

### 3. Submit Your Selection
- Choose an **attribute** and **task** to analyze.

### 4. View Suggested Practices
- The backend filters practices that match your selections.
- Practices are ranked based on a **cost-effectiveness score** between -1 and 1 (lower absolute value = better balance between performance and fairness).
- The practices that have a good balance between fairness improvements and performance losses are returned with:
  - **Title of the practice**
  - **Cost-effectiveness score**
  - Relevant **performance** and **fairness** metrics for the selected task

### 5. Visualize Practice Graph
- You can also request a graph visualization that shows:
  - Nodes: the selected context and the recommended practices
  - Edges: connections between the context and each practice
  - Node colors reflect cost-effectiveness (green for balanced practices)

