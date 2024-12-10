import argparse
import json
import random
from datetime import datetime


def load_json(file="data.json"):
    task_json = {}

    try:
        with open(file, "r") as f:
            task_json = json.load(f)

    except FileNotFoundError:
        pass

    if not task_json:
        print('no json')
        return {}
    
    task_list = {}
    for t_id, t_data in task_json.items():
        task_list.update({t_id: t_data})

    return task_list
    
def save_json(data, file="data.json"):
    # Serialize
    with open(file, 'w+') as f:
        json.dump(data, f)


task_list = task_list = load_json()

def main():
    parser = argparse.ArgumentParser()
    actions = parser.add_subparsers(title="commands", description="valid commands to manage tasks", required=True, dest="action")
    add_action = actions.add_parser("add", help="add a new task")
    update_action = actions.add_parser("update", help="update an existing task")
    mark_action = actions.add_parser("mark", help="change status of existing task")
    delete_action = actions.add_parser("delete", help="delete existing task")
    list_action = actions.add_parser("list", help="list existing tasks")

    # add action
    add_action.add_argument("description", help="description of task")
    add_action.add_argument("-s", "--status", dest="status", help="status of task", default="todo", required=False, choices=["todo", "in-progress", "done"])

    # update action
    update_action.add_argument("id", help="id of the task")
    update_action.add_argument("description", help="description of task")

    # mark action
    mark_action.add_argument("id", help="id of task")
    mark_action.add_argument("status", help="status of task")

    # delete action
    delete_action.add_argument("id", help="id of task")

    # list action
    list_action.add_argument("-s", "--status", dest="status", help="status of task", required=False, choices=["todo", "in-progress", "done"])

    # parse args
    args = vars(parser.parse_args())

    # Call function based on action in args
    task = FUNCTION_MAP[args["action"]](args, task_list)
    if task:
        task_list.update(task)
    
    if args["action"] != "list":
        list_func({"status": ""}, task_list)

    # save json
    save_json(task_list)

    # print output
    #list_func('', task_list)

def add_func(args, task_list):
    # generate id number
    t_id = len(task_list)
    t_desc = args["description"]
    t_status = args["status"]
    t_created_at = datetime.now().ctime()
    t_updated_at = datetime.now().ctime()

    return {t_id: [t_desc, t_status, t_created_at, t_updated_at]}

def update_func(args, task_list):
    # Get task id
    t_id = args["id"]
    # Update desc
    task_list[t_id][0] = args["description"]
    task_list[t_id][2] = datetime.now().ctime()

def mark_func(args, task_list):
    # Get task id
    t_id = args["id"]
    # Update desc
    task_list[t_id][1] = args["status"]
    task_list[t_id][2] = datetime.now().ctime()

def delete_func(args, task_list):
    # Get task id
    t_id = args["id"]
    # Update desc
    task_list[t_id][0] = ""

def list_func(args, task_list):
    # constants for borders
    TOP_LEFT, TOP_RIGHT, BOT_RIGHT, BOT_LEFT, HORIZONTAL, VERTICAL = "╭", "╮", "╯", "╰", "─", "│"
    # get max length for each string
    max_id = 4 # covers digits up to 9999
    max_desc = 0 # variable but can set minimum
    max_status = 11 # always 11 for in-progress

    # get filter
    list_filter = args["status"]

    t_str_list = []
    for t_id, t_data in task_list.items():
        # If task deleted or not in filter (if there is one)
        if t_data[0] == '' or (list_filter and t_data[1] != list_filter):
            continue

        # get max desc
        if len(t_data[0]) > max_desc:
            max_desc = len(t_data[0])

        t_str_1 = f"{t_id!s:^{max_id}}| "
        t_str_2 = f"{t_data[1]:^{max_status}} | {t_data[2]} | {t_data[3]}"

        t_str_list.append((t_str_1, t_str_2, t_data[0]))

    # get border lengths
    horiz_length = max_id + max_desc + max_status + 60 # 60 = hardcoded spacing for datetime

    t_fin = [" Taskify", f"{TOP_LEFT}{HORIZONTAL * horiz_length}{TOP_RIGHT}"]

    id_header = "id"
    desc_header = "description"
    status_header = "status"
    updated_header = "updated at"
    created_header = "created at"

    t_fin.append(f"{VERTICAL}{id_header:^{max_id}}| {desc_header:^{max_desc}} | {status_header:^{max_status}} | {updated_header:^25}|{created_header:^25} {VERTICAL}")
    for t_str_tup in t_str_list:
        t_str_1, t_str_2, desc = t_str_tup
        t_fin.append(f"{VERTICAL}{t_str_1}{desc:^{max_desc}} | {t_str_2} {VERTICAL}")
    t_fin.append(f"{BOT_LEFT}{HORIZONTAL * horiz_length}{BOT_RIGHT}")

    [print(line) for line in t_fin]

FUNCTION_MAP ={
    "add": add_func,
    "update": update_func,
    "mark": mark_func,
    "delete": delete_func,
    "list": list_func
}

if __name__ == "__main__":
    # test_args = [
    #     # ["add", "test 0"],
    #     # ["add", "test 1"],
    #     # ["add", "test 2"],
    #     # ["delete", "2"],
    #     # ["add", "test 3"],
    #     # ["mark","3", "done"],
    #     ["list"],
    #     []
    # ]
    # for test_arg in test_args:
    #     main(test_arg)
    main()