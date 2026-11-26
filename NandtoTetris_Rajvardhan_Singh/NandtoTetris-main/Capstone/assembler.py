import sys
import os

COMP_TABLE = {
    "0":   "0101010", "1":   "0111111", "-1":  "0111010",
    "D":   "0001100", "A":   "0110000", "!D":  "0001101",
    "!A":  "0110001", "-D":  "0001111", "-A":  "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M":   "1110000", "!M":  "1110001", "-M":  "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101"
}

DEST_TABLE = {
    "":    "000", "M":   "001", "D":   "010", "MD":  "011",
    "A":   "100", "AM":  "101", "AD":  "110", "AMD": "111"
}

JUMP_TABLE = {
    "":    "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def clean_line(line):
    # Remove comments and whitespace
    if "//" in line:
        line = line.split("//")[0]
    return line.strip()

def assemble(asm_path):
    # Initialize predefined symbols
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }
    for i in range(16):
        symbols[f"R{i}"] = i

    user_labels = {}
    user_variables = {}

    with open(asm_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # PASS 1: Collect labels and build clean instruction list
    instructions = []
    rom_address = 0
    for line in raw_lines:
        cleaned = clean_line(line)
        if not cleaned:
            continue
        if cleaned.startswith("(") and cleaned.endswith(")"):
            label = cleaned[1:-1].strip()
            symbols[label] = rom_address
            user_labels[label] = rom_address
        else:
            instructions.append(cleaned)
            rom_address += 1

    # PASS 2: Translate instructions to 16-bit binary
    next_ram_address = 16
    binary_lines = []

    for inst in instructions:
        if inst.startswith("@"):
            # A-instruction
            symbol = inst[1:].strip()
            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_ram_address
                    user_variables[symbol] = next_ram_address
                    next_ram_address += 1
                address = symbols[symbol]
            binary_lines.append(f"0{address:015b}")
        else:
            # C-instruction: dest=comp;jump
            dest, comp, jump = "", inst, ""
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)

            dest = dest.strip()
            comp = comp.strip()
            jump = jump.strip()

            c_bits = COMP_TABLE[comp]
            d_bits = DEST_TABLE[dest]
            j_bits = JUMP_TABLE[jump]
            binary_lines.append(f"111{c_bits}{d_bits}{j_bits}")

    # Write output .hack file
    hack_path = os.path.splitext(asm_path)[0] + ".hack"
    with open(hack_path, "w", encoding="utf-8") as f:
        f.write("\n".join(binary_lines) + "\n")

    # Extra Feature for K = 27 (27 mod 3 == 0): Save labels and variables to symbols.txt
    symbols_path = os.path.join(os.path.dirname(os.path.abspath(asm_path)), "symbols.txt")
    with open(symbols_path, "w", encoding="utf-8") as f:
        f.write("=== LABELS (ROM Addresses) ===\n")
        for lbl, addr in user_labels.items():
            f.write(f"{lbl}: {addr}\n")
        f.write("\n=== VARIABLES (RAM Addresses) ===\n")
        for var, addr in user_variables.items():
            f.write(f"{var}: {addr}\n")

    print(f"Successfully assembled '{asm_path}' -> '{hack_path}'")
    print(f"Saved symbols to '{symbols_path}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <Program.asm>")
        sys.exit(1)
    assemble(sys.argv[1])