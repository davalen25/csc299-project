import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
	if not os.path.exists(DATA_FILE):
		return []
	with open(DATA_FILE, "r") as f:
		return json.load(f)

def main():
	tasks = load_tasks()
	if not tasks:
		print("No tasks found.")
		return
	for i, task in enumerate(tasks, 1):
		status = task.get('status', 'not started')
		print(f"{i}. [{status.upper()}] {task['description']}")
		if 'due_date' in task:
			print(f"   Due: {task['due_date']}")
		if 'note' in task:
			print(f"   Note: {task['note']}")

if __name__ == "__main__":
	main()
