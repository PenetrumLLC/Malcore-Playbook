import os
import sys
import datetime
import logging

import malcore_playbook.lib.cli as cli
import malcore_playbook.lib.settings as settings
import malcore_playbook.lib.api as api
import malcore_playbook.execution.recipe_exec as recipe_exec


logger = settings.logger


def main():
    try:
        if "FORCE-RELOG" in sys.argv:
            force = True
        else:
            force = False
        settings.init(force=force)
        parser = cli.Parser().optparse()

        if not parser.hideBanner:
            print(settings.HEADER)
        if parser.noStartEnd:
            logger.info(f"Starting up at: {datetime.datetime.now()}")
        if parser.viewRemote:
            _api = api.Api(only_remote=True)
            settings.display_recipes(_api.list_recipes())
        elif parser.viewLocal:
            files = [f"{settings.RECIPE_HOME}{os.path.sep}{f}" for f in os.listdir(settings.RECIPE_HOME)]
            if len(files) == 0:
                logger.error("You have not downloaded any recipes, please use the --download-remote flag to start")
            else:
                dict_ = settings.create_recipe_dict_from_local(files)
                settings.display_recipes(dict_)
        elif parser.downloadRecipe:
            _api = api.Api(only_remote=True)
            recipes = _api.list_recipes()
            selected_recipe_name = parser.downloadRecipe
            for selected in selected_recipe_name:
                if "all" in selected.lower():
                    settings.download_all_recipes()
                else:
                    for recipe in recipes:
                        if selected in recipe['filename']:
                            settings.download_recipe(selected, recipe, force=parser.forceAction)
            logger.info("Finished processing all acceptable recipes")
        else:
            if not os.path.exists(settings.HAS_INITIALIZED_DOWNLOADS):
                settings.logger.warning(
                    "You have not downloaded all the currently available recipes, "
                    "please use --download-remote all flag to download them"
                )
            if parser.useRecipe is not None:
                logger.debug("Checking if passed recipe is available in current recipe list")
                available_recipes = settings.load_recipes()
                passed_recipes = settings.create_recipe_list_from_passed(parser.useRecipe)
                for passed_recipe in passed_recipes:
                    if passed_recipe in list(available_recipes):
                        logger.info(f"Recipe found in available recipes, starting processing")
                        loaded_recipe = recipe_exec.load_recipe([passed_recipe], load_one=True)
                        if loaded_recipe is None:
                            logger.error(f"Recipe not loaded, skipping")
                        else:
                            logger.debug("Starting execution of loaded recipe")
                            try:
                                exec_results = recipe_exec.execute_recipe(loaded_recipe, parser.filename, parser.kwargs)
                                if exec_results is not None:
                                    logger.debug("Recipe executed successfully starting output parsing")
                                    output_file = settings.create_output_file(
                                        parser.outputType, parser.filename, passed_recipe.split(".")[0]
                                    )
                                    output_results = settings.create_output(exec_results, output_file)
                                    print(output_results)
                                else:
                                    logger.warning("Recipe did not execute successfully, skipping")
                            except Exception as e:
                                logger.error(f"Unable to execute recipe successfully, got error: {str(e)}")
                    else:
                        logging.warning(f"Passed recipe: {passed_recipe} not found in available recipes, skipping")
            if parser.useChain:
                logger.info("User passed chain process, starting the script parsing")
                if parser.chainScript is None:
                    logger.fatal("You did not pass a script to execute, please pass a chain script")
                else:
                    if parser.filename is None:
                        logger.fatal("You did not pass a filename to execute")
                    else:
                        chain_results = settings.execute_chain(parser.chainScript, parser.filename, **parser.kwargs)
                        output_file = settings.create_output_file(
                            parser.outputType, parser.filename, "recipe-chain"
                        )
                        output_results = settings.create_output(chain_results, output_file)
                        print(output_results)
        if parser.noStartEnd:
            logger.debug(f"Shutting down at: {datetime.datetime.now()}")
    except KeyboardInterrupt:
        logger.fatal("User interrupted the program, shutting down")
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.fatal(f"Unhandled exception happened, MCPB is exiting: {str(e)}")