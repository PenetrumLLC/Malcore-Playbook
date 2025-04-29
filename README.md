<p align="center" width="100%"><img src=".github/assets/logos/mcpb.png"/></p>

Malcore Playbook is a powerful framework for automating malware analysis, malware triaging, and analyst workflows using modular recipes and scripting. Designed for reverse engineers, threat hunters, and cybersecurity professionals, Playbook allows users to build chains to automate workflows, and extract actionable intelligence from suspicious files through a simple, flexible scripting language, and individual recipes.

With its recipe system, real-time variable tracking, and conditional logic engine, Malcore Playbook transforms analyst tasks in an easily scriptable solution. Whether you're investigating advanced persistent threats (APTs), or building automated triage pipelines, Malcore Playbook gives you full control — without sacrificing speed, precision, or customization.

Key Features:

- Modular scriptable engine using "MalScript" syntax
- Analysis chaining and conditional logic
- Real-time execution tracing and output handling
- Full integration with Malcore's API
- Built for performance, flexibility, and deep analysis insights

Malcore Playbook: Automate the Hunt. Understand the Enemy.

#### Installation

For now, you will have to perform a manual installation like so:

```shell
git clone https://github.com/PenetrumLLC/Malcore-Playbook.git && \
  cd Malcore-Playbook && \
  python setup.py install && \
  malcore-playbook
```

## Usage

```
usage: malcore-playbook [-h] [-r RECIPE-NAME [RECIPE-NAME ...]] [--chain-script CHAIN-SCRIPT] [--list-remote] [--list-local] 
                        [--download-remote RECIPE-NAME [RECIPE-NAME ...]] [--force] [--output OUTPUT-TYPE]
                        [--filename FILENAME] [--kwargs [KWARGS [KWARGS ...]]] [--hide]

optional arguments:
  -h, --help            show this help message and exit
  -r RECIPE-NAME [RECIPE-NAME ...], --recipe RECIPE-NAME [RECIPE-NAME ...]
                        Pass a recipe name to begin the recipe execution, pass multiple with commas IE: recipe1,recipe2,...
  --chain-script CHAIN-SCRIPT, -S CHAIN-SCRIPT, --script CHAIN-SCRIPT, -C CHAIN-SCRIPT
                        Pass either a filename or a chain script
  --list-remote, --list-remote-recipes, -lR
                        List all remote recipes that are available for download
  --list-local, --list-local-recipes, -lL
                        List all local recipes that are available to execute
  --download-remote RECIPE-NAME [RECIPE-NAME ...], --download-recipe RECIPE-NAME [RECIPE-NAME ...], 
                                                   --download RECIPE-NAME [RECIPE-NAME ...], -D RECIPE-NAME [RECIPE-NAME ...]
                        Pass a remote recipe name to download it to your recipe folder (pass 'all' to download all available recipes)
  --force               Force actions that would otherwise fail
  --output OUTPUT-TYPE, -O OUTPUT-TYPE, --output-type OUTPUT-TYPE
                        Pass to control the type of output you want, default is JSON files stored in: C:\Users\saman\.mcpb
  --filename FILENAME, -f FILENAME, --file-to-analyze FILENAME
                        Filename for the recipes to process
  --kwargs [KWARGS [KWARGS ...]]
                        Key and value pairs to pass to the recipe IE: arg1=var1,arg2=var2
  --hide                Hide the banner

```

## MalScript

MalScript is a scripting engine built specifically for the Malcore Playbook that allows users the ability to automate workflows. By chaining recipes together and executing recipes by condition MalScript provides a powerful workflow automation tool.

### Built ins

- `!`
  - Use this to set a variable for future use: `!emu`
- `=`
  - Use in conjunction with the variable set to set the variable to the action: `!emu=ACTION`
- `str()`
  - Use to set a string for searching in condition statements: `str('exe')`
- `int()`
  - Use to set an integer for searching in condition statements: `int(182)`
- `exec()`
  - Use to perform execution of a downloaded recipe, must be used with variable setting: `!emu=exec(dynamic-analysis)`
- `if`
  - Use to perform a condition statement: `if str('exe')`
- `ret`
  - Use to return a value from the script execution: `ret(!emu)`
- `.`
  - Use to access data within a variable: `!emu.data.[1]`
- ';'
  - Use to end a line, must be at the end of every line: `!emu=exec(dynamic-analysis);`

### Setting and Accessing Variables

To set a variable in MalScript you will need declare the variable and set it to an action, for example: `!emu=exec(dynamic-analysis);` will set the variable `!emu` to the output of the `dynamic-analysis` recipe. You will then be able to access the output from the recipe by calling the set variable.

Since the recipes are based off a RESTful API on the Malcore website you are also able to access variables and list indexes within the output by chaining it with `.` (periods) to the location of the required data. For example if we have the following assigned to variable `!results`:

```json
{
  "results": {
    "test1": [
      {"test2": "results"}
    ]
  }
}
```

We can access the `results` variable by chaining the location together: `!results.results.test1.[0].test2` will give us the string `"results"`.

### Executing Recipes and Assigning them to Variables

The `exec()` built in allows you to execute a recipe. For example: `!exifData=exec(exif-data);`. To break this down:

```
!VAR_NAME     # set the variable name
=             # Assign the variable
exec(         # Execute a recipe
RECIPE-NAME   # Execute this recipe name
)             # Close the brackets
;             # End the line
```

### Example Script

```malscript
!emu=exec(dynamic-emulation);
if int(182) in !emu.[0].entry_points.[0].instr_count then !exif=exec(exif-data);
if str('exe') in !exif then !str=exec(strings);
ret(!str.[0]);
```