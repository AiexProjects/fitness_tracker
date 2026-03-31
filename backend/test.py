data = {
    'present_key': [1, 2, 3],
    'another_key': 'value'
}

# Example 1: Key exists, returns the associated value (a list)
value1 = data.get('present_key', [])
print(f"'present_key' value: {value1}")

# Example 2: Key does not exist, returns the specified default value ([])
value2 = data.get('missing_key', [])
print(f"'missing_key' value: {value2}")
