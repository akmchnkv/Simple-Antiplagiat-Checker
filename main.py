import ast
import argparse
import sys


def create_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('input_path', type=str, help='Input file')
    args_parser.add_argument('output_path', type=str, help='Output file')
    return args_parser


class Analyzer(ast.NodeTransformer):
    def node_visit(self, node):
        self.generic_visit(node)
        return node

    def node_visit_from(self, node):
        self.generic_visit(node)
        return node

    def translate_name(self, node):
        self.generic_visit(node)
        return node.id

    def translate_num(self, node):
        self.generic_visit(node)
        return str(node.n)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        ast.get_docstring(node, clean=True)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef):
        ast.get_docstring(node, clean=True)
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef):
        ast.get_docstring(node, clean=True)
        self.generic_visit(node)
        return node


def code_conversion(file):
    code = open(file, 'r').readlines()
    tree_ast = ast.parse('\n'.join(code))
    analyzer = Analyzer()
    tree_ast = analyzer.visit(tree_ast)
    return ast.dump(tree_ast)


def levenstein(ast1, ast2):
    n, m = len(ast1), len(ast2)
    if n > m:
        ast1, ast2 = ast2, ast1
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if ast1[j - 1] != ast2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return round((n - current_row[n]) / n, 2)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Check the correctness of your input")
    else:
        parser = create_parser()
        args = parser.parse_args(sys.argv[1:])
        files = open(args.input_path, 'r').readlines()
        output = open(args.output_path, 'w')
        for line in files:
            file1, file2 = line.split()
            a = code_conversion('./plagiat/' + file1)
            b = code_conversion('./plagiat/' + file2)
            res = str(levenstein(a, b))
            output.write(res)
            output.write('\n')
        output.close()
