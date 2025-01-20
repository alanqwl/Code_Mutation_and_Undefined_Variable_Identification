import ast

# detect whether an assignment statement uses undefined varible
def detectInAssignment(assign, defined_variable, count):
    value = assign.value
    if isinstance(value, ast.BinOp):
        fg, cnt = detectInBinOp(value, defined_variable, count)
        return fg, cnt
    elif isinstance(value, ast.Name):
        if value.id in defined_variable:
            return True, count
        else:
            count += 1
            return False, count
    elif isinstance(value, ast.Constant):
        return True, count
    else:
        print('error')
        return False, count

# detect whether undefined variable is used in a binary operator
# This function is defined recursively to deal with cases like "x = 1 + y + z"
def detectInBinOp(Binop, defined_variable, count):
    flag = True
    if isinstance(Binop.right, ast.Name) and Binop.right.id not in defined_variable:
        count += 1
        flag = False
    if isinstance(Binop.left, ast.Constant):
        if flag:
            return True, count
        else:
            return False, count
    elif isinstance(Binop.left, ast.Name):
        if Binop.left.id in defined_variable and flag:
            return True, count
        else:
            if Binop.left.id not in defined_variable:
                count += 1
            return False, count
    elif isinstance(Binop.left, ast.BinOp):
        fg, cnt = detectInBinOp(Binop.left, defined_variable, count)
        return fg, cnt
    else:
        print('error')
        return False, count
    
'''
This function detect unused variable in function calls.
"definition" is the function definition node of the detected function in the ast
"defined_variable" stores the variables which are defined outside the function
"func_dict" and "func_def" contains information of all functions in the program
'''
def detectInFunction(definition, defined_variable, defined_parameter, undefined_parameter, func_dict, func_def, count):
    defined_in_function = defined_variable + defined_parameter      # store defined local variables in a function 
    defaultListLength = len(definition.args.defaults)

    # add default variable to the list of defined local variable
    for i in range(len(definition.args.args) - defaultListLength, len(definition.args.args)):
        if definition.args.args[i].arg not in defined_in_function and definition.args.args[i].arg not in undefined_parameter:
            defined_in_function.append(definition.args.args[i].arg)
    func = definition.body

    for node in func:

        # case 1: For an assignment in a function, we need to call the helper function above to detect unused variable
        if isinstance(node, ast.Assign):
            fg, count = detectInAssignment(node, defined_in_function, count)
            if fg:
                for target in node.targets:
                    defined_in_function.append(target.id)
            else:
                # remove it from the list since it becomes undefined
                for target in node.targets:
                    if target.id in defined_in_function:
                        defined_in_function.remove(target.id)
        
        # case 2: For a function call in the function, we use "detectInFunction" helper function to detect unused variable
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            value = node.value
            defpara_next_level = []
            undefined_next_level = []
            for args_index in range(len(value.args)):
                if isinstance(value.args[args_index], ast.Name):
                    if value.args[args_index].id in defined_in_function:
                        defpara_next_level.append(func_dict[value.func.id][args_index].arg)
                    else:
                        undefined_next_level.append(func_dict[value.func.id][args_index].arg)
            target_function = func_def[value.func.id]
            count = detectInFunction(target_function, defined_variable, defpara_next_level, undefined_next_level, func_dict, func_def, count)
        else: 
            pass
    return count

# main procedures for the detection process
def main(tr):
    defined_variable = []
    body = tr.__dict__['body']
    count = 0
    func_dict = {}
    func_def = {}
    for object in body:
        if isinstance(object, ast.Assign):
            flag, count_tmp = detectInAssignment(object, defined_variable, 0)
            count += count_tmp
            if not flag:
                # remove the varible if it exists in the list of defined variable
                for variable in object.targets:
                    if variable.id in defined_variable:
                        defined_variable.remove(variable.id)
            else:
                for variable in object.targets:
                    if variable.id not in defined_variable:
                        defined_variable.append(variable.id)

        elif isinstance(object, ast.FunctionDef):
            func_dict[object.name] = object.args.args
            func_def[object.name] = object

        elif isinstance(object, ast.Expr) and isinstance(object.value, ast.Call):
            defined_parameter = []
            undefined_parameter = []
            func = func_def[object.value.func.id]

            for i in range(len(object.value.args)):
                element = object.value.args[i]
                if isinstance(element, ast.Name):
                    if element.id in defined_variable:
                        defined_parameter.append(func.args.args[i].arg)
                    else:
                        undefined_parameter.append(func.args.args[i].arg)
                else:
                    defined_parameter.append(func.args.args[i].arg)
            
            for j in range(len(object.value.keywords)):
                keyword_arg = object.value.keywords[j].arg
                keyword_value = object.value.keywords[j].value
                if isinstance(keyword_value, ast.Constant):
                    defined_parameter.append(keyword_arg)
                elif isinstance(keyword_value, ast.Name):
                    if keyword_value.id in defined_variable:
                        defined_parameter.append(keyword_arg)
                    else:
                        undefined_parameter.append(keyword_arg)
                elif isinstance(keyword_value, ast.BinOp):
                    count_tmp = 0
                    flag, count_tmp = detectInAssignment(object.value.keywords[j], defined_variable, count_tmp)
                    print(count_tmp)
                    if flag:
                        defined_parameter.append(keyword_arg)
                    else:
                        undefined_parameter.append(keyword_arg)
                else:
                    pass
            count = detectInFunction(func, defined_variable, defined_parameter, undefined_parameter, func_dict, func_def, count)
    return count, defined_variable

def input(src):
    tree = ast.parse(src)
    count, def_var = main(tree)
    return count

if __name__ == '__main__':
    filePath = 'pretest2/7.py'
    file = open(filePath)
    sourceCode = ''
    for line in file:
        sourceCode += line
    result = input(sourceCode)
    print(result)