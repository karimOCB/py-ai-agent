from functions.get_file_content import get_file_content

result1 = get_file_content("calculator", "main.py")
result2 = get_file_content("calculator", "pkg/calculator.py")
result3 = get_file_content("calculator", "/bin/cat")
result4 = get_file_content("calculator", "pkg/does_not_exist.py") 

print(f'''
    {result1}
    {result2}
    {result3}
    {result4}
''')