def create_uc_function(*args, **kwargs):
    """
    Create and return a UC function using a function tempate
    :param args:
    :param kwargs:
    :return:
    """
    f_name = args[0]  # Name of the function
    f_code = args[1]  # Command ID for Serial communication or Dict of commands
    if type(args[1]) == int:
        f_code = args[1]
    elif type(args[1]) == dict:
        function_params = args[1]  # type: dict
        f_code = function_params["command"]
        function_params.pop('command', None)
        print(f"Keys: {function_params.keys()}")

    def function_template(*args, duration: int = 0, repeat: int = 1, verbose: bool =False, **kwargs):
        if verbose:
            print(f"Calling function: {f_name}")
            print(f"     duration: {duration}")
            print(f"     repeat:   {repeat}")

        # Store non default data
        other_parameters = []

        # Loop over values and add to data
        for name, value in kwargs.items():
            if verbose:
                print('     {0} = {1}'.format(name, value))
            if type(value) == int:
                other_parameters.append(value)
            else:
                other_parameters += value

        code_list = [(f_code >> 8) & 0xFF, (f_code & 0xFF)]
        duration_list = [duration >> 8, duration & 0xFF]
        run_list = [repeat >> 8, repeat & 0xFF]
        if verbose:
            print((code_list + duration_list + run_list + other_parameters))

    return function_template


x = create_uc_function("foo", 0x3001)
x(duration=100)

y = create_uc_function("bar", {"command": 0x3001, "curve": 1})
y(curve=8, data=[1,2,3], duration=100)
