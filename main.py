from typing import List, Tuple
import sys


def CFG_to_PDA(gram: List[Tuple[str, List[str]]], nonterm_states: List[str], term_states: List[str],
               start_state: str) -> None:
    print("Grammar given as input:")
    print(f"Start State: {start_state}")
    print("Non Terminal States: ")
    print(*nonterm_states, sep=" ")
    print("Terminal States: ")
    print(*term_states, sep=" ")
    print("Production Rule: ")
    for rule in gram:
        state, productions = rule
        print(f"{state} -> {productions[0]}", end="")
        for i in range(1, len(productions)):
            print(f" | {productions[i]}", end="")
        print()
    print("-" * 73)

    print("\nCorresponding PDA: ")
    for rule in gram:
        state, productions = rule
        print(f"δ(q, ε, {state}) = {{ (q, {productions[0]})", end="")
        for i in range(1, len(productions)):
            print(f", (q, {productions[i]})", end="")
        print(" }")
    print()
    for term in term_states:
        print(f"δ(q, {term}, {term}) = (q, ε)")


if __name__ == "__main__":
    gram = []
    nonterm_states = []
    term_states = []

    start_state = ""
    with open("cfg.txt") as fin:
        for line in fin:
            line = line.strip()
            if line.startswith("NT"):
                nonterm_states = line.split()[1:]
                start_state = nonterm_states[0]
            elif line.startswith("T"):
                term_states = line.split()[1:]
            else:
                state, productions = line.split(maxsplit=1)
                productions = productions.split("|")
                productions = [p.strip() for p in productions]
                gram.append((state, productions))

    CFG_to_PDA(gram, nonterm_states, term_states, start_state)