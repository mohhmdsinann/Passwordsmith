#!/usr/bin/env python3
# engine.py — collects input and calls pattern generator (no leet)
import os
import sys
from datetime import datetime
import pattern  # local module; ensure pattern.py sits beside this file

# ---------------- Config ----------------
MIN_LINES = 10000
MAX_LINES = 10_000_000  # 10 million
LARGE_WARN_THRESHOLD = 100_000  # require extra confirmation if > this

# ANSI color codes
C_RESET = '\033[0m'
C_RED = '\033[31m'
C_GREEN = '\033[32m'
C_YELLOW = '\033[33m'
C_CYAN = '\033[36m'
C_BOLD = '\033[1m'

# ---------------- Helpers ----------------
def colored(prompt, color=C_CYAN, bold=False):
    return (C_BOLD if bold else '') + color + prompt + C_RESET

def safe_input(prompt, required=False):
    try:
        while True:
            v = input(prompt).strip()
            if v == '' and not required:
                return ''
            if v == '' and required:
                print(colored("Input required. Please type a value.", C_YELLOW))
                continue
            return v
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(1)

def split_tokens(s, max_items=25):
    if not s:
        return []
    parts = [p.strip() for p in s.split(',') if p.strip()]
    bad = [p for p in parts if ' ' in p]
    if bad:
        print(colored(f"Tokens must not contain spaces. Found: {', '.join(bad)}", C_RED))
        sys.exit(1)
    if len(parts) > max_items:
        print(colored(f"Warning: More than {max_items} tokens provided — truncating extras.", C_YELLOW))
        parts = parts[:max_items]
    return parts

def confirm_yes(prompt):
    v = safe_input(colored(prompt + " (Y/n): ", C_CYAN), required=True)
    return v.lower() == 'y'

# ---------------- Profile collection ----------------
def collect_profile():
    print("\n" + colored("=== Passwordsmith — input profile ===", C_GREEN, bold=True) + "\n")

    ack = safe_input(colored("Type 'I understand' to continue (case-insensitive): ", C_YELLOW), required=True)
    if ack.strip().lower() != 'i understand':
        print(colored("Acknowledgement not accepted. Exiting.", C_RED))
        sys.exit(1)

    # target_count prompt (bounds)
    while True:
        s = safe_input(colored(f"Enter maximum number of lines to save (min {MIN_LINES}, max {MAX_LINES}): ", C_CYAN), required=True)
        try:
            n = int(s)
            if n < MIN_LINES or n > MAX_LINES:
                print(colored(f"Number out of range. Must be between {MIN_LINES} and {MAX_LINES}.", C_YELLOW))
                continue
            target_count = n
            break
        except ValueError:
            print(colored("Enter a valid integer.", C_YELLOW))

    # If very large, show a warning and require explicit PROCEED
    if target_count > LARGE_WARN_THRESHOLD:
        print("\n" + colored("WARNING: You requested a very large wordlist.", C_RED, bold=True))
        print(colored("Generating millions of passwords can take a long time, use lots of disk, and may slow/stop your device.", C_RED))
        if safe_input(colored("Type 'PROCEED' to confirm you understand and want to continue: ", C_YELLOW), required=True) != 'PROCEED':
            print(colored("Confirmation not given. Aborting.", C_RED))
            sys.exit(1)

    # Input tokens (groups a..i)
    print("\nProvide tokens as comma-separated lists (no spaces inside tokens). Leave blank if none (except required fields).")
    a = split_tokens(safe_input(colored("1) Firstname(s) [a] (required): ", C_CYAN), required=True))
    b = split_tokens(safe_input(colored("2) Lastname(s) [b] (required): ", C_CYAN), required=True))
    c = split_tokens(safe_input(colored("3) Nicknames [c] (optional): ", C_CYAN)))
    d = split_tokens(safe_input(colored("4) Birthyear / important years [d] (optional): ", C_CYAN)))
    e = split_tokens(safe_input(colored("5) City / State [e] (optional): ", C_CYAN)))
    f = split_tokens(safe_input(colored("6) Social usernames [f] (required): ", C_CYAN), required=True))
    g = split_tokens(safe_input(colored("7) Pet / Partner names [g] (optional): ", C_CYAN)))
    h = split_tokens(safe_input(colored("8) Phone endings / custom numbers [h] (optional): ", C_CYAN)))
    i = split_tokens(safe_input(colored("9) Hobbies / extra words [i] (optional): ", C_CYAN)))

    syms_raw = safe_input(colored("Symbols to prefer [j] (comma-separated) — leave blank for default '@,!#_.*&$-': ", C_CYAN))
    symbols = split_tokens(syms_raw) if syms_raw else ['@','!', '#','_','.', '*', '&', '$', '-']

    # Export rule file option
    export_rules = confirm_yes("Export Hashcat/JtR rule file after generation?")

    # Final confirmation before starting generation
    print("\n" + colored("Summary:", C_GREEN))
    print(colored(f"Target lines: {target_count}", C_CYAN))
    provided = []
    for key, val in [('a',a),('b',b),('c',c),('d',d),('e',e),('f',f),('g',g),('h',h),('i',i)]:
        if val:
            provided.append(key)
    print(colored("Groups provided (non-empty): " + ', '.join(provided), C_CYAN))
    if not confirm_yes("Proceed with generation now?"):
        print(colored("Aborted by user.", C_RED))
        sys.exit(0)

    profile = {
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'e': e,
        'f': f,
        'g': g,
        'h': h,
        'i': i,
        'j': symbols
    }

    options = {
        'export_rules': export_rules
    }

    return profile, target_count, options

# ---------------- Main ----------------
def main():
    profile, target_count, options = collect_profile()

    out_dir = os.path.join(os.path.dirname(__file__), 'wordlists')
    os.makedirs(out_dir, exist_ok=True)
    base = f"wordlist_{target_count}"
    idx = 1
    out_path = os.path.join(out_dir, f"{base}_{idx}.txt")
    while os.path.exists(out_path):
        idx += 1
        out_path = os.path.join(out_dir, f"{base}_{idx}.txt")

    print(colored(f"\nStarting generation: target_count={target_count}. Output -> {out_path}\n", C_GREEN))
    start = datetime.now()
    try:
        # pass options through to pattern.generate_and_write
        pattern.generate_and_write(profile, target_count, out_path, min_len=8, max_len=32, options=options)
    except KeyboardInterrupt:
        print(colored("\nGeneration aborted by user.", C_RED))
        sys.exit(1)
    end = datetime.now()
    elapsed = (end - start).total_seconds()

    print(colored(f"\nDone. Wrote up to {target_count} lines (stopped at target or exhausted combinations). Time: {int(elapsed)}s", C_GREEN))

    # Report rules export if requested
    if options.get('export_rules'):
        rules_path = os.path.splitext(out_path)[0] + '.rule'
        if os.path.exists(rules_path):
            print(colored(f"Rules file exported: {rules_path}", C_CYAN))
        else:
            print(colored("Rules export was requested but no rules file found.", C_YELLOW))

if __name__ == '__main__':
    main()
