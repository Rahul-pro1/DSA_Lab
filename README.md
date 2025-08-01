# DSA Lab Interactive Platform

This is an interface to enable users to solve DSA problems and understand various data structures and algorithms through simulations. The system is implemented as multiple microservices running on separate Docker containers, which are orchestrated using Kubernetes.

The system's landing page provides routes to:
- **Repository of problems**
- **Tree traversal visualization**
- **Sorting algorithm visualizations**
- **Graph traversals**
- **Breadth-First Search (BFS) & Depth-First Search (DFS)** simulators

The **Problem Repository** further routes users to the **Code Execution Window**, where users can:
- Solve problems using **Python**, **C**, **C++**, **Java**, or **JavaScript**
- Validate their solutions against **test cases**
- **Add**, **Edit**, or **Delete** problems based on needs

---

## How to Run the Project

Follow the steps below to get the entire system up and running:

### 1. **Clone the repository**
```bash
git clone https://github.com/Rahul-pro1/DSA_Lab.git
cd DSA_Lab
```

### 2. Create a .env file
Inside the root directory, create a `.env` file and add the following:
```env
MONGODB_URI=<your_mongodb_connection_string>
```
Replace `<your_mongodb_connection_string>` with your actual MongoDB connection string (e.g., from MongoDB Atlas or local instance).

### 3. Push container images to Docker Hub  
Ensure you have Docker installed and logged into Docker Hub:
```bash
docker login
```

Then build and push each service image:
```bash
docker build -t <your-dockerhub-username>/problem_repo ./problem_repo
docker push <your-dockerhub-username>/problem_repo

docker build -t <your-dockerhub-username>/code_exec ./code_exec
docker push <your-dockerhub-username>/code_exec

# Repeat similarly for landing_page, bfs_dfs, dij_flw, sorting, tree_traversal
```

### 4. Deploy with Kubernetes
Make sure Kubernetes is running (e.g., via Docker Desktop or Minikube):

```bash
kubectl config current-context
kubectl create namespace dsa-lab
kubectl apply -f k8s/  # Assuming all your deployment & ingress YAMLs are in the `k8s/` directory
```

### 5. Add `dsa.lab.local` to your hosts file
To access via the custom domain:

- Open `/etc/hosts` (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows) and add:
```
127.0.0.1 landing.dsa.lab.local
127.0.0.1 repo.dsa.lab.local
127.0.0.1 exec.dsa.lab.local
127.0.0.1 bfs.dsa.lab.local
127.0.0.1 dij.dsa.lab.local
127.0.0.1 sort.dsa.lab.local
127.0.0.1 tree.dsa.lab.local
```

### 6. Access the application
Open your browser and go to:
```
http://landing.dsa.lab.local/landing-page
```

### Tech Stack
- **Python:** Primary language for implementing backend logic, algorithms, and visualizations.
- **Docker:** To containerize & manage each microservice.
- **Kubernetes:** For scalable and efficient orchestration of the Docker containers.
- **Streamlit:** For building interactive web interfaces for each microservice.
- **MongoDB:** To store problems, test cases, and related metadata.
- **GraphViz:** Used in the Tree Traversal visualizer for rendering graph/tree structures.
