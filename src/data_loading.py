import csv
from typing import Optional


ILLEGAL_HEADER_CHARACTERS = {"!", " ", "~", "&", "|", "(", ")", "+", "*"}
ALLOWED_BOOLEAN_CHARACTERS = {"x", "0", "1"}


def check_csv_headers_illegal_format(headers: list[str], filename: str) -> None:    
    for index, header in enumerate(headers):
        base_error = f"Column {index}, {header} of CSV file {filename}"
        if len(header) != 1:
            if "O" not in header:
                raise NameError(f"{base_error} contains input longer than 1 character. For the sake of clarity in final output, ensure input column lengths do not exceed 1 character")
            else:
                extracted_header = header[1:]
                try: int(extracted_header)
                except: raise NameError(f"{base_error} is an output, but contains secondary identifiers that are not integers. Outputs should only contain 'O' and numbers.\nExamples: O1, O2, O3")
        elif header in ILLEGAL_HEADER_CHARACTERS:
            raise NameError(f"{base_error} uses character {header} which violates input rules. Characters from the set: {ILLEGAL_HEADER_CHARACTERS} cannot be used")
        
def check_data_dimension(current_row: dict[str, str], current_row_index: int, filename: str, previous_row: Optional[dict[str, str]]) -> None:
    if previous_row and len(previous_row) != len(current_row):
        raise Exception(f"Row {current_row_index} of file {filename} differs in length from row {current_row_index - 1}. All rows must be of equal dimension")
    
def check_data_illegal_characters(current_row: dict[str, str], row_number: int, filename: str) -> None:
    for column_header, row_value in current_row.items():
        if row_value not in ALLOWED_BOOLEAN_CHARACTERS:
            raise Exception(f"Boolean value {row_value} stored at column {column_header} and row {row_number} in {filename} is illegal! Allows boolean characters are: {ALLOWED_BOOLEAN_CHARACTERS}")
            
def load_csv(csv_path: str) -> list[dict[str, str]]:
    if ".csv" not in csv_path:
        raise NameError(f"The file {csv_path} must be a CSV file!")
    with open(csv_path) as file:
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        rows: list[str] = []

        for row_number, row in enumerate(csv_reader):
            if line_count == 0:
                headers: list[str] = row
                check_csv_headers_illegal_format(headers, csv_path)
            else:
                row: dict[str, str] = dict(zip(headers, row))
                check_data_dimension(row, row_number, csv_path, rows[-1] if row_number > 1 else None)
                check_data_illegal_characters(row, row_number, csv_path)
                rows.append(row)
            line_count += 1
    
    return rows