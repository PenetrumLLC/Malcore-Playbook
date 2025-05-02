#  Copyright (c) 2025.
#  Penetrum LLC (all rights reserved)
#  Copyright last updated: 5/2/25, 10:29 AM
#
#
#

import re

import malcore_playbook.execution.recipe_exec as recipe_exec
import malcore_playbook.lib.settings as settings


class MalScriptParserError(Exception):

    def __init__(self, msg, code, offending_line):
        self.msg = msg
        self.code = code
        self.offending_line = offending_line
        super().__init__(msg)

    def __str__(self):
        return f"[Error][{self.code}]: {self.msg}\n\t-> Code causing crash: {self.offending_line}"


class ScriptSyntaxError(MalScriptParserError): pass


class ScriptParserError(MalScriptParserError): pass


class ScriptExecutionError(MalScriptParserError): pass


class InvalidScriptPassed(FileNotFoundError): pass


class MalScriptInterpreter(object):

    """ basic interpreter for the MalScript scripting language """

    def __init__(self, filename, **kwargs):
        self.variables = {}
        self.filename = filename
        self.kwargs = kwargs
        self.matcher = re.compile(r"if (.+?) in (.+?) then (.+)")
        self.version = "1.0"

    def exec_command(self, command, line_no, line):
        """ executes the exec() built in """
        settings.logger.info(f"Executing command: {command} on filename: {self.filename}")
        recipe = recipe_exec.load_recipe([command], load_one=True)
        if recipe is None:
            raise ScriptExecutionError(
                f"Failed to execute requested recipe: {command}, lino_no: {line_no}", -3, line
            )
        exec_results = recipe_exec.execute_recipe(recipe, self.filename, **self.kwargs)
        return exec_results

    def parse_value(self, value, line_no, line):
        """ parses and adds the variables to the storage dict """
        value = value.strip()
        type_, value = value.split("(")
        value = value.split(")")[0]
        if type_.lower() == "str":
            return value
        elif type_.lower() == "int":
            value = value.replace('"', "").replace("'", "")
            if not isinstance(value, int):
                return int(value)
            else:
                return value
        elif type_.lower() == "exec":
            command = value
            return self.exec_command(command, line_no, line)
        else:
            raise ScriptSyntaxError(
                f"Unsupported value type: {value}, line_no: {line_no}", -2, line
            )

    def get_nested_variables(self, var_name, condition_value, then_part, line_no, line, **kwargs):
        """ find nested variables data from the script """
        is_from_ret = kwargs.get("is_from_ret", False)

        if not is_from_ret:
            parts = var_name.split(".")
            var_name = parts[0]
            if var_name not in self.variables:
                raise ScriptParserError(
                    f"Requested variable: {var_name} not found, line_no: {line_no}", -1, line
                )
            data = self.variables[var_name]
            keys = parts[1:]
            for key in keys:
                if key.startswith("["):
                    try:
                        index_number = int(key.split("[")[1].split("]")[0])
                        data = data[index_number]
                    except:
                        raise ScriptSyntaxError(
                            f"Invalid index for variable: {var_name}, line_no: {line_no}", -2, line
                        )
                else:
                    if key in data.keys():
                        data = data.get(key)
                    else:
                        raise ScriptSyntaxError(
                            f"Invalid variable: {var_name}, line_no: {line_no}", -2, line
                        )
            var_value = data
            if isinstance(var_value, list):
                if any(condition_value == item for item in var_value):
                    self.parse_value(then_part, line_no, line)
            else:
                if isinstance(condition_value, int):
                    if condition_value == var_value:
                        self.parse_line(then_part, line_no)
                else:
                    if condition_value in str(var_value):
                        self.parse_line(then_part, line_no)
        else:
            parts = var_name.split(".")
            var_name = parts[0]
            keys = parts[1:]
            data = self.variables[var_name]
            for key in keys:
                if key.startswith("["):
                    try:
                        index_number = int(key.split("[")[1].split("]")[0])
                        data = data[index_number]
                    except:
                        raise ScriptSyntaxError(
                            f"Invalid index for variable: {var_name}, line_no: {line_no}", -2, line
                        )
                else:
                    if key in data.keys():
                        data = data.get(key)
                    else:
                        raise ScriptSyntaxError(
                            f"Invalid variable: {var_name}, line_no: {line_no}", -2, line
                        )
            return data

    def parse_line(self, line, line_no):
        """ parses the lines of the script """
        line_no = str(line_no)
        line = line.strip()
        if line.startswith('$') and '=' in line:
            settings.logger.debug(f"Found variable in script, parsing variable, line_no: {line_no}")
            var_name, value = line.split('=', 1)
            var_name = var_name.strip()
            value = value.strip().rstrip(';')
            if var_name in self.variables:
                settings.logger.debug(f"Variable already exists from line_no: {line_no}, overwriting")
                del self.variables[var_name]
            self.variables[var_name] = self.parse_value(value, line_no, line)

        elif line.startswith("#"):
            settings.logger.debug(f"Found a commented line on line_no: {line_no}, skipping")

        elif line.startswith('if '):
            settings.logger.debug(f"Found conditional if statement on line_no: {line_no}, parsing condition")
            match = self.matcher.match(line)
            if match:
                settings.logger.debug(f"Condition is acceptable, starting execution")
                condition_value, var_name, then_part = match.groups()
                condition_value = self.parse_value(condition_value, line_no, line)
                if isinstance(condition_value, str):
                    condition_value = condition_value.replace("'", "").replace('"', "")
                var_name = var_name.strip()
                if var_name.startswith('$'):
                    var_name = var_name
                else:
                    var_name = '$' + var_name
                then_part = then_part.strip()
                if "." in var_name:
                    self.get_nested_variables(var_name, condition_value, then_part, line_no, line)
                else:
                    if var_name not in self.variables:
                        raise ScriptParserError(
                            f"Requested variable: {var_name} not found, line_no: {line_no}", -1, line
                        )
                    var_value = self.variables[var_name]
                    if isinstance(var_value, list):
                        if any(condition_value == item for item in var_value):
                            self.parse_line(then_part, line_no)
                    else:
                        if condition_value in str(var_value):
                            self.parse_line(then_part, line_no)

        elif line.startswith('ret'):
            settings.logger.debug(f"Found return statement on line_no: {line_no}, parsing return")
            var_name = line.split("(")[1].split(")")[0].strip()
            if var_name.startswith('$'):
                var_name = var_name
            else:
                var_name = '$' + var_name
            if "." in var_name:
                return self.get_nested_variables(
                    var_name, None, None, line_no, line, is_from_ret=True
                )
            else:
                if var_name in self.variables:
                    return self.variables[var_name]
                else:
                    raise ScriptParserError(
                        f"Variable {var_name} not found, line_no: {line_no}", -1, line
                    )

        else:
            raise ScriptSyntaxError(
                f"Unknown line format: {line}, line_no: {line_no}", -2, line
            )

    def start_execution(self, script):
        """ starts execution of the script """
        settings.logger.debug(f"Starting execution of passed script")
        lines = script.strip().split(';')
        settings.logger.debug(f"Total of {len(lines)} line(s) to parse in script")
        result = None
        for i, line in enumerate(lines, start=1):
            if line != '':
                out = self.parse_line(line, i)
                if out is not None:
                    result = out
        return result


def run(script, filename, kwargs):
    """ pointer function to start the entire process """
    if kwargs is None:
        kwargs = {}
    engine = MalScriptInterpreter(filename, **kwargs)
    result = engine.start_execution(script)
    return result
