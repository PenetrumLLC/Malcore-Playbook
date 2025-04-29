import argparse

import malcore_playbook.lib.settings as settings


logger = settings.logger


class Parser(argparse.ArgumentParser):

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-r", "--recipe", nargs="+", metavar="RECIPE-NAME",
            help="Pass a recipe name to begin the recipe execution, pass multiple with commas IE: recipe1,recipe2,...",
            default=None, dest="useRecipe"
        )
        parser.add_argument(
            "-c", "--chain", action="store_true",
            dest="useChain", default=False,
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            "--chain-script", "-S", "--script", "-C", metavar="CHAIN-SCRIPT",
            dest="chainScript", default=None,
            help="Pass either a filename or a chain script"
        )
        parser.add_argument(
            "--list-remote", "--list-remote-recipes", "-lR", action="store_true", default=False,
            help="List all remote recipes that are available for download", dest="viewRemote"
        )
        parser.add_argument(
            "--list-local", "--list-local-recipes", "-lL", action="store_true", default=False,
            help="List all local recipes that are available to execute", dest="viewLocal"
        )
        parser.add_argument(
            "--download-remote", "--download-recipe", "--download", "-D",
            nargs="+", metavar="RECIPE-NAME", default=None,
            help="Pass a remote recipe name to download it to your recipe folder ("
                 "pass 'all' to download all available recipes"
                 ")",
            dest="downloadRecipe"
        )
        parser.add_argument(
            "--force", action="store_true", default=False,
            help="Force actions that would otherwise fail", dest="forceAction"
        )
        parser.add_argument(
            "--output", "-O", "--output-type",
            default="json", choices=["json", "pdf", "txt", "console"],
            metavar="OUTPUT-TYPE", dest="outputType",
            help=f"Pass to control the type of output you want, default is JSON files stored in: {settings.HOME}"
        )
        parser.add_argument(
            "--filename", "-f", "--file-to-analyze", nargs=1, default=None,
            help="Filename for the recipes to process", dest="filename"
        )
        parser.add_argument(
            "--kwargs", dest="kwargs", nargs="*", default={},
            help="Key and value pairs to pass to the recipe IE: arg1=var1,arg2=var2"
        )
        parser.add_argument(
            "--hide", action="store_true", help="Hide the banner"
        )
        parsed = parser.parse_args()

        kwargs_dict = {}
        for item in parsed.kwargs:
            if "=" in item:
                key, value = item.split("=")
                kwargs_dict[key] = value
            else:
                logger.warning(f"Key value pair: {item} will be skipped")
        parsed.kwargs = kwargs_dict

        return parsed

