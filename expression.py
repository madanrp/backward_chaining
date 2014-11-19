__author__ = 'madanrp'

SIMPLE_EXPR = 0
AND_EXPR = 1
IMPLICATION = 2

from utility import *

class Expression():
    def __init__(self):
        pass


class Clause:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def get_name(self):
        return self.name

    def get_arguments(self):
        return self.arguments

    def get_variables(self):
        variables = []
        for arg in self.arguments:
            if arg[0].islower():
                variables.append(arg)
        return variables

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if len(self.arguments) != len(other.arguments):
            return False
        for i in range(len(self.arguments)):
            if self.arguments[i] != other.arguments[i]:
                return False
        return True

    def __str__(self):
        return self.name + "(" + ",".join(self.arguments) + ")"

    def does_unify(self, other):
        if self.name == other.name:
            for i in range(len(self.arguments)):
                x = self.arguments[i]
                y = other.arguments[i]
                if (is_constant(x) and is_constant(y) and not(x == y)):
                    return False
            return True
        else:
            return False

    #to be used only does_unify returns true
    def unify(self, other):
        dic = {}
        for i in range(len(self.arguments)):
            var = self.arguments[i]
            val = other.arguments[i]
            if is_variable(var):
                dic[var] = val
            elif is_variable(val):
                dic[val] = var
        return dic

    def unify_and_ret(self, theta):
        arguments = []
        for arg in self.arguments:
            if arg in theta:
                arguments.append(theta[arg])
            else:
                arguments.append(arg)
        new_clause = Clause(self.name, arguments)
        return new_clause

class SimpleExpression(Expression):
    def __init__(self, clause= None):
        self.type = SIMPLE_EXPR
        self.clause = clause

    def add_clause(self, clause):
        self.clause = clause

    def get_clause(self, clause):
        return self.clause

    def __eq__(self, other):
        assert isinstance(other, SimpleExpression)
        return (self.type == other.type and self.clause == other.clause)

    def does_unify(self, other):
        assert isinstance(other, SimpleExpression)
        return self.clause.does_unify(other.clause)


class AndExpression(Expression):
    def __init__(self):
        self.type = AND_EXPR
        self.clauses = []
        self.all_clause_satisfied = False

    def add_clause(self, expr):
        self.clauses.append(expr)

    def get_clauses(self):
        return self.clauses

    def get_variables(self):
        variables = []
        for clause in self.clauses:
            vars = clause.get_variables()
            for var in vars:
                variables.append(var)
        return variables


class ImplicationExpression(Expression):
    def __init__(self):
        self.type = IMPLICATION
        self.goal = None
        self.premises = []

    def add_goal(self, expr):
        self.goal = expr

    def get_goal(self):
        return self.goal

    def add_premise(self, expr):
        self.premises.append(expr)

    def get_premises(self):
        return self.premises

    def goal_match(self, other):
        assert isinstance(other, Clause)
        return self.goal == other

    def does_goal_unify(self, goal):
        assert isinstance(goal, SimpleExpression)
        result = self.goal.does_unify(goal.clause)
        return result


class KnowledgeBase:
    def __init__(self, simples, implications):
        self.simples = simples
        self.implications = implications

    def find_implication(self, goal):
        theta = {}
        for implication in self.implications:
            if implication.does_goal_unify(goal):
                theta = implication.get_goal().unify(goal.clause)
                premises = implication.get_premises()
                new_premises = []
                for premise in premises:
                    new_premises.append(SimpleExpression(premise.unify_and_ret(theta)))
                return theta, new_premises
        return theta, []

    def does_unify_simple(self, goal):
        for simple in self.simples:
            if goal == simple or goal.does_unify(simple):
                return True
        return False

    def unify_simple(self, goal):
        for simple in self.simples:
            if goal.clause.does_unify(simple.clause):
                theta = goal.clause.unify(simple.clause)
                return theta
        return None

    def fol_bc_or(self, goal, theta):
        for simple in self.simples:
            if goal == simple:
                return theta
            if goal.does_unify(simple):
                theta1 = self.unify_simple(goal)
                for var in theta1:
                    if  var in theta and theta[var] != theta1[var]:
                        return None
                    theta[var] = theta1[var]
                return theta

        tmp_theta, new_premises = self.find_implication(goal)
        if len(new_premises) == 0:
            return None

        theta1 = self.fol_bc_and(new_premises, tmp_theta)

        return theta1

    def fol_bc_and(self, goals, theta):
        if theta is None:
            pass
        elif not goals:
            return theta
        else:
            first, rest = goals[0], goals[1:]
            theta1 = self.fol_bc_or(first, theta)
            if theta1:
                theta2 = self.fol_bc_and(rest, theta1)
                return theta2