from typing import Iterable


class Minterm:
    pass

class Minterm:
    def __init__(self, expression: dict[str, str], comprising: tuple[Minterm, Minterm] | None, id: str = ""):
        self.expression: dict[str, str] = expression
        self.matched: bool = False
        self.layer: int = 0
        self.comprising: tuple[Minterm, Minterm] = comprising
        self.id: str = id

    def get_num_terms(self) -> int:
        return len(self.expression)

    def count_true(self) -> int:
        count = 0
        
        for value in self.expression.values():
            if(value == "1"):
                count += 1

        return count
    
    def __diff(self, minterm: Minterm) -> list[str]:
        foreign_expression: Iterable = minterm.expression.items()
        non_matching_columns: list[str] = []

        for column, value in foreign_expression: # change to while
            if value != self.expression[column]:
                non_matching_columns.append(column)
            
        return non_matching_columns

    def will_match(self, minterm: Minterm) -> bool: # optimize later
        return len(self.__diff(minterm)) == 1

    def match_next_minterm(self, minterm: Minterm) -> Minterm:
        difference: list[str] = self.__diff(minterm)
        new_expression = {column:(value if column not in difference else "x") for column, value in self.expression.items()}

        new_minterm: Minterm = Minterm(new_expression, (self, minterm))
        self.matched = True
        minterm.set_matched()

        return new_minterm
    
    def set_matched(self):
        self.matched = True

    def is_matched(self) -> bool:
        return self.matched
    
    def get_root_comprising(self) -> list[Minterm]:
        root_comprising: list[Minterm] = []

        if not self.comprising:
            root_comprising = [self]
        else:
            root_comprising = self.comprising[0].get_root_comprising() + self.comprising[1].get_root_comprising()

        return root_comprising
    
    def __eq__(self, other: Minterm):
        return self.expression == other.expression
    
    def __str__(self):
        stringified: str = ""

        for column, value in self.expression.items():
            if value == "1":
                stringified += column
            elif value == "0":
                stringified += "!" + column

        return stringified
    

class RootMinterm:
    def __init__(self, minterm: Minterm):
        self.minterm: Minterm = minterm
        self.is_alone = False
    
    def set_alone(self):
        self.is_alone = True

    def check_alone(self) -> bool:
        return self.is_alone
    