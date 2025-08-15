from os import remove
import subprocess as sp
import json

exit_words = ["exit", "quit", "q"]
help_words = ["help", "h"]
full_parameter_list = [
    "id",
    "name",
    "description",
    "make",
    "model",
    "serial",
    "width",
    "height",
    "refreshRate",
    "x",
    "y",
    "activeWorkspace",
    "specialWorkspace",
    "reserved",
    "scale",
    "transform",
    "focused",
    "dpmsStatus",
    "vrr",
    "solitary",
    "activelyTearing",
    "directScanoutTo",
    "disabled",
    "currentFormat",
    "mirrorOf",
    "availableModes",
]

current_hypr_monitor_config = []
hyprland_file_path = "./hyprland.conf"
hyprland_file_start_line = "MONITOR SCRIPT START HERE"
hyprland_file_stop_line = "MONITOR SCRIPT STOP HERE"


def open_hyprland_file(file_path):
    with open(file_path) as f:
        found_start = False
        for line in f:
            if line.find("\n") == 0:
                continue
            if line.find(hyprland_file_stop_line) == 4:
                print("Found stop line ")
                break
            if found_start:
                current_hypr_monitor_config.append(line.replace("\n", ""))

            if line.find(hyprland_file_start_line) == 4:
                found_start = True
                print("found start")
    return current_hypr_monitor_config


print(open_hyprland_file(hyprland_file_path))


def get_hyprctl_monitors_list() -> list:

    cmd = sp.run(["hyprctl", "monitors", "-j"], capture_output=True).stdout

    return json.loads(cmd)


monitor_list = get_hyprctl_monitors_list()


def print_monitor_info(mon, parameter_list):

    for param in parameter_list:
        try:
            if param == "availableModes":
                print(f"---> |{mon["id"]}| availableModes:")
                for mode in mon["availableModes"]:
                    print(f"---> |{mon["id"]}|\t\t\t-  {mode}")
                continue
            print(f"---> |{mon["id"]}| {param:<15}\t-  {mon[param]}")
        except KeyError:
            print(f"> Could not understand parameter {param}")


def print_monitor_list(*args):

    print_mon_list = monitor_list
    print_parameters = [
        "id",
        "name",
        "description",
        "make",
        "model",
        "width",
        "height",
        "refreshRate",
    ]
    for i, arg in enumerate(args[0]):
        if arg == "-l":
            for param in full_parameter_list:
                print(f"> {param}")

            return

        if arg == "-f":
            print_parameters = full_parameter_list

        if arg == "-a":
            try:
                next_arg = args[0][i + 1]
                print_parameters.append((next_arg))
            except IndexError:
                print("> No extra parameter given!")

        if arg == "-m":
            select_mon_id = 0
            try:
                next_arg = args[0][i + 1]
                if next_arg.isdigit():
                    select_mon_id = int(next_arg)
            except IndexError:
                print("> No monitor N given, printing monitor 0!")

            try:
                print_monitor_info(print_mon_list[select_mon_id], print_parameters)
            except IndexError:
                print("> Monitor index out of range")
            return

    for i, mon in enumerate(print_mon_list):
        print(f"> HWP MONITOR {i}:")
        print_monitor_info(mon, print_parameters)
        print()


def update_monitor_list(*args):
    monitor_list = get_hyprctl_monitors_list()
    print(f"> Updated monitor list, found {len(monitor_list)} monitors")


def print_help_text(func_list):
    for func in func_list:
        print(f">\t{func[1]:<15}\t|\t\t{func[2]}")
    print(">\thelp\t\t|\t\tPrint help menu")
    print(">\tquit\t\t|\t\tQuit the program")
    print(">\texit\t\t|\t\tExit the program")


inf_print_monitor_list = [
    print_monitor_list,
    "print",
    """Prints out full monitors list
--->\t   -a [param] for more params
--->\t   -l for param list
--->\t   -f for all parameters
--->\t   -m [N] for monitor N""",
]
inf_update_monitors_list = [
    update_monitor_list,
    "update",
    "Updates the stored monitor list",
]

inf_main_menu_list = [inf_print_monitor_list, inf_update_monitors_list]


def get_user_input(func_list):
    inp = input("HWP> ").rsplit(sep=" ")

    if inp[0].lower() in help_words:
        print_help_text(func_list)
        return True

    if inp[0].lower() in exit_words:
        return False

    for func_lst in func_list:
        if inp[0] == func_lst[1]:
            func_lst[0](inp)
    return True


def main():

    monitor_list = get_hyprctl_monitors_list()

    while get_user_input(inf_main_menu_list):
        pass


if __name__ == "__main__":

    main()
