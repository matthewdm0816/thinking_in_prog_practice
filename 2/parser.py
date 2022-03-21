# @author: Wentao Mo a.k.a. Michiru
from typing import Dict, Set, Optional, List, Tuple, List
from concurrent.futures import ThreadPoolExecutor
from icecream import ic
import csv 

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
        ic(line)
        raise e

def writeCSV(filename: str, data: List[Tuple], headers: Optional[List[str]] = None):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if headers:
            writer.writerow(headers)
        writer.writerows(data)

OPR_COUNT_TO_NAME = {
    0: "无",
    1: "单",
    2: "双",
    3: "三",
    4: "四",
}

OPR_COUNT_TO_NAME = {
    i: name+'参指令' for i, name in OPR_COUNT_TO_NAME.items()
}

# Main Executor
def main():
    ic(OPR_COUNT_TO_NAME)

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

    ic(op_freq)

    # 2. Operand count frequency
    opr_freq = {op: {} for op in op_freq}
    for line in lines:
        op, opr_count = line["opcode"], len(line["operand"])
        opr_freq[op][opr_count] = opr_freq[op].get(opr_count, 0) + 1
        
    ic(opr_freq)
    for line in filter(lambda l: len(l["operand"]) >= 4, lines):
        ic(line)
    
    # 3. Transform into CSV like data for Excel
    # Opr_count - Opr_freq
    opr_freq_data = [
        (op, amount) for op, amount in op_freq.items()
    ]
    ic(opr_freq_data)
    writeCSV(filename="opr_freq_1.csv", data=opr_freq_data, headers=["指令", "频次"])

    # Opr_count - Opr_freq
    opr_freq_2 = {}
    for op, opr_data in opr_freq.items():
        for opr_count, amount in opr_data.items():
            opr_freq_2[opr_count] = opr_freq_2.get(opr_count, 0) + amount

    opr_freq_data2 = [
        (OPR_COUNT_TO_NAME[opr_count], amount) for opr_count, amount in opr_freq_2.items()
    ]
    ic(opr_freq_data2)
    writeCSV(filename="opr_freq_2.csv", data=opr_freq_data2, headers=["类别", "频次"])

    # Opr - Opr_count - Opr_freq
    opr_freq_data3 = [
        (op, amount, OPR_COUNT_TO_NAME[opr_count]) 
        for op, op_data in opr_freq.items() 
        for opr_count, amount in op_data.items()
        
    ]
    opr_freq_data3 = sorted(opr_freq_data3, key=lambda x: x[1], reverse=True)
    ic(len(opr_freq_data3), opr_freq_data3)
    writeCSV(filename="opr_freq_3.csv", data=opr_freq_data3, headers=["指令", "频次", "类别"])
    

if __name__ == "__main__":
    main()