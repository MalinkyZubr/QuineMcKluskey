from src.classes import Minterm, RootMinterm
    

def extract_single_out_cols(row: dict[str, str], output_key: str) -> dict[str, str]:
    return {key:value for key, value in row.items() if key == output_key or "O" not in key.upper()}

def extract_single_output_rows(rows: list[dict[str, str]], output_key: str) -> list[dict, str]:
    return [extract_single_out_cols(row, output_key) for row in rows]

def separate_outputs(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    headers: list[str] = list(rows[0].keys())
    output_keys: list[str] = list(filter(lambda x: "O" in str(x), headers))

    output_datasets: dict = {key:extract_single_output_rows(rows, key) for key in output_keys}

    return output_datasets

def identify_minterms(output_group: list[dict[str, str]], output_column_header: str) -> list[Minterm]:
    minterms: list[dict[str, str]] = list(filter(lambda x: x[output_column_header] == "1", output_group))

    minterm_object_list: list[Minterm] = []
    for index, row in enumerate(minterms):
        row.pop(output_column_header)
        minterm_object_list.append(Minterm(row, None, str(index)))

    return minterm_object_list

def generate_groups(minterms: list[Minterm]) -> dict[int, list[Minterm]]:
    groups: dict[int, list[Minterm]] = dict()

    for minterm in minterms:
        num_true: int = minterm.count_true()
        if num_true not in groups:
            groups[num_true] = []
        groups[num_true].append(minterm)

    return groups

def generate_matched_pairs_single(selected_minterm: Minterm, next_group: list[Minterm]) -> list[Minterm]:
    new_minterms: list[Minterm] = []

    for minterm in next_group:
        if selected_minterm.will_match(minterm):
            new_minterms.append(selected_minterm.match_next_minterm(minterm))
    
    return new_minterms

def generate_matched_pairs_2_group(group_1: list[Minterm], group_2: list[Minterm]) -> tuple[list[Minterm], list[Minterm]]:
    new_minterms: list[Minterm] = []
    prime_implicants: list[Minterm] = []

    for minterm in group_1:
        new_minterms += generate_matched_pairs_single(minterm, group_2)

        if not minterm.is_matched():
            prime_implicants.append(minterm)
    
    return new_minterms, prime_implicants

def get_unmatched_in_group(group: list[Minterm]) -> list[Minterm]:
    return [minterm for minterm in group if not minterm.is_matched()]

def generate_matched_pairs_group(groups: dict[int, list[Minterm]]) -> tuple[list[Minterm], list[Minterm]]:
    minterm_pairs: list[Minterm] = []
    prime_implicants: list[Minterm] = []

    for group_num, group in groups.items():
        if group_num + 1 in groups:
            generated_minterms, generated_prime_implicants = generate_matched_pairs_2_group(group, groups[group_num + 1])
            minterm_pairs += generated_minterms
            prime_implicants += generated_prime_implicants
        else:
            prime_implicants += get_unmatched_in_group(group)
    
    return minterm_pairs, prime_implicants

def remove_duplicate_implicants(minterms: list[Minterm]) -> list[Minterm]:
    current_index: int = 0

    while current_index < len(minterms):
        current_minterm: Minterm = minterms[current_index]

        if minterms.count(current_minterm) > 1:
            minterms.pop(current_index)
        else:
            current_index += 1
    
    return minterms

def recurse_find_all_prime_implicants(minterms: list[Minterm]) -> list[Minterm]:
    groups: dict[int, list[Minterm]] = generate_groups(minterms)
    minterm_pairs, prime_implicants = generate_matched_pairs_group(groups)

    if len(minterm_pairs):
        prime_implicants += recurse_find_all_prime_implicants(minterm_pairs)

    return remove_duplicate_implicants(prime_implicants)

def generate_prime_implicant_table(prime_implicants: list[Minterm]) -> list[tuple[Minterm, list[Minterm]]]:
    origin_minterms_table: list[tuple[Minterm, list[Minterm]]] = list()

    for prime_implicant in prime_implicants:
        origin_minterms_table.append((prime_implicant, prime_implicant.get_root_comprising()))

    return origin_minterms_table

def flatten_origin_minterms(prime_implicants_table: list[tuple[Minterm, list[Minterm]]]) -> list[Minterm]:
    all_origin_minterms: list[Minterm] = []

    for prime_implicant, associated_minterms in prime_implicants_table:
        all_origin_minterms += associated_minterms

    return all_origin_minterms

def identify_essential_prime_implicants(prime_implicants: list[Minterm]) -> set[Minterm]:
    prime_implicants_table: list[tuple[Minterm, list[Minterm]]] = generate_prime_implicant_table(prime_implicants)
    essential_prime_implicants: list[Minterm] = list()
    all_origin_minterms: list[Minterm] = flatten_origin_minterms(prime_implicants_table)

    for prime_implicant, associated_minterms in prime_implicants_table:
        for minterm in associated_minterms:
            if all_origin_minterms.count(minterm) == 1 and minterm not in essential_prime_implicants:
                essential_prime_implicants.append(prime_implicant)
    
    return essential_prime_implicants

def format_expression(essential_prime_implicants: list[Minterm], output_column_header: str) -> str:
    return output_column_header + ": " + " + ".join({str(epi) for epi in essential_prime_implicants})

def quine_mckluskey_minimize(boolean_group: list[dict[str, str]], output_column_header: str) -> str:
    all_origin_minterms: list[Minterm] = identify_minterms(boolean_group, output_column_header)
    prime_implicants: list[Minterm] = recurse_find_all_prime_implicants(all_origin_minterms)
    essential_prime_implicants: list[Minterm] = identify_essential_prime_implicants(prime_implicants)

    return format_expression(essential_prime_implicants, output_column_header)

def quine_mckluskey_mppool(output_group: tuple[list[dict[str, str]], str]):
    return quine_mckluskey_minimize(output_group[1], output_group[0])

def minimize_dataset(dataset_loaded: list[dict[str, str]]) -> list[str]:
    separated_output_tables: dict[str, dict[str, str]] = separate_outputs(dataset_loaded)
    
    # with multiprocessing.Pool(len(separated_output_tables)) as p:
    #     fully_processed = p.map(quine_mckluskey_mppool, list(separated_output_tables.items()))
    
    fully_processed = [quine_mckluskey_minimize(group, header) for header, group in separated_output_tables.items()]

    return list(fully_processed)