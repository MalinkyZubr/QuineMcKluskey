import time
from typing import Callable
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.classes import Token


def time_execution(to_time: Callable) -> tuple[int, str]:
    start_time: float = time.time()
    return_value: str = to_time()
    end_time: float = time.time()
    
    return end_time - start_time, return_value

def extract_nested_expression(stringified_expression: str) -> str:
    print(stringified_expression[0])
    open_count: int = 1
    closed_count: int = 0
    
    index = 1
    
    while open_count > closed_count and index < len(stringified_expression):
        if stringified_expression[index] == "(":
            open_count += 1
        elif stringified_expression[index] == ")":
            closed_count += 1
        index += 1
        
    print(stringified_expression[1:index - 1])
    return stringified_expression[1:index - 1]


def tokenize_expression(stringified_expression: str) -> list[str | list]:
    not_flag = False
    index: int = 0
    tokenized_expression: list[str] = []
    
    while index < len(stringified_expression):
        token: str | list[str] = stringified_expression[index]
        if token != "!":
            if token == "(":
                nested_expression: str = extract_nested_expression(stringified_expression[index:])
                token: list[str | list] = tokenize_expression(nested_expression)
                index += len(nested_expression)
                
            if token not in (" ", ")"):
                if not_flag:
                    token = ["!", token]
                    not_flag = False
                tokenized_expression.append(token)
        else:
            not_flag = True
        index += 1
        
    return tokenized_expression
        
def identify_extractable(token_table: dict[str, Token]) -> list[Token]:
    first_key: list[str] = list(token_table.keys())[0]
    maximum_references: list[Token] = [token_table[first_key]]
    
    for token in token_table.values():
        if token.count > maximum_references[0].count:
            maximum_references = [token]
        elif token.count == maximum_references[0].count:
            maximum_references.append(token)
    
    return maximum_references

def extract_token_groups(token_set: list[str | list]) -> list[list[str | list]]:
    token_groups: list[list[str | list]] = []
    current_token_group: list[str] = []
    
    for token in token_set:
        if token == "+":
            token_groups.append(current_token_group)
            current_token_group = []
        else:
            if isinstance(token, list):
                token = extract_token_groups(token)
            current_token_group.append(token)
    
    if current_token_group:
        token_groups.append(current_token_group)
    
    return token_groups

def extract_distributed(grouped_token_set: list[list[str]]):
    for group in grouped_token_set:
        pass
            
            
        
        
            

