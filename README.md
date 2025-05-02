<p align="center" width="100%"><img src="https://github.com/PenetrumLLC/Malcore-Playbook/blob/master/.github/assets/logos/mcpb.png?raw=true"/></p>

[![Available Recipes](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Frecipes.malcore.io%2Fassets%2Fdbs%2Frecipe-count-badge.json&query=%24.message&style=for-the-badge&label=Available%20recipes)](https://recipes.malcore.io)
[![MalScript Docs](https://img.shields.io/badge/MalScript%20Documentation-red?style=for-the-badge)](https://github.com/PenetrumLLC/Malcore-Playbook/blob/master/.github/docs/malscript_docs.md)
[![Build Recipe](https://img.shields.io/badge/Build%20A%20Recipe-blue?style=for-the-badge)](https://github.com/PenetrumLLC/Malcore-Playbook-Recipes)

Malcore Playbook is a powerful framework for automating malware analysis, malware triaging, and analyst workflows using modular recipes and scripting. Designed for SOC analysts, threat hunters, and cybersecurity professionals, Malcore Playbook allows users to build chains to automate workflows, and extract actionable intelligence from suspicious files through a simple, flexible scripting language, and individual recipes.

With its recipe system, real-time variable tracking, and conditional logic engine, Malcore Playbook transforms analyst tasks in an easily scriptable solution. Whether you're investigating advanced persistent threats (APTs), or building automated triage pipelines, Malcore Playbook gives you full control — without sacrificing speed, precision, or customization.

Key Features:

- Modular scriptable engine using "MalScript" syntax
- Analysis chaining and conditional logic
- Real-time execution tracing and output handling
- Full integration with Malcore's API
- Built for performance, flexibility, and deep analysis insights
 
## Installation

Simply run:

```shell
pip install malcore-playbook
```

Or, you can manually install like so:

```shell
git clone https://github.com/PenetrumLLC/Malcore-Playbook.git && \
  cd Malcore-Playbook && \
  python setup.py install && \
  malcore-playbook
```

## Usage

```
usage: malcore-playbook --recipe RECIPE[,RECIPE,..] --filename FILE [--chain --script [SCRIPT] 
                        --kwargs ARG1=VAL1[,ARG2=VAL2,...]]

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -r RECIPE-NAME [RECIPE-NAME ...], --recipe RECIPE-NAME [RECIPE-NAME ...]
                        Recipes to execute one at a time, pass multiple using a comma seperated list 
                        (eg, recipe1,recipe2,...)
  -c, --chain           Pass this to chain recipes together with a script, must pass the --script flag with this
  --filename FILENAME, -f FILENAME, --file-to-analyze FILENAME
                        The filename that you want to process with the recipes. This is required for the recipes to work

chain related arguments:
  --chain-script CHAIN-SCRIPT, -S CHAIN-SCRIPT, --script CHAIN-SCRIPT, -C CHAIN-SCRIPT
                        Pass either a filename or a raw chain script in order to execute the MalScript chain

recipe related arguments:
  --list-remote, --list-remote-recipes, -lR
                        List all remote recipes that are available for download
  --list-local, --list-local-recipes, -lL
                        List all local recipes that are available to execute
  --download-remote RECIPE-NAME [RECIPE-NAME ...], --download-recipe RECIPE-NAME [RECIPE-NAME ...], 
  --download RECIPE-NAME [RECIPE-NAME ...], -D RECIPE-NAME [RECIPE-NAME ...]
                        Pass a remote recipe name to download it to your recipe folder 
                        (pass 'all' to download all available recipes)
  --recipe-updates ACTION
                        Check for recipe updates
  --kwargs [KWARGS [KWARGS ...]]
                        Key and value pairs to pass to the recipe IE: arg1=var1,arg2=var2

misc arguments:
  --force               Force actions that would otherwise fail
  --output OUTPUT-TYPE, -O OUTPUT-TYPE, --output-type OUTPUT-TYPE
                        Pass to control the type of output you want, default is JSON files stored in: C:\Users\saman\.mcpb
  --hide                Hide the banner
  --version             Show version numbers and exit
```

## MalScript Overview

<p align="center" width="100%"><img height="201" width="474" src="https://github.com/PenetrumLLC/Malcore-Playbook/blob/master/.github/assets/logos/malscript_logo.png?raw=true"/></p>

MalScript is a domain-specific scripting language (DSL) built specifically for the Malcore Playbook. This language is designed to automate malware analysis and file triaging workflows. By providing the ability to chain recipes and execute them conditionally, MalScript provides a powerful declarative automation to help automate reverse engineers and analysts. MalScript combines function and imperative elements to support rule-based execution, and data inspection on real-time analysis results.

Full language documentation can be found [HERE](.github/docs/malscript_docs.md)

## Example Usage

The help menu:
![Help Menu](https://github.com/PenetrumLLC/Malcore-Playbook/blob/master/.github/assets/examples/help_menu.png?raw=true)

Executing a single recipe
![Single Recipe](https://github.com/PenetrumLLC/Malcore-Playbook/blob/master/.github/assets/examples/single-recipe.png?raw=true)

Downloading recipes:
![Download Recipes](https://github.com/PenetrumLLC/Malcore-Playbook/blob/master/.github/assets/examples/download_recipes.png?raw=true)


Executing a recipe chain and saving it to a text file:
![Download Recipes](https://github.com/PenetrumLLC/Malcore-Playbook/blob/master/.github/assets/examples/recipe_chain_saved.png?raw=true)