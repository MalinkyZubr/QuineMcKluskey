import csv
import argparse
import enum


class ExpressionType(enum.Enum):
    POS: int = "0"
    SOP: int = "1"


def process_single_output(output_column_header: str, dataset, expression_type: ExpressionType) -> list[str]:
    output_expression = []
    for row in range(len(dataset[output_column_header])):
        print(expression_type.value)
        print(dataset[output_column_header][row])
        if (dataset[output_column_header][row] == expression_type.value):
            row_expression = locate_true_row_inputs(row, dataset, expression_type)
            if row_expression:
                output_expression.append(row_expression)
    
    return output_expression
            
def SOP_generate_value(value: str, column: str) -> str:
    if value == "1":
        return_value = column
    elif value == "0":
        return_value = "!" + column
    
    return return_value

def POS_generate_value(value: str, column: str) -> str:
    if value == "0":
        return_value = column
    elif value == "1":
        return_value = "!" + column
    
    return return_value

def locate_true_row_inputs(row: int, dataset: list[bool], expression_type: ExpressionType) -> str:
    expression = ""
    for header, column in dataset.items():
        if "O" not in header and "N" not in header and column[row] != "x":
            if expression_type == ExpressionType.SOP:
                expression += SOP_generate_value(column[row], header)
            else:
                expression += POS_generate_value(column[row], header) + " "
                print(expression)

    if expression_type == ExpressionType.POS:
        expression_split = expression.split(" ")
        expression_add = " + ".join(expression_split[:-1])
        expression = "(" + expression_add + ")"
    return expression

def process_truth_table(dataset: dict[str, list], expression_type: ExpressionType)-> dict[list[str]]:
    output_expression_dict = dict()

    for header in dataset.keys():
        if "O" in header:
            output_expression_dict[header] = process_single_output(header, dataset, expression_type)
    
    return output_expression_dict

def load_truth_csv(filepath: str) -> dict[str, list]:
    with open(filepath) as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                headers = row
                table = dict(zip(headers, [[] for x in range(len(headers))]))
            else:
                for index, item in enumerate(table.items()):
                    header, column = item
                    column.append(row[index])
            line_count += 1
    
    return table


def parse_output(generated_output: str, expression_type: ExpressionType):
    parsed_output = ""
    for header, result in generated_output.items():
        if expression_type == ExpressionType.SOP:
            parsed_output += f'{header}: {" + ".join(result)}\n'
        else:
            parsed_output += f'{header}: {"".join(result)}\n'

    return parsed_output


if __name__ == "__main__":
    print(parse_output(process_truth_table(load_truth_csv(r"/home/malinkyzubr/Desktop/InterruptExpander/hardware/logic/TRUTH_TABLE2.csv"), ExpressionType.SOP), ExpressionType.SOP))