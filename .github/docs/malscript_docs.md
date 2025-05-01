Language type breakdown:

| Feature                 | Classification                                                            |
|-------------------------|---------------------------------------------------------------------------|
| Purpose-built           | DSL tailored for analysis, workflow automation, and automatic triaging    |
| Imperative flow control | Condition logic resembles traditional scripting                           |
| Declarative intent      | Each line is designed to express what to do based on prior outputs        | 
| Functional style        | Uses built-in functions with little not no side effects or mutable states | 
| Minimal syntax          | Provides a compact and expressive styling                                 |
| Dot-path dereferencing  | Provides the ability to access JSON-like objects with `.`                 |

### Built ins

- `$`
  - Use this to set a variable for future use: `$emu`
- `=`
  - Use in conjunction with the variable set to set the variable to the action: `$emu=ACTION`
- `str()`
  - Use to set a string for searching in condition statements: `str('exe')`
- `int()`
  - Use to set an integer for searching in condition statements: `int(182)`
- `exec()`
  - Use to perform execution of a downloaded recipe, must be used with variable setting: `$emu=exec(dynamic-analysis)`
- `if`
  - Use to perform a condition statement: `if str('exe')`
- `ret`
  - Use to return a value from the script execution: `ret($emu)`
- `.`
  - Use to access data within a variable: `$emu.data.[1]`
- `;`
  - Use to end a line, must be at the end of every line: `$emu=exec(dynamic-analysis);`

### Setting and Accessing Variables

To set a variable in MalScript you will need declare the variable and set it to an action, for example: `$emu=exec(dynamic-analysis);` will set the variable `$emu` to the output of the `dynamic-analysis` recipe. You will then be able to access the output from the recipe by calling the set variable.

Since the recipes are based off a RESTful API on the Malcore website you are also able to access variables and list indexes within the output by chaining it with `.` (periods) to the location of the required data. For example if we have the following assigned to variable `$results`:

```json
{
  "results": {
    "test1": [
      {"test2": "results"}
    ]
  }
}
```

We can access the `results` variable by chaining the location together: `$results.results.test1.[0].test2` will give us the string `"results"`.

### Executing Recipes and Assigning them to Variables

The `exec()` built in allows you to execute a recipe. For example: `$exifData=exec(exif-data);`. To break this down:

```
$VAR_NAME     # set the variable name
=             # Assign the variable
exec(         # Execute a recipe
RECIPE-NAME   # Execute this recipe name
)             # Close the brackets
;             # End the line
```

### Example Script

```malscript
# This is a comment that must also end with: ;
# Will will set the variable $s to the output of executing the strings recipe ;
$s=exec(strings);
# If we find a string matching GetCurrentProcess in the strings output ;
# We execute the threat-score recipe and assign the output to variable $t ;
if str('GetCurrentProcess') in $s then $t=exec(threat-score);
# We can access the exact score variable by using derreferencing with . ;
# If 5.13 is in the JSON key score we will execute the AI classifier recipe ;
if str('5.13') in $t.score then $a=exec(ai-class);
# If the string safe is in the AI classifier output ;
# We will execute the exif-data recipe and assign output to variable $e ;
if str('safe') in $a then $e=exec(exif-data);
# Then we will return the code_signature JSON variable from the exif-data output ;
ret($e.code_signature);
```