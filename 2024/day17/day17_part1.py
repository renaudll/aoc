from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class Computer:
    register_a: int = 0
    register_b: int = 0
    register_c: int = 0
    instructions: list[int] = field(default_factory=list)
    instruction_pointer: int = 0
    output: list[int] = field(default_factory=list)

    def _compute_combo_operand(self, operand: int):
        if operand < 4:
            return operand
        if operand == 4:
            return self.register_a
        if operand == 5:
            return self.register_b
        if operand == 6:
            return self.register_c
        raise ValueError(f"Invalid operand: {operand}")

    def adv(self, operand: int):
        """
        The adv instruction (opcode 0) performs division.
        The numerator is the value in the A register.
        The denominator is found by raising 2 to the power of the instruction's combo operand.
        (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        The result of the division operation is truncated to an integer and then written to the A register.
        """
        operand = self._compute_combo_operand(operand)
        numerator = self.register_a
        denominator = 2 ** operand
        result = numerator // denominator
        self.register_a = result

    def bdv(self, operand: int):
        """
        The bdv instruction (opcode 6) works exactly like the adv instruction
        except that the result is stored in the B register.
        (The numerator is still read from the A register.)
        """
        operand = self._compute_combo_operand(operand)
        numerator = self.register_a
        denominator = 2 ** operand
        result = int(numerator / denominator)
        self.register_b = result

    def cdv(self, operand: int):
        """
        The cdv instruction (opcode 7) works exactly like the adv instruction
        except that the result is stored in the C register.
        (The numerator is
         still read from the A register.)
        """
        operand = self._compute_combo_operand(operand)
        numerator = self.register_a
        denominator = 2 ** operand
        result = int(numerator / denominator)
        self.register_c = result

    def bxl(self, operand: int):
        """
        The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand,
        then stores the result in register B.
        """
        result = self.register_b ^ operand
        self.register_b = result

    def bst(self, operand: int):
        """
        The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
        (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        """
        operand = self._compute_combo_operand(operand)
        result = operand % 8
        self.register_b = result

    def jnz(self, operand: int):
        """
        The jnz instruction (opcode 3) does nothing if the A register is 0.
        However, if the A register is not zero,
        it jumps by setting the instruction pointer to the value of its literal operand;
        if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
        """
        if self.register_a == 0:
            return
        self.instruction_pointer = operand - 2  # compensate for the instruction pointer increasing by two

    def bxc(self, operand: int):
        """
        The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C,
        then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        result = self.register_b ^ self.register_c
        self.register_b = result

    def out(self, operand: int):
        """
        The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
        (If a program outputs multiple values, they are separated by commas.)
        """
        operand = self._compute_combo_operand(operand)
        result = operand % 8
        self.output.append(result)

    def debug(self):
        print(f"Register A: {self.register_a}")
        print(f"Register B: {self.register_b}")
        print(f"Register C: {self.register_c}")
        print(f"Instruction Pointer: {self.instruction_pointer}")

    def run(self):
        FUNC_BY_OP_CODE = [
            self.adv,  # 0
            self.bxl,  # 1
            self.bst,  # 2
            self.jnz,  # 3
            self.bxc,  # 4
            self.out,  # 5
            self.bdv,  # 6
            self.cdv,  # 7
        ]

        num_instructions = len(self.instructions)
        while self.instruction_pointer < num_instructions:
            instruction = FUNC_BY_OP_CODE[self.instructions[self.instruction_pointer]]
            operand = self.instructions[self.instruction_pointer+1]
            # print(f"Executing {instruction.__name__} with {operand}")
            instruction(operand)
            self.instruction_pointer += 2
            #self.debug()
        return self

    def get_output(self) -> str:
        return ",".join(str(number) for number in self.output)


def test():
    # If register C contains 9, the program 2,6 would set register B to 1.
    actual = Computer(register_c=9, instructions=[2, 6]).run()
    assert actual.register_b == 1

    # If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    actual = Computer(register_a=10, instructions=[5, 0, 5, 1, 5, 4]).run()
    assert actual.get_output() == "0,1,2"

    # If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    actual = Computer(register_a=2024, instructions=[0, 1, 5, 4, 3, 0]).run()
    assert actual.get_output() == "4,2,5,6,7,7,7,7,3,1,0"
    assert actual.register_a == 0

    # If register B contains 29, the program 1,7 would set register B to 26.
    actual = Computer(register_b=29, instructions=[1, 7]).run()
    assert actual.register_b == 26

    # If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    actual = Computer(register_b=2024, register_c=43690, instructions=[4, 0]).run()
    assert actual.register_b == 44354

    actual = Computer(register_a=729, instructions=[0, 1, 5, 4, 3, 0]).run()
    assert actual.get_output() == "4,6,3,5,6,3,5,2,1,0"


def parse() -> Computer:
    register_a_str, register_b_str, register_c_str, _, instructions_str = Path("input.txt").read_text(
        encoding="utf-8").split("\n")
    register_a = int(register_a_str.split(":")[1])
    register_b = int(register_b_str.split(":")[1])
    register_c = int(register_c_str.split(":")[1])
    instructions = [int(number_str) for number_str in instructions_str.split(":")[1].split(",")]
    return Computer(register_a, register_b, register_c, instructions)


test()

real_computer = parse()
print(real_computer.run().get_output())


# 0,4,4,4,0,0,0,0,0 = incorrect
# 5,3,2,1,3,3,5,6,0 = incorrect
# 7,3,5,7,5,7,4,3,0 = correct!
