import ast
from astmonkey import visitors


class Optimizer(ast.NodeTransformer):

    # optimising nodes with Binary operation type
    def visit_BinOp(self, node):
        node = Optimizer.generic_visit(self, node)

        # Addition
        if isinstance(node.op, ast.Add):
            # zero case (num + 0 = num, a + 0 = a)
            if isinstance(node.left, ast.Constant) and node.left.value == 0:
                return node.right

            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                return node.left

            # general case
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if type(node.left.value) == type(node.right.value):
                    return ast.Constant(
                        value=node.left.value + node.right.value
                    )

        # Subtraction
        if isinstance(node.op, ast.Sub):
            # zero case (num - 0 = num, a - 0 = a)
            if isinstance(node.left, ast.Constant) and node.left.value == 0:
                return node.right

            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                return node.left

            #general case
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.right.value, (int, float)) and isinstance(node.left.value, (int, float)):
                    return ast.Constant(
                        value=node.left.value - node.right.value
                    )

        # Multiplication
        if isinstance(node.op, ast.Mult):
            # zero case (num*0 = 0, a*0 = 0)
            if isinstance(node.left, ast.Constant) and node.left.value == 0 or \
                    isinstance(node.right, ast.Constant) and node.right.value == 0:
                return ast.Constant(
                    value=0
                )

            #general case
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.right.value, (int, float)) and isinstance(node.left.value, (int, float)):
                    return ast.Constant(
                        value=node.left.value * node.right.value
                    )

        # Division
        if isinstance(node.op, ast.Div):
            #zero case (a / 0)
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                print("Zero division error")
                return node

            # zero case (0/a = 0)
            if isinstance(node.left, ast.Constant) and node.left.value == 0:
                return ast.Constant(
                    value=0
                )

            #general case
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.right.value, (int, float)) and isinstance(node.left.value, (int, float)):
                    return ast.Constant(
                        value=node.left.value / node.right.value
                    )

        # Mod
        if isinstance(node.op, ast.Mod):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.right.value, (int, float)) and isinstance(node.left.value, (int, float)):
                    try:
                        return ast.Constant(
                            value=node.left.value % node.right.value
                        )
                    except ZeroDivisionError:
                        print("Zero division error")

        # Power
        if isinstance(node.op, ast.Pow):
            if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                if isinstance(node.right.value, (int, float)) and isinstance(node.left.value, (int, float)):
                    return ast.Constant(
                            value=node.left.value**node.right.value
                    )

        return node


print("enter your line")
code = input()

tree = ast.parse(code)
new_tree = ast.fix_missing_locations(Optimizer().visit(tree))
generated_code = visitors.to_source(new_tree)
print(generated_code)

"""
Написана оптимизация для:
1) случая сложения констант. Рассмотрено сложение с 0.
2) случая вычитания констант и рассмотрен случай ноля
3) умножения констант и 0
4) деления и случаи с 0
5) взятия остатка
6) возведения в степень
"""
