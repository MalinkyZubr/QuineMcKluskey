import time
from typing import Callable

from src.classes import Token


def time_execution(to_time: Callable) -> tuple[int, str]:
    start_time: float = time.time()
    return_value: str = to_time()
    end_time: float = time.time()
    
    return end_time - start_time, return_value

def tokenize_expression(stringified_expression: str) -> list[str | list]:
    not_flag = False
    index: int = 0
    tokenized_expression: list[str] = []
    
    while index < len(stringified_expression):
        token: str | list[str] = stringified_expression[index]
        if token == "(":
            closing_parentheses_index = stringified_expression[index + 1:].find(")")
            nested_tokens = stringified_expression[index + 1: closing_parentheses_index]
            token = tokenize_expression(nested_tokens)
        elif token == "!":
            not_flag = True
            index += 1
            continue
        index += 1
        
        if not_flag:
            token = ["!", token]
        tokenized_expression.append(token)
        
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

def extract_expressions(token_set: list[str | list], extractable: list[Token]) -> list[str | list]:
    # make sure to handle + and " " properly when extracting distributed values
    # also make sure to check ref indicies on each max reference token
    pass

def distributive(stringified_expression: str) -> tuple[list[str | None], list]:
    tokenized: list[str | list] = tokenize_expression(stringified_expression)
    token_table: dict[str, Token] = dict()
    index: int = 0
    
    while index < len(tokenized):
        token: list | str = tokenized[index]
        if type(token) == list:
            extracted, nested_tokens = distributive(token)
            
            tokenized[index] = extracted
            tokenized.insert(index + 1, nested_tokens)
            token = extracted
        elif token and token not in {"!", " ", "+"}:
            if token not in token_table:
                token_table[token] = Token(token, index)
            else:
                token_table[token].add_ref_location(index)
    
    extractable: list[Token] = identify_extractable(token_table)
            
            
        
        
            

