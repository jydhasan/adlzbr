# # Example input strings
# input_string1 = "Hello"
# input_string2 = "hElLo"

# # Convert both strings to lowercase and then perform the comparison
# if input_string1.lower() == input_string2.lower():
#     print("The strings are equal (case-insensitive).")
# else:
#     print("The strings are not equal (case-insensitive).")
def to_camel_case(input_string):
    words = input_string.strip().split()
    camel_case_string = words[0].lower(
    ) + ''.join(word.capitalize() for word in words[1:])
    return camel_case_string


# Example usage:
input_string = "hello world how are you"
camel_case_output = to_camel_case(input_string)
print(camel_case_output)  # Output: "helloWorldHowAreYou"
