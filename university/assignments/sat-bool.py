def is_satisfiable(formula):
    def backtrack(assignment):
        if len(assignment) == len(variables):
            return evaluate(formula, assignment)
        var = select_unassigned_variable(assignment)
        for value in [True, False]:
            assignment[var] = value
            if backtrack(assignment):
                return True
            assignment[var] = None
        return False
    
    variables = extract_variables(formula)
    return backtrack({})

def evaluate(formula, assignment):
    for clause in formula:
        clause_eval = False
        for literal in clause:
            var, is_negated = literal
            if var in assignment:
                if assignment[var] == is_negated:
                    clause_eval = True
                    break
        if not clause_eval:
            return False
    return True

def extract_variables(formula):
    variables = set()
    for clause in formula:
        for literal in clause:
            var, _ = literal
            variables.add(var)
    return variables

def select_unassigned_variable(assignment):
    for var in assignment:
        if assignment[var] is None:
            return var

formula = [[('x1', False), ('x2', False)], [('x1', True), ('x3', False)], [('x2', True)]]
print("A formula kielégíthető." if is_satisfiable(formula) else "A formula nem kielégíthető.")
