# Create a list of numbers from 1 to 10
numbers = list(range(1, 11))

# Find even numbers using list comprehension
even_numbers = [num for num in numbers if num % 2 == 0]

# Print the results
print("Even numbers from 1 to 10:")
print(even_numbers)

# Alternative: print each number on a separate line
print("\nEven numbers (one per line):")
for num in even_numbers:
    print(num)