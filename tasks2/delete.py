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
	if len(sys.argv) < 2:
		print("Usage: python delete.py <task_number>")
		return
	
	try:
		task_num = int(sys.argv[1])
	except ValueError:
		print("Error: Task number must be an integer")
		return
	
	tasks = load_tasks()
	
	if not tasks:
		print("No tasks found.")
		return
	
	if task_num < 1 or task_num > len(tasks):
		print(f"Error: Task number must be between 1 and {len(tasks)}")
		return
	
	deleted_task = tasks.pop(task_num - 1)
	save_tasks(tasks)
	print(f"Task {task_num} deleted: {deleted_task['description']}")

if __name__ == "__main__":
	main()
