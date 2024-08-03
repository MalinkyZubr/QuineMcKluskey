import sys
sys.path.append("/home/malinkyzubr/Desktop/InterruptExpander/hardware/logic")

import pytest

from scripts.QuineMcluskey import *


def test_extract_single_out_cols():
    row = {"a":1, "b":2, "c":3, "O1":4, "O5":3}
    assert extract_single_out_cols(row, "O1") == {"a":1, "b":2, "c":3, "O1":4}

def test_extract_single_output_rows():
    rows = [{"a":1, "b":2, "c":3, "O1":4, "O5":3} for x in range(3)]
    assert extract_single_output_rows(rows, "O1") == [{"a":1, "b":2, "c":3, "O1":4} for x in range(3)]

def test_separate_outputs():
    rows = [{"a":1, "b":2, "c":3, "O1":4, "O5":3} for x in range(3)]

    first_set = [{"a":1, "b":2, "c":3, "O1":4} for x in range(3)]
    second_set = [{"a":1, "b":2, "c":3, "O5":3} for x in range(3)]

    assert separate_outputs(rows) == {"O1":first_set, "O5":second_set}

def test_identify_minterms():
    dataset = [
        {"a":"1", "b":"0", "c":"1", "d":"0", "O5":"1"},
        {"a":"0", "b":"0", "c":"1", "d":"0", "O5":"0"}
    ]

    minterms = identify_minterms(dataset, "O5")
    assert minterms[0].expression == {"a":"1", "b":"0", "c":"1", "d":"0"}
    assert len(minterms) == 1

def test_generate_groups():
    minterms_list = [
        Minterm({"a":"1", "b":"0", "c":"1", "d":"0"}, None), 
        Minterm({"a":"0", "b":"0", "c":"1", "d":"1"}, None),
        Minterm({"a":"0", "b":"1", "c":"1", "d":"1"}, None)
    ]

    groups = generate_groups(minterms_list)

    assert groups[2][0].expression == {"a":"1", "b":"0", "c":"1", "d":"0"}
    assert groups[2][1].expression == {"a":"0", "b":"0", "c":"1", "d":"1"}
    assert groups[3][0].expression == {"a":"0", "b":"1", "c":"1", "d":"1"}

def test_generate_matched_pairs_single():
    prime_midterm = Minterm({"a":"0", "b":"0", "c":"1", "d":"0"}, None)
    minterms_list = [
        Minterm({"a":"0", "b":"1", "c":"1", "d":"0"}, None), 
        Minterm({"a":"0", "b":"0", "c":"1", "d":"1"}, None),
        Minterm({"a":"0", "b":"1", "c":"1", "d":"x"}, None)
    ]

    matched_pairs = generate_matched_pairs_single(prime_midterm, minterms_list)

    assert len(matched_pairs) == 2

    assert matched_pairs[0].expression == {"a":"0", "b":"x", "c":"1", "d":"0"}
    assert matched_pairs[1].expression == {"a":"0", "b":"0", "c":"1", "d":"x"}

    assert prime_midterm in matched_pairs[0].comprising
    assert minterms_list[0] in matched_pairs[0].comprising

def test_generate_matched_pairs_2_group():
    minterms_list1 = [
        Minterm({"a":"0", "b":"1", "c":"1", "d":"0"}, None), 
        Minterm({"a":"0", "b":"0", "c":"1", "d":"1"}, None),
        Minterm({"a":"0", "b":"1", "c":"1", "d":"x"}, None)
    ]

    minterms_list2 = [
        Minterm({"a":"0", "b":"1", "c":"1", "d":"1"}, None), 
        Minterm({"a":"1", "b":"0", "c":"1", "d":"1"}, None),
        Minterm({"a":"1", "b":"1", "c":"1", "d":"x"}, None)
    ]

    matched_pairs, prime_implicants = generate_matched_pairs_2_group(minterms_list1, minterms_list2)

    assert len(matched_pairs) == 5
    assert len(prime_implicants) == 0

    assert matched_pairs[0].expression == {"a":"0", "b":"1", "c":"1", "d":"x"}

    minterms_list1 = [
        Minterm({"a":"0", "b":"0", "c":"0", "d":"1"}, None), 
    ]

    minterms_list2 = [
        Minterm({"a":"1", "b":"1", "c":"0", "d":"0"}, None), 
        Minterm({"a":"1", "b":"0", "c":"1", "d":"0"}, None)
    ]

    matched_pairs, prime_implicants = generate_matched_pairs_2_group(minterms_list1, minterms_list2)

    assert len(prime_implicants) == 1
    assert len(matched_pairs) == 0

def test_generate_matched_pairs_group():
    groups = {
        0: [Minterm({"a":"0", "b":"0", "c":"0", "d":"0"}, None)],
        1: [Minterm({"a":"1", "b":"0", "c":"0", "d":"0"}, None), 
            Minterm({"a":"0", "b":"0", "c":"1", "d":"0"}, None)],
        2:
            [Minterm({"a":"0", "b":"1", "c":"1", "d":"0"}, None), 
            Minterm({"a":"0", "b":"0", "c":"1", "d":"1"}, None),
            Minterm({"a":"0", "b":"1", "c":"1", "d":"x"}, None)
            ],
        3: 
            [Minterm({"a":"0", "b":"1", "c":"1", "d":"1"}, None), 
            Minterm({"a":"1", "b":"0", "c":"1", "d":"1"}, None),
            Minterm({"a":"1", "b":"1", "c":"1", "d":"x"}, None)]
        }
    
    matched_pairs, prime_implicants = generate_matched_pairs_group(groups)

    assert len(matched_pairs) == 9
    assert len(prime_implicants) == 0

def test_recurse_find_all_prime_implicants():
    minterms = [
        Minterm({"a":"0", "b":"0", "c":"0", "d":"0"}, None),
        Minterm({"a":"1", "b":"0", "c":"0", "d":"0"}, None),
        Minterm({"a":"0", "b":"0", "c":"1", "d":"0"}, None),
        Minterm({"a":"0", "b":"1", "c":"1", "d":"0"}, None),
        Minterm({"a":"0", "b":"0", "c":"1", "d":"1"}, None),
        Minterm({"a":"0", "b":"1", "c":"1", "d":"x"}, None),
        Minterm({"a":"0", "b":"1", "c":"1", "d":"1"}, None),
        Minterm({"a":"1", "b":"0", "c":"1", "d":"1"}, None),
        Minterm({"a":"1", "b":"1", "c":"1", "d":"x"}, None)
    ]
    
    primes = recurse_find_all_prime_implicants(minterms)

    expressions = [prime.expression for prime in primes]

    assert len(expressions) == 5

    proper_expressions = [
        {"a":"x", "b":"0", "c":"0", "d":"0"},
        {"a":"0", "b":"0", "c":"x", "d":"0"},
        {"a":"x", "b":"0", "c":"1", "d":"1"},
        {"a":"x", "b":"1", "c":"1", "d":"x"},
        {"a":"0", "b":"x", "c":"1", "d":"x"}
    ]

    for expression in expressions:
        assert expression in proper_expressions

    return primes

def test_get_root_comprising():
    minterm: Minterm = Minterm({"a":"0", "b":"x", "c":"1", "d":"x"},
                               (
                                   Minterm({"a":"0", "b":"x", "c":"1", "d":"0"}, 
                                           (
                                               Minterm({"a":"0", "b":"0", "c":"1", "d":"0"}, None),
                                               Minterm({"a":"0", "b":"1", "c":"1", "d":"0"}, None)
                                           )
                                        ),
                                   Minterm({"a":"0", "b":"x", "c":"1", "d":"1"}, 
                                           (
                                               Minterm({"a":"0", "b":"0", "c":"1", "d":"1"}, None),
                                               Minterm({"a":"0", "b":"1", "c":"1", "d":"1"}, None)
                                           )
                                        )
                                    )
                                )
    
    assert len(minterm.get_root_comprising()) == 4

def test_generate_prime_implicant_table():
    primes = test_recurse_find_all_prime_implicants()

    assert len(primes) == 5

    prime_implicant_table = generate_prime_implicant_table(primes)
    assert len(generate_prime_implicant_table(primes)) == 5

    return prime_implicant_table

def test_identify_essential_prime_implicants():
    prime_implicants = test_recurse_find_all_prime_implicants()
    print(prime_implicants)

    essential_prime_implicants = identify_essential_prime_implicants(prime_implicants)

    assert len(essential_prime_implicants) == 4