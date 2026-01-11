# Community Detection in Complex Networks

This repository contains the code and resources developed for my **Final Degree Project (TFG)** focused on community detection in graphs and complex networks. The main objective is to analyze and implement algorithms that allow the identification of groups of nodes with high internal connection density.

## 📝 Project Description

Community detection is a fundamental task in network analysis (social, biological, transportation, etc.). This project explores various algorithmic approaches to solve this problem, evaluating their efficiency and the quality of the partitions obtained.

### Algorithms Included:
- **Louvain Method:** Hierarchical optimization of modularity.
- **Girvan-Newman Algorithm:** Based on the centrality of edge intermediation.
- **Label Propagation (LPA):** Algorithm based on label diffusion.
- **Leiden Algorithm:** Improvement of the Louvain method to ensure well-connected communities.

## 🛠️ Requirements and Installation

To run the code in this repository, you will need to have **Python 3.8+** installed. 

1. Clone the repository:
```bash
   git clone [https://github.com/jorge1380/Community-detection.git](https://github.com/jorge1380/Community-detection.git)
   cd Community-detection
   ```

2. Install Python dependencies

```bash
  pip install -r backend/requirements.txt
  ```

3. Install Node.js dependencies
```bash
  cd frontend
 npm install
  ```

4. Start the frontend
  ```bash
  cd frontend
  npm run dev
  ```

5. Start the backend
  ```bash
  cd backend
  pypy main.py # Run with PyPy, replace with Python if you don't want to install PyPy
  ```
