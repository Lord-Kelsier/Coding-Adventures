from cgitb import reset
from CPU.cpu import CPU
from random import randint


def get_two_bytes(code):
    first_byte = code >> 8
    second_byte = code & 0xff
    return first_byte, second_byte


def get_code_with_addr(instr):
    addr = randint(0x0, 0xfff)
    code = instr + addr
    return code, addr


def get_code_formart_xkk(instr):
    x = randint(0x0, 0xf)
    value = randint(0x0, 0xff)
    code = instr + (x << 8) + value
    return code, x, value


def set_bytes_to_RAM(cpu: CPU, *bytes_arr):
    i = 0
    for b in bytes_arr:
        cpu.memory.RAM[cpu.memory.START_PROG_RAM + i]
        i += 1


def get_code_format_xy(instr, I):
    x = randint(0x0, 0xf)
    y = randint(0x0, 0xf)
    code = instr + (x << 8) + (y << 4) + I
    return code, x, y


def test_00e0(cpu: CPU) -> int:
    return 2


def test_00ee(cpu: CPU) -> int:
    return 2


def test_0nnn(cpu: CPU) -> int:
    return 2


def test_1nnn(cpu: CPU) -> int:
    code, addr = get_code_with_addr(0x1000)
    set_bytes_to_RAM(cpu, *get_two_bytes(code))
    cpu._1nnn(code)
    if cpu.register.program_counter == addr:
        return 0
    else:
        return 1


def test_2nnn(cpu: CPU) -> int:
    code, addr = get_code_with_addr(0x2000)
    set_bytes_to_RAM(cpu, *get_two_bytes(code))
    last_pc = cpu.register.program_counter
    cpu._2nnn(code)
    if last_pc == cpu.register.stack[-1] and cpu.register.program_counter == addr:
        return 0
    else:
        return 1


def test_3xkk(cpu: CPU) -> int:
    code, x, value = get_code_formart_xkk(0x3000)
    set_bytes_to_RAM(cpu, *get_two_bytes(code))
    cpu.register.all_purpuse[x] = value
    last_pc = cpu.register.program_counter
    cpu._3xkk(code)
    if cpu.register.program_counter != last_pc + 2:
        return 1
    cpu.register.program_counter -= 2
    cpu.register.all_purpuse[x] += 1
    if cpu.register.program_counter == last_pc:
        return 0
    else:
        return 1


def test_4xkk(cpu: CPU) -> int:
    return 2


def test_5xy0(cpu: CPU) -> int:
    return 2


def test_6xkk(cpu: CPU) -> int:
    return 2


def test_7xkk(cpu: CPU) -> int:
    return 2


def test_8xy0(cpu: CPU) -> int:
    return 2


def test_8xy1(cpu: CPU) -> int:
    return 2


def test_8xy2(cpu: CPU) -> int:
    return 2


def test_8xy3(cpu: CPU) -> int:
    return 2


def test_8xy4(cpu: CPU) -> int:
    return 2


def test_8xy5(cpu: CPU) -> int:
    return 2


def test_8xy6(cpu: CPU) -> int:
    return 2


def test_8xy7(cpu: CPU) -> int:
    return 2


def test_8xye(cpu: CPU) -> int:
    return 2


def test_9xy0(cpu: CPU) -> int:
    return 2


def test_annn(cpu: CPU) -> int:
    return 2


def test_bnnn(cpu: CPU) -> int:
    return 2


def test_cxkk(cpu: CPU) -> int:
    return 2


def test_dxyn(cpu: CPU) -> int:
    return 2


def test_eandf(cpu: CPU) -> int:
    return 2


funcs = [
    test_00e0,
    test_00ee,
    test_0nnn,
    test_1nnn,
    test_2nnn,
    test_3xkk,
    test_4xkk,
    test_5xy0,
    test_6xkk,
    test_7xkk,
    test_8xy0,
    test_8xy1,
    test_8xy2,
    test_8xy3,
    test_8xy4,
    test_8xy5,
    test_8xy6,
    test_8xy7,
    test_8xye,
    test_9xy0,
    test_annn,
    test_bnnn,
    test_cxkk,
    test_dxyn,
    test_eandf
]
return_codes = {
    0: "Test Completed Succesfully",
    1: "Test Failed",
    2: "Test Not Implemented"
}


def execute_unit_tests(cpu: CPU):
    cpu.initialize()
    resume = []
    for function in funcs:
        cpu.memory.reset_memory()
        cpu.register.set_registers_to_zero()
        print(f"{function.__name__}: Executing")
        code = function(cpu)
        resume.append((code, function.__name__))
        print(f"\t{return_codes[code]}")

    aproved = filter(lambda x: x[0] == 0, resume)
    not_aproved = filter(lambda x: x[0] != 0, resume)
    print("-" * 60)
    print("\t\tResume")
    print("Completed succesfully: ")
    for _, func in aproved:
        print(func, end=" | ")
    print("\n")
    print("Failed: ")
    for _, func in not_aproved:
        print(func, end=" | ")
    print()
