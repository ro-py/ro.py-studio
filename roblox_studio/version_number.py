class VersionNumber:
    """
    Represents a Roblox deployment's version number.
    """

    def __init__(self, values: tuple):
        assert len(values) == 4, "values must be of length 4"
        self.values = tuple(map(int, values))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.values == self.values

    def __hash__(self):
        return hash(self.values)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return other.values != self.values

        return True

    def __repr__(self):
        return f"<{self.__class__.__name__} values={self.values}>"

    def __str__(self):
        return ", ".join([str(value) for value in self.values])

    def __gt__(self, other):
        return self.values > other.values

    def __ge__(self, other):
        return self.values >= other.values

    def __lt__(self, other):
        return self.values < other.values

    def __le__(self, other):
        return self.values <= other.values


if __name__ == '__main__':
    number_1 = VersionNumber((0, 488, 0, 427188))
    number_2 = VersionNumber((0, 493, 1, 4930375))

    print(f"number_1 = {number_1}")
    print(f"number_2 = {number_2}")
    print(f"number_1 == number_2: {number_1 == number_2}")
    print(f"number_1 != number_2: {number_1 != number_2}")

    print(f"number_1 > number_2: {number_1 > number_2}")
    print(f"number_1 < number_2: {number_1 < number_2}")
    print(f"number_1 >= number_2: {number_1 >= number_2}")
    print(f"number_1 <= number_2: {number_1 <= number_2}")
