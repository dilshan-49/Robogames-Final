from collections import Counter

def most_repeated(arr):
    counter = Counter(arr)
    return max(counter, key=counter.get)

# Example usage
print(most_repeated(["apple", "banana", "apple", "orange"]))  # Output: "apple"
