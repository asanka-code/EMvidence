
uc_command_dict = {}
with open("uc_commands.csv") as f:
    csv_data = f.read()
    for line in csv_data.split('\n'):
        data = line.split(',')
        if len(data) == 2:
            uc_command_val = int(data[0], 16)
            uc_command_name = data[1]
            uc_command_dict[uc_command_val] = uc_command_name

print(uc_command_dict)
