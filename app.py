import argparse
import jsonManager
from datetime import datetime
from tabulate import tabulate

def tasks(args):
    data = jsonManager.read_json()
    if len(data) < 1:
        print('There are no pending tasks')
        return
    table_data = []
    table_data.append(['ID', 'Description', 'Status', 'Created At', 'Updated At'])
    for task in data:
        aux = [task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt']]
        table_data.append(aux)
    print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))

def addTask(args):
    if args is None:
        print('You must write a description for the task')
        return
    try:
        data = jsonManager.read_json()
        newID = len(data) + 1
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        newTask = {
            "id": newID,
            "description": args.description,
            "status": "todo",
            "createdAt": date,
            "updatedAt": ""
        }
        data.append(newTask)
        jsonManager.write_json(data)
        print (f"Task added successfully (ID: {newID})")
    except Exception as e:
        print(f"An error has ocurred: {e}")

def main():
    parser = argparse.ArgumentParser(description = "Task Tracker CLI Application")
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    parser_add = subparsers.add_parser('add', help = "Add a new task")
    parser_add.add_argument('description', type=str, help="Task description")
    parser_add.set_defaults(func = addTask)

    parser_tasks = subparsers.add_parser('tasks', help = "List all tasks")
    parser_tasks.set_defaults(func = tasks)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func(args)

if __name__ == '__main__':
    main()