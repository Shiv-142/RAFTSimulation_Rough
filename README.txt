To run...
First run: "pip install -r requirements.txt"
Then: "python main.py" or "python3 main.py"

Game Description: 
This program was created in Pygame and is meant to simulate the RAFT election algorithm. 
Each of the nodes are on their own thread, and there are enemy cubes moving towards the nodes to kill them. Clicking on enemy cubes accumulates points. 
When a leader node dies (indicated by the color changing from blue to red), an election begins, with the node with the highest term number becoming the new leader. Nodes in yellow are in a candidate state
