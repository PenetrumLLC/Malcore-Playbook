<p align="center" width="100%"><img src=".github/assets/logos/mcpb.png"/></p>

Malcore Playbook is a powerful framework for automating malware analysis, malware triaging, and analyst workflows using modular recipes and scripting. Designed for SOC analysts, threat hunters, and cybersecurity professionals, Malcore Playbook allows users to build chains to automate workflows, and extract actionable intelligence from suspicious files through a simple, flexible scripting language, and individual recipes.

With its recipe system, real-time variable tracking, and conditional logic engine, Malcore Playbook transforms analyst tasks in an easily scriptable solution. Whether you're investigating advanced persistent threats (APTs), or building automated triage pipelines, Malcore Playbook gives you full control — without sacrificing speed, precision, or customization.

Key Features:

- Modular scriptable engine using "MalScript" syntax
- Analysis chaining and conditional logic
- Real-time execution tracing and output handling
- Full integration with Malcore's API
- Built for performance, flexibility, and deep analysis insights

## Installation

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

## MalScript Overview

<p align="center" width="100%"><img height="201" width="474" src=".github/assets/logos/malscript_logo.png"/></p>

MalScript is a domain-specific scripting language (DSL) built specifically for the Malcore Playbook. This language is designed to automate malware analysis and automate triaging workflows. By providing the ability to chain recipes and execute them conditionally, MalScript provides a powerful declarative automation to help automate reverse engineers and analysts. MalScript combines function and imperative elements to support rule-based execution, and data inspection on real-time analysis results.

Full language documentation can be found [HERE](.github/docs/malscript_docs.md)

## Example Usage

The help menu:
![Help Menu](.github/assets/examples/help_menu.png)


Downloading recipes:
![Download Recipes](.github/assets/examples/download_recipes.png)


Executing a recipe chain and saving it to a text file:
![Download Recipes](.github/assets/examples/recipe_chain_saved.png)