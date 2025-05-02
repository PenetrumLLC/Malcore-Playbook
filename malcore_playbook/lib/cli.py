import sys
import argparse

import malcore_playbook.lib.settings as settings


logger = settings.logger


class Parser(argparse.ArgumentParser):

    """ class placeholder for the argparse item """

    @staticmethod
    def optparse():
        """ makes it easier to call from Parser().optparse() and looks nicer """
        parser = argparse.ArgumentParser()

        parser.usage = (f"malcore-playbook --recipe RECIPE[,RECIPE,..] --filename FILE "
                        "[--chain --script [SCRIPT] "
                        "--kwargs ARG1=VAL1[,ARG2=VAL2,...]]")

        required = parser.add_argument_group("required arguments")
        required.add_argument(
            "-r", "--recipe", nargs="+", metavar="RECIPE-NAME",
            help="Recipes to execute one at a time, pass multiple using a comma seperated list ("
                 "eg, recipe1,recipe2,...)",
            default=None, dest="useRecipe"
        )
        required.add_argument(
            "-c", "--chain", action="store_true",
            dest="useChain", default=False,
            help="Pass this to chain recipes together with a script, must pass the --script flag with this"
        )
        required.add_argument(
            "--filename", "-f", "--file-to-analyze", nargs=1, default=None,
            help="The filename that you want to process with the recipes. This is required for the recipes to work",
            dest="filename"
        )

        chain_flags = parser.add_argument_group("chain related arguments")
        chain_flags.add_argument(
            "--chain-script", "-s", "--script", "-C", metavar="CHAIN-SCRIPT",
            dest="chainScript", default=None,
            help="Pass either a filename or a raw chain script in order to execute the MalScript chain"
        )

        recipe_args = parser.add_argument_group("recipe related arguments")
        recipe_args.add_argument(
            "--list-remote", "--list-remote-recipes", "-lR", action="store_true", default=False,
            help="List all remote recipes that are available for download", dest="viewRemote"
        )
        recipe_args.add_argument(
            "--list-local", "--list-local-recipes", "-lL", action="store_true", default=False,
            help="List all local recipes that are available to execute", dest="viewLocal"
        )
        recipe_args.add_argument(
            "--download-remote", "--download-recipe", "--download", "-D",
            nargs="+", metavar="RECIPE-NAME", default=None,
            help="Pass a remote recipe name to download it to your recipe folder ("
                 "pass 'all' to download all available recipes"
                 ")",
            dest="downloadRecipe"
        )
        recipe_args.add_argument(
            "--search", "-S", "--search-string",
            metavar="KEYWORD", default=None,
            help="Pass a search string to filter the local or remote recipe list",
            dest="searchString"
        )
        recipe_args.add_argument(
            "--recipe-updates", "--update-recipes", "--updates", "-U",
            metavar="ACTION", help="Check for recipe updates",
            dest="checkRecipeUpdates", default=None, choices=["check", "download"]
        )
        recipe_args.add_argument(
            "--kwargs", dest="kwargs", nargs="*", default={},
            help="Key and value pairs to pass to the recipe IE: arg1=var1,arg2=var2"
        )

        misc_args = parser.add_argument_group("misc arguments")
        misc_args.add_argument(
            "--force", action="store_true", default=False,
            help="Force actions that would otherwise fail", dest="forceAction"
        )
        misc_args.add_argument(
            "--output", "-O", "--output-type",
            default="json", choices=["json", "pdf", "txt", "console"],
            metavar="OUTPUT-TYPE", dest="outputType",
            help=f"Pass to control the type of output you want, default is JSON files stored in: {settings.HOME}"
        )
        misc_args.add_argument(
            "--hide", action="store_true", help="Hide the banner", dest="hideBanner"
        )
        misc_args.add_argument(
            "--version", action="store_true", help="Show version numbers and exit",
            dest="showVersions"
        )

        # Hidden args
        parser.add_argument(
            "--no-start-end", action="store_true", default=False, dest="noStartEnd",
            help=argparse.SUPPRESS
        )
        parsed = parser.parse_args()

        # if any of these are passed we will go ahead and hide the banner and prevent the
        # startup and shutdown logging
        if parsed.viewLocal or parsed.viewRemote or parsed.showVersions:
            parsed.hideBanner = True
            parser.noStartEnd = True

        # process KEY=VAL pairs from the --kwargs argument and put them into a dict
        # for future use
        kwargs_dict = {}
        for item in parsed.kwargs:
            if "=" in item:
                key, value = item.split("=")
                kwargs_dict[key] = value
            else:
                logger.warning(f"Key value pair: {item} will be skipped")
        parsed.kwargs = kwargs_dict

        return parsed

