def loadWords() -> list[str]:
    with open('words.txt', 'r') as file:
        return file.read().splitlines()
