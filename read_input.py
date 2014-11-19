__author__ = 'madanrp'

from expression import *

def construct_clause(str, standard_var_count):
    name, args = str.split("(")
    args = args.split(")")[0]
    args = args.split(",")
    for index, arg in enumerate(args):
        if is_variable(arg.strip()):
            args[index] = arg.strip() + "_%d" % standard_var_count
        else:
            args[index] = arg.strip()
    clause = Clause(name.strip(), args)
    return clause

def read_input(file):
    sentence_count = 1
    lines = open(file, 'r').readlines()
    simple_sentences = []
    implication_sentences = []

    #goal constrcution
    goal_str = lines[0].strip()
    clause = construct_clause(goal_str, sentence_count)
    goal = SimpleExpression()
    goal.add_clause(clause)

    for line in lines[2:]:
        sentence_count += 1
        line = line.strip()
        implication_found = False
        if line.find("=>") != -1:
            implication_found = True

        lhs = ""
        rhs = None

        if implication_found:
            lhs, rhs = line.split("=>")
            lhs = lhs.strip()
            rhs = rhs.strip()
        else:
            lhs = line.strip()
            rhs = None

        and_found = 0
        lhs_clauses = []
        if lhs.find("&") != -1:
            clauses = lhs.split("&")
            for clause in clauses:
                lhs_clauses.append(construct_clause(clause.strip(), sentence_count))
        else:
            lhs_clauses.append(construct_clause(lhs, sentence_count))

        rhs_clause = None
        if rhs:
            rhs_clause = construct_clause(rhs, sentence_count)

        if implication_found:
            sentence = ImplicationExpression()
            for expr in lhs_clauses:
                sentence.add_premise(expr)
            sentence.add_goal(rhs_clause)
            implication_sentences.append(sentence)
        else:
            sentence = SimpleExpression()
            for clause in lhs_clauses:
                sentence.add_clause(clause)
            simple_sentences.append(sentence)
    return goal, simple_sentences, implication_sentences

def write_output(file, output):
    f = open(file, "w")
    f.write(output)
    f.close()

if __name__ == "__main__":
    goal, simples, implications = read_input("input.txt")
    KB = KnowledgeBase(simples, implications)
    output = "FALSE"
    try:
        goal_found = False

        answers = KB.fol_bc_or(goal, {})

        if answers:
            output = "TRUE"

    except Exception, e:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)

    write_output("output.txt", output)