import json
import sys
import os

DATA_FILE = "tasks.json"

def load_tasks():
	if not os.path.exists(DATA_FILE):
		return []
	with open(DATA_FILE, "r") as f:
		return json.load(f)

def main():
	if len(sys.argv) < 2:
		print("Usage: python search.py <search term>")
		return
	term = " ".join(sys.argv[1:]).lower()
	tasks = load_tasks()
	found = [task for task in tasks if term in task['description'].lower()]
	if not found:
		print("No matching tasks found.")
		return
	for i, task in enumerate(found, 1):
		status = task.get('status', 'not started')
		print(f"{i}. [{status.upper()}] {task['description']}")
		if 'due_date' in task:
			print(f"   Due: {task['due_date']}")
		if 'note' in task:
			print(f"   Note: {task['note']}")

if __name__ == "__main__":
	main()
