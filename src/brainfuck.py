from typing_extensions import Any, Generator, Never


class BrainFuckVm:
    def __init__(self, memory_size: int) -> None:
        self.memory_size: int = memory_size
        self.buffer: Generator[int, Never, Any] = byte_buffer()

    def new(self, code_str: str) -> None:
        self.code_str: str = "".join(i for i in code_str if i in ("><+-.,[]"))

        self.pc: int = 0
        self.ptr: int = 0
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
        if self.pc >= len(self.code_str):
            return False

        cmd: str = self.code_str[self.pc]

        match cmd:
            case ">":
                self.ptr_right()
            case "<":
                self.ptr_left()
            case "+":
                self.inc()
            case "-":
                self.dec()
            case ".":
                self.output()
            case ",":
                self.input_()
            case "[":
                self.jump_fwd()
            case "]":
                self.jump_back()

        self.pc += 1
        return True

    # >
    def ptr_right(self) -> None:
        self.ptr = (self.ptr + 1) % self.memory_size

    # <
    def ptr_left(self) -> None:
        self.ptr = (self.ptr - 1) % self.memory_size

    # +
    def inc(self) -> None:
        self.memory[self.ptr] = (self.memory[self.ptr] + 1) % 256

    # -
    def dec(self) -> None:
        self.memory[self.ptr] = (self.memory[self.ptr] - 1) % 256

    # .
    def output(self) -> None:
        print(chr(self.memory[self.ptr]), end="")

    # ,
    def input_(self) -> None:
        self.memory[self.ptr] = next(self.buffer)

    # [
    def jump_fwd(self) -> None:
        if self.memory[self.ptr] == 0:
            self.pc = self.bracket_map[self.pc]

    # ]
    def jump_back(self) -> None:
        if self.memory[self.ptr] != 0:
            self.pc = self.bracket_map[self.pc]

    def read_bf_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def dump_memory(self, width: int = 16) -> None:
        for i in range(0, len(self.memory), width):
            chunk: list[int] = self.memory[i : i + width]
            offset: str = f"{i:03X}"
            bytes_str: str = " ".join(f"{b:02X}" for b in chunk)

            print(f"{offset}: {bytes_str}")

    def run(self) -> None:
        while self.step():
            pass


def byte_buffer() -> Generator[int, Never, Any]:
    while True:
        user_bytes: bytes = input().encode("utf-8")
        for byte in user_bytes:
            yield byte
