# DSA Lab Interactive Platform

We have built an interface to enable users to solve DSA problems and understand various data structures and algorithms through simulations. The system is implemented as multiple microservices running on separate Docker containers. 

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
Inside the root directory, create a .env file and add the following:
```env
MONGODB_URI=<your_mongodb_connection_string>
```
Replace <your_mongodb_connection_string> with your actual MongoDB connection string (e.g., from MongoDB Atlas or local instance).

### 3. Build and run the containers
Ensure Docker is installed and running on your system, then run:
```bash
docker-compose up --build
```

### 4. Access the application
Once the services are running, open your browser and visit http://localhost:8507, which will display the landing page.

### Tech Stack
- **Python:** Primary language for implementing backend logic, algorithms, and visualizations.
- **Docker:** To containerize & manage each microservice.
- **Streamlit:** For building interactive web interfaces for each microservice.
- **MongoDB:** To store problems, test cases, and related metadata.
- **GraphViz:** Used in the Tree Traversal visualizer for rendering graph/tree structures.
