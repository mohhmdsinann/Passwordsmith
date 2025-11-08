#!/usr/bin/env python3
# pattern.py — generates and filters passwords; symbols BETWEEN groups only; no leet
import itertools
import sys
import time
import os

PLACEHOLDERS = ['a','b','c','d','e','f','g','h','i']  # allowed groups

# Default symbol and number fallbacks
DEFAULT_SYMBOLS = ['@','!', '#','_','.', '*', '&', '$', '-']
DEFAULT_NUMBERS = ['123', '1234', '12345', '1230', '007', '2020', '2021']

def has_three_consecutive_same(seq):
    run = 1
    for i in range(1, len(seq)):
        if seq[i] == seq[i-1]:
            run += 1
            if run >= 3:
                return True
        else:
            run = 1
    return False

def generate_sequences(min_groups=1, max_groups=9):
    """Yield placeholder sequences length min..max excluding triple repeats."""
    for n in range(min_groups, max_groups + 1):
        for tup in itertools.product(PLACEHOLDERS, repeat=n):
            if has_three_consecutive_same(tup):
                continue
            yield list(tup)

def expand_sequence_with_tokens_and_middle_symbols(seq, profile, symbol_list):
    """
    Given seq like ['a','b','c'], expand to concrete strings by:
      - substituting one token from each placeholder group in order, and
      - for each between-slot, choose either '' (no symbol) or one symbol from symbol_list.
    Yields each concrete string.
    """
    # Build token lists for each placeholder
    lists = []
    for ph in seq:
        vals = profile.get(ph, [])
        # if any placeholder has no tokens, expansion impossible for this seq
        if not vals:
            return
        lists.append(vals)

    slots = len(seq) - 1
    # separator choices for each between-slot: empty or one symbol
    sep_choices = [''] + (symbol_list if symbol_list else DEFAULT_SYMBOLS)

    # iterate all token choices (cartesian product of token lists)
    for token_combo in itertools.product(*lists):
        # if there are no separator slots, yield the single token_combo joined
        if slots == 0:
            yield ''.join(token_combo)
            continue

        # otherwise, iterate separator choices for each slot
        for seps in itertools.product(sep_choices, repeat=slots):
            # interleave tokens and separators to build string
            parts = []
            for i, tok in enumerate(token_combo):
                parts.append(tok)
                if i < slots:
                    parts.append(seps[i])
            candidate = ''.join(parts)
            yield candidate

def write_rules_file(out_path):
    """
    Write a simple Hashcat/JtR rule file next to the output file.
    This is a basic set of example rules (capitalize, append digit, append 123).
    """
    rules_path = os.path.splitext(out_path)[0] + '.rule'
    try:
        with open(rules_path, 'w', encoding='utf-8') as rf:
            rf.write('# Passwordsmith generated rule file (basic transforms)\n')
            rf.write('c\n')     # capitalize first letter
            rf.write('$1\n')   # append '1'
            rf.write('$123\n') # append '123'
            rf.write('^123\n') # prepend '123'
        print(f"Rules file saved: {rules_path}")
    except Exception as ex:
        print("Error writing rules file:", ex)

def generate_and_write(profile, target_count, out_path, min_len=8, max_len=32, min_groups=1, max_groups=9, options=None):
    """
    Streams expanded passwords (with middle-symbols) to out_path.
    - profile: dict mapping 'a'..'i' and 'j' (symbols) to lists of tokens
    - symbol list is expected in profile['j'] (if absent, DEFAULT_SYMBOLS used)
    - target_count: stops when this many passwords have been written
    - min_len / max_len: inclusive character length filter
    - options: dict, supports 'export_rules' boolean
    """
    if options is None:
        options = {}
    export_rules = bool(options.get('export_rules'))

    # prepare symbol list from profile['j'] if present
    symbol_list = profile.get('j', []) or DEFAULT_SYMBOLS

    # ensure profile keys a..i are lists and strings
    for k in ['a','b','c','d','e','f','g','h','i']:
        if k not in profile:
            profile[k] = []
        else:
            profile[k] = [str(x) for x in profile[k]]

    written = 0
    start_time = time.time()
    with open(out_path, 'w', encoding='utf-8') as f:
        for seq in generate_sequences(min_groups=min_groups, max_groups=max_groups):
            for cand in expand_sequence_with_tokens_and_middle_symbols(seq, profile, symbol_list):
                L = len(cand)
                if L < min_len or L > max_len:
                    continue
                f.write(cand + '\n')
                written += 1
                if written % 100000 == 0:
                    elapsed = int(time.time() - start_time)
                    print(f"Wrote {written} lines... elapsed {elapsed}s")
                if written >= target_count:
                    if export_rules:
                        write_rules_file(out_path)
                    return
    # finished all combos
    if export_rules:
        write_rules_file(out_path)
    return
