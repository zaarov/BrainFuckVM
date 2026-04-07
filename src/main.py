from typing_extensions import Any, Generator, Never


class VirtualMachine:
    def __init__(self, memory_size: int) -> None:
        self.memory_size: int = memory_size
        self.buffer: Generator[int, Never, Any] = byte_buffer()

    def load(self, code_str: str) -> None:
        self.code_str: str = "".join(i for i in code_str if i in ("><+-.,[]"))

        self.program_counter: int = 0
        self.memory_pointer: int = 0
        self.memory: list[int] = [0] * self.memory_size

        stack: list[Any] = []
        self.bracket_map: dict[Any, Any] = {}

        for i, c in enumerate(self.code_str):
            if c == "[":
                stack.append(i)
            elif c == "]":
                if not stack:
                    print("error")
                    exit(1)
                start: Any = stack.pop()
                self.bracket_map[start] = i
                self.bracket_map[i] = start
        if stack:
            print("error")
            exit(1)

    def step(self) -> bool:
        if self.program_counter >= len(self.code_str):
            return False

        cmd: str = self.code_str[self.program_counter]

        match cmd:
            case ">":
                self.memory_pointer = (self.memory_pointer + 1) % self.memory_size
            case "<":
                self.memory_pointer = (self.memory_pointer - 1) % self.memory_size
            case "+":
                self.memory[self.memory_pointer] = (
                    self.memory[self.memory_pointer] + 1
                ) % 256
            case "-":
                self.memory[self.memory_pointer] = (
                    self.memory[self.memory_pointer] - 1
                ) % 256
            case ".":
                print(chr(self.memory[self.memory_pointer]), end="")
            case ",":
                self.memory[self.memory_pointer] = next(self.buffer)
            case "[":
                if self.memory[self.memory_pointer] == 0:
                    self.program_counter = self.bracket_map[self.program_counter]
            case "]":
                if self.memory[self.memory_pointer] != 0:
                    self.program_counter = self.bracket_map[self.program_counter]

        self.program_counter += 1
        return True

    def run(self) -> None:
        while self.step():
            pass


def byte_buffer() -> Generator[int, Never, Any]:
    while True:
        user_bytes: bytes = input().encode("utf-8")
        for byte in user_bytes:
            yield byte


def main() -> None:
    code: str = ">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
    print(f"CODE: {code}")
    bf: VirtualMachine = VirtualMachine(256)
    bf.load(code)
    bf.run()
    print("DEBUG:")
    print(f"{bf.memory, bf.memory_pointer, bf.program_counter}")


if __name__ == "__main__":
    main()
