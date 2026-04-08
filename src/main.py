import sys

from brainfuck import BrainFuckVm


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <path/to/file.bf>")
        exit(1)

    path: str = sys.argv[1]

    bf: BrainFuckVm = BrainFuckVm(256)

    code: str = bf.read_bf_file(path)
    bf.new(code)
    bf.run()

    print()
    print(f"\nMEM SIZE: {bf.memory_size}")
    print("MEM DUMP:")
    bf.dump_memory()


if __name__ == "__main__":
    main()
