# @author: Wentao Mo a.k.a. Michiru
from typing import Dict, Set, Optional, List, Tuple, List
from concurrent.futures import ThreadPoolExecutor
# from itertools import filter
FILENAME = "asmData.txt"

# Validate line effectiveness
def validate(line: str) -> bool:
    line = line.split("\t")
    return len(line) >= 4

# Parse single line into a dictionary
def parseline(line: str) -> Dict:
    line = line.split("\t")
    # Merge call/jmp to function name like _flush_mmap(bool, QString, const& QString) 
    if len(line) > 8:
        line[4] = "\t".join(line[4:])
        del line[5:]
    try:
        return {
            "offset": line[0],
            "addr": line[1],
            "binary": line[2],
            "opcode": line[3],
            "operand": line[4:],
        }
    except IndexError as e:
        print(line)
        raise e

# Main Executor
def main():

    # Read file and validate
    with open(FILENAME, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines if validate(line)]

    # Parse lines
    with ThreadPoolExecutor(max_workers=12) as executor:
        lines = executor.map(parseline, lines)
    lines = list(lines)

    # 1. Operation frequency
    op_freq = {}
    for line in lines:
        op_freq[line["opcode"]] = op_freq.get(line["opcode"], 0) + 1

    print(op_freq)

    # 2. Operand count frequency
    opr_freq = {op: {} for op in op_freq}
    for line in lines:
        op, opr_count = line["opcode"], len(line["operand"])
        opr_freq[op][opr_count] = opr_freq[op].get(opr_count, 0) + 1
        
    print(opr_freq)
    for line in filter(lambda l: len(l["operand"]) >= 4, lines):
        print(line)
    

if __name__ == "__main__":
    main()