import os
import sys

import malcore_playbook.lib.settings as settings


def load_recipe(recipes, load_one=False, speak=True):
    loaded = []
    for recipe in recipes:
        if speak:
            try:
                settings.logger.info(f"Attempting to load recipe: {recipe.__name__}")
            except:
                settings.logger.info("Attempting to load recipe")
        recipe_home = settings.RECIPE_HOME
        full_path = os.path.join(recipe_home, recipe)
        path, fname = os.path.split(full_path)
        modulename, _ = os.path.splitext(fname)
        if path not in sys.path:
            if speak:
                settings.logger.debug("Path not found in sys.path adding to it")
            sys.path.insert(0, path)
        try:
            imported_mod = __import__(modulename)
            if settings.user_can_use_recipe(imported_mod.__excluded_plans__):
                loaded.append(__import__(modulename))
            else:
                if speak:
                    settings.logger.warning(
                        f"Your plan does not allow usage of recipe: {recipe}, "
                        f"to upgrade your plan see here: https://malcore.io/pricing"
                    )
        except Exception as e:
            if speak:
                settings.logger.error(f"Cannot import recipe: {recipe}, hit error: {str(e)}")
    if len(loaded) != 0:
        if load_one:
            return loaded[0]
        else:
            return loaded
    else:
        settings.logger.warning("No recipes loaded successfully")
        return None


def execute_recipe(recipe, *args, **kwargs):
    settings.logger.info(f"Attempting to execute recipe: {recipe}")
    try:
        results = recipe.plugin(*args, **kwargs)
        if results is not None:
            settings.logger.debug(f"Recipe executed successfully returning results")
        return results
    except Exception as e:
        import traceback
        traceback.print_exc()
        settings.logger.error(f"Unable to execute recipe, got error: {str(e)}")
        return None
