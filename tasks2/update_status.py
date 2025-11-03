import json
import sys
import os

DATA_FILE = "tasks.json"

def load_tasks():
	if not os.path.exists(DATA_FILE):
		return []
	with open(DATA_FILE, "r") as f:
		return json.load(f)

def save_tasks(tasks):
	with open(DATA_FILE, "w") as f:
		json.dump(tasks, f, indent=2)

def main():
	if len(sys.argv) < 3:
		print("Usage: python update_status.py <task_number> <status>")
		print("Status options: 'not started', 'started', 'complete'")
		return
	
	try:
		task_num = int(sys.argv[1])
	except ValueError:
		print("Error: Task number must be an integer")
		return
	
	status = " ".join(sys.argv[2:]).lower()
	
	valid_statuses = ["not started", "started", "complete"]
	if status not in valid_statuses:
		print(f"Error: Invalid status. Must be one of: {', '.join(valid_statuses)}")
		return
	
	tasks = load_tasks()
	
	if not tasks:
		print("No tasks found.")
		return
	
	if task_num < 1 or task_num > len(tasks):
		print(f"Error: Task number must be between 1 and {len(tasks)}")
		return
	
	tasks[task_num - 1]["status"] = status
	save_tasks(tasks)
	print(f"Task {task_num} status updated to: {status}")
	print(f"Task: {tasks[task_num - 1]['description']}")

if __name__ == "__main__":
	main()
