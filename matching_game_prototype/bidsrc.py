import ast, textwrap

def extract_function_source(code_text: str, func_name: str) -> str:
    tree = ast.parse(code_text)

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            # Extract the exact source lines corresponding to the function
            lines = code_text.splitlines()
            func_lines = lines[node.lineno - 1 : node.end_lineno]
            return "\n".join(func_lines)
    return None

def load_bid_function(text, func_name):
    """
    Extract the bid_function from the text and then return a callable object.
    """
    source = extract_function_source(text, func_name)
    local_vars = {}
    exec(source, {}, local_vars)
    if "bid" not in local_vars:
        raise ValueError("Didn't find bid function, please input text like 'def bid(...): ... '.")
    return local_vars["bid"]