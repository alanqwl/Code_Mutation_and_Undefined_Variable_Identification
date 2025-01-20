import ast

class OpTransformer(ast.NodeVisitor):

    def visit_BinOp(self, node):
        op = node.op
        if isinstance(op, ast.Add):
            node.op = ast.Sub()
        if isinstance(op, ast.Sub):
            node.op = ast.Add()
        if isinstance(op, ast.Mult):
            node.op = ast.Div()
        if isinstance(op, ast.Div):
            node.op = ast.Mult()
        self.generic_visit(node)
    
    def visit_Compare(self, node):
        op = node.ops
        for i in range(len(op)):
            if isinstance(op[i], ast.GtE):
                op[i] = ast.Lt()
            if isinstance(op[i], ast.LtE):
                op[i] = ast.Gt()
        self.generic_visit(node)
    
class FunctionCall(ast.NodeVisitor):
    def __init__(self):
        self.func_call = []

    def visit_Call(self, node):
        name = node.func
        self.func_call.append(ast.unparse(name))
        self.generic_visit(node)

class FunctionDef(ast.NodeTransformer):
    def __init__(self, func_call):
        self.func_call = func_call

    def visit_FunctionDef(self, node):
        defName = node.name
        if defName not in self.func_call:
            return None
        else:
            return node
        
def input(src_code):
    tree = ast.parse(src_code)
    transform = OpTransformer()
    transform.visit(tree)
    delete_1 = FunctionCall()
    delete_1.visit(tree)
    delete_2 = FunctionDef(delete_1.func_call)
    delete_2.visit(tree)

    all_vars = []
    local_vars = []
    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            for x in ast.iter_child_nodes(node):
                if isinstance(x, ast.Assign):
                    local_vars.append(x)
        
        if isinstance(node, ast.Assign):
            all_vars.append(node)
        
    global_vars = []
    for element in all_vars:
        if element not in local_vars:
            global_vars.append(ast.unparse(element.__dict__['targets']))

    global_vars = list(set(global_vars))
    for variable in global_vars:
        insert_expression = 'print(' + variable + ')'
        expr = ast.parse(insert_expression).body[0]
        tree.body.append(expr)
    return ast.unparse(tree)

if __name__ == '__main__':
    filePath = 'pretest1/7.py'
    file = open(filePath)
    src_code = ''
    for line in file:
        src_code += line
    print('input:\n', src_code)
    output = input(src_code)
    print('\n')
    print('output:\n', output)