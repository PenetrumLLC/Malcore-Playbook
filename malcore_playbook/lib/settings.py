#  Copyright (c) 2025.
#  Penetrum LLC (all rights reserved)
#  Copyright last updated: 5/2/25, 12:44 PM
#
#

import os
import sys
import json
import time
import getpass
import logging
import datetime
import hashlib
from logging.handlers import RotatingFileHandler
from importlib.metadata import distribution

import malcore_playbook.writers.json_output as json_writer
import malcore_playbook.writers.pdf_output as pdf_writer
import malcore_playbook.writers.txt_output as txt_writer
import malcore_playbook.writers.console_output as console_writer
import malcore_playbook.malscript.parse as chain_script
import malcore_playbook.lib.api as api
import malcore_playbook.__version__ as version

import requests


class NoFilenameProvided(Exception):
    """ raise when there is no file provided """
    pass


class JsonLogFormatter(logging.Formatter):

    """ export the log to a JSON format and log to a JSON file """

    def format(self, record):
        log_record = {
            "timestamp": datetime.datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "filename": record.filename,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


# home directory where all config files are stored
HOME = f"{os.path.expanduser('~')}{os.path.sep}.mcpb"
# this is where the recipes are stored
RECIPE_HOME = f"{HOME}{os.path.sep}.recipes"
# RECIPE_HOME = "test-plugins"
# the config file that contains the API keys and what not
CONFIG_FILE = f"{HOME}{os.path.sep}config.json"
# the directory that will contain all the output results
OUTPUT_DIR = f"{HOME}{os.path.sep}results"
# did the user accept the eula?
ACCEPTED_EULA = f"{HOME}{os.path.sep}.accepted"
# what plan does the user have? this isn't used yet
PLAN_FILE = f"{HOME}{os.path.sep}.user_plan"
# backup plan file incase the plans differ
BACKUP_USER_PLAN = f"{HOME}{os.path.sep}.backup_plan"
# has the user download anything yet?
HAS_INITIALIZED_DOWNLOADS = f"{HOME}{os.path.sep}.initialized_downloads"
# version of the program
VERSION = version.VERSION
# program alias nick
VERSION_ALIAS = version.VERSION_ALIAS
# logo header
HEADER = f"""
\033[91m• ▌ ▄ ·. \033[0m ▄▄·  ▄▄▄·▄▄▄▄· 
\033[91m·██ ▐███▪\033[0m▐█ ▌▪▐█ ▄█▐█ ▀█▪
\033[91m▐█ ▌▐▌▐█·\033[0m██ ▄▄ ██▀·▐█▀▀█▄
\033[91m██ ██▌▐█▌\033[0m▐███▌▐█▪·•██▄▪▐█
\033[91m▀▀  █▪▀▀▀·\033[0m▀▀▀ .▀   ·▀▀▀▀  v{VERSION}({VERSION_ALIAS})
     Malcore-Playbook
"""
# the eula
EULA = """MALCORE PLAYBOOK END USER LICENSE AGREEMENT (EULA)

1. LICENSE GRANT
Malcore grants you a limited, non-exclusive, non-transferable, revocable license to use the Malcore Playbook software ("Software") solely for personal, non-commercial, and evaluation purposes during the trial period.

2. TRIAL PERIOD
The Software may be used under a free trial license for evaluation purposes only. The trial period is limited to 30 days from the initial installation date, unless otherwise explicitly granted in writing by Malcore. Continuation of use beyond the trial period without obtaining a valid commercial license is strictly prohibited for any commercial, organizational, or institutional purpose.

3. COMMERCIAL USE
Use of the Software by any entity other than an individual for non-commercial personal evaluation is considered Commercial Use. This includes, but is not limited to:
- Use by businesses, corporations, LLCs, partnerships, government agencies, educational institutions, and non-profits;
- Use on behalf of an employer;
- Use in support of business operations, revenue-generating activities, cybersecurity services, malware analysis services, or internal security operations.
Commercial Use requires the purchase of an active commercial license, regardless of any technical limitations or continued functionality of the Software beyond the trial period.

4. LICENSE COMPLIANCE
By using the Software, you agree to comply with all license terms, including timely acquisition of a commercial license where required. Failure to obtain an appropriate license for Commercial Use constitutes a violation of this EULA and may result in legal action, penalties, or termination of access.

5. UNAUTHORIZED MODIFICATION AND CIRCUMVENTION
You agree not to attempt to modify, tamper with, disable, reverse-engineer, or circumvent any technical limitations, license controls, or usage restrictions in the Software. Malcore reserves the right to audit Software usage to verify compliance.

6. OWNERSHIP
Malcore retains all rights, title, and interest in and to the Software, including all intellectual property rights. No ownership or other rights are transferred under this EULA except as expressly stated.

7. DISCLAIMER OF WARRANTIES
The Software is provided "AS IS" without warranties of any kind, express or implied. Malcore disclaims all warranties, including but not limited to implied warranties of merchantability, fitness for a particular purpose, and non-infringement.

8. LIMITATION OF LIABILITY
In no event shall Malcore, its affiliates, or its licensors be liable for any indirect, incidental, special, consequential, or punitive damages, or any loss of profits or revenues, whether incurred directly or indirectly, arising from your use of the Software.

9. GOVERNING LAW
This EULA is governed by and construed in accordance with the laws of Virginia USA.

10. AMENDMENTS
Malcore reserves the right to modify or update this EULA at any time. Continued use of the Software following any changes constitutes your acceptance of those changes.

USER ACCEPTANCE
By installing, copying, accessing, or otherwise using the Malcore Playbook Software, you acknowledge that you have read, understood, and agree to be bound by the terms of this EULA.

NOTICE: Commercial use of Malcore Playbook without an active commercial license is prohibited. Unauthorized commercial use may result in retroactive licensing fees, account suspension, and/or legal action."""


def init(force=False):
    """ initialization function that starts the init of the program """
    if force:
        print("Forcing config refactoring")
    if not os.path.exists(HOME) or force:
        try:
            try:
                os.makedirs(HOME)
                os.makedirs(RECIPE_HOME)
            except:
                pass
            print(
                "You will need to accept out EULA before you begin, you will only see this once, "
                "you can find our terms of service here: https://malcore.io/terms-of-use"
            )
            print(f"\n{EULA}\n")
            is_accepted = False
            acceptable_answers = ('yes', 'no')
            while not is_accepted:
                answer = input("To accept type 'yes' to decline type 'no': ").strip()
                if answer.lower() not in list(acceptable_answers):
                    logger.warning("Please type 'yes' or 'no'")
                elif answer.lower() == 'yes':
                    open(ACCEPTED_EULA, "a+").write(f"Accepted on: {datetime.datetime.utcnow().isoformat()} UTC")
                    is_accepted = True
                else:
                    print("You have declined the EULA, this program will now exit")
                    os.remove(HOME)
                    return
            trial_file = f"{HOME}/.trial"
            with open(trial_file, "w") as fh:
                json.dump({"trial_end_date": int(time.time())}, fh)
            with open(PLAN_FILE, "w") as fh:
                fh.write("*")
            print("A free 30 day trial has been activated for you!")
            with open(CONFIG_FILE, 'w') as fh:
                print(
                    "You will need to login to start using the Malcore Playbook. If you do not have an account "
                    "please make one here: https://app.malcore.io/register"
                )
                api_ = api.Api(only_remote=True)
                entered = False
                while not entered:
                    username = input("Enter your email: ")
                    password = getpass.getpass("Enter your password: ")
                    if username == "" or password == "":
                        print("Please enter your credentials")
                    else:
                        data = api_.login(username, password)
                        if data['data'] is None:
                            print("Got error while trying to login:")
                            for warning in data['messages']:
                                print(f"Type: {warning['type']} Message: {warning['message']}")
                            print("Please try again")
                        else:
                            key = data['data']['user']['apiKey']
                            user_plan = data['data']['user']['subscription']['name']
                            plan_id = data['data']['user']['subscription']['planId']
                            file_size_limit = data['data']['user']['subscription']['fileSizeLimit']
                            entered = True
                key = key.strip()
                json.dump({"api_key": key, "plan_id": plan_id, "file_size_limit": file_size_limit}, fh)
                with open(BACKUP_USER_PLAN, 'w') as fh1:
                    fh1.write(user_plan)
                if force:
                    print("Config refactored successfully, you will need to rerun the program to start")
                else:
                    print("Initialization completed, you will need to rerun the program to start")
            exit(1)
        except KeyboardInterrupt:
            print("User quit install, removing home directory")
            try:
                os.remove(HOME)
            except:
                print(f"Failed to remove home directory do so manually: {HOME}")
            sys.exit(1)
        except Exception as e:
            print(f"Caught error: {str(e)}, please start the program again")
            try:
                os.remove(HOME)
            except:
                print(f"Failed to remove the HOME directory to restart install, do so manually: {HOME}")
            sys.exit(1)
    else:
        check_is_trial()
        with open(CONFIG_FILE, 'r') as fh:
            return json.load(fh)


def setup_logger(logger_name="MalcorePlaybook"):
    """ logger setup """
    log_dir = f"{HOME}"
    if not os.path.exists(log_dir):
        init()
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('[%(asctime)s][%(module)s:%(funcName)s:%(lineno)d][%(name)s][%(levelname)s] %(message)s')
    output_formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
    output_handler = logging.StreamHandler()
    output_handler.setLevel(logging.DEBUG)
    output_handler.setFormatter(output_formatter)
    stream_handler = RotatingFileHandler(f"{log_dir}/malcore-playbook.json", maxBytes=1_000_000, backupCount=3)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(JsonLogFormatter())
    file_handler = RotatingFileHandler(f"{log_dir}/malcore-playbook.log", maxBytes=1_000_000, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(output_handler)
    logger.addHandler(stream_handler)
    return logger


logger = setup_logger()


def load_conf():
    """ load the config file """
    with open(CONFIG_FILE, 'r') as fh:
        return json.load(fh)


def display_recipes(recipes, filter_=None):
    """ display the recipes passed in a pretty format """
    max_display_chars = 25
    col_width = 35
    s = f"{'Recipe:'.ljust(col_width)}{'Version'.ljust(col_width)}{'Author'}"
    print("-" * (len(s) + 10))
    print(s)
    for recipe in recipes:
        if filter_ is None:
            recipe_name = recipe["filename"].split(".")[0]
            recipe_name = recipe_name[:max_display_chars]
            version = recipe['version'][:max_display_chars]
            author = recipe['author'][:max_display_chars]
            print(f"{recipe_name.ljust(col_width)}{version.ljust(col_width)}{author}")
        else:
            recipe_name = recipe["filename"].split(".")[0]
            if filter_ in recipe_name:
                recipe_name = recipe_name[:max_display_chars]
                version = recipe['version'][:max_display_chars]
                author = recipe['author'][:max_display_chars]
                print(f"{recipe_name.ljust(col_width)}{version.ljust(col_width)}{author}")
    print("-" * (len(s) + 10))


def create_recipe_dict_from_local(local_files):
    """ creates a dict from local recipe files"""
    recipes = []
    for file_ in local_files:
        if not any(p in file_ for p in ("__pycache__", "__init__.py")):
            path, fname = os.path.split(file_)
            modulename, _ = os.path.splitext(fname)
            if path not in sys.path:
                sys.path.insert(0, path)
            i = __import__(modulename)
            author = i.__author__
            version = i.__version__
            filename = file_.split(os.path.sep)[-1]
            recipes.append({"filename": filename, "version": version, "author": author})
    return recipes


def download_recipe(recipe, full_data, force=False, show_output=True):
    """ download the external recipes into the RECIPE directory """
    try:
        output_dir = f"{RECIPE_HOME}{os.path.sep}{recipe}.py"
        logger.info(f"Attempting to download recipe: {recipe} to {output_dir}")
        if os.path.exists(output_dir):
            if not force:
                logger.error("Recipe exists, skipping installation")
                return
            else:
                logger.debug("Recipe exists, forcing installation")
        url = f"https://recipes.malcore.io/recipes/{recipe}.py"
        logger.info(f"Downloading recipe from: {url}")
        if show_output:
            print(f"Recipe metadata:\n"
                  f"\tHashsum: {full_data['hashsum']}\n"
                  f"\tVersion: {full_data['version']}\n"
                  f"\tAuthor: {full_data['author']}")
        with open(output_dir, 'wb') as fh:
            logger.debug("Starting download ....")
            with requests.get(url, stream=True) as req:
                req.raise_for_status()
                for chunk in req.iter_content(chunk_size=1024):
                    if chunk:
                        fh.write(chunk)
        logger.info(f"Recipe downloaded successfully to: {output_dir}")
        return True
    except Exception as e:
        logger.error(f"Hit error: {str(e)} while downloading recipe")
        return False


def load_recipes():
    """ load all the local recipes """
    return os.listdir(RECIPE_HOME)


def create_recipe_list_from_passed(passed):
    """ create a list of files from loaded recipes """
    logger.debug(f"Creating recipe list from passed, total of {len(passed)} recipe(s) to process")
    results = []
    for recipe in passed:
        results.append(f"{recipe}.py")
    return results


def hash_file(filename):
    """ get the hash of a file """
    if isinstance(filename, list):
        filename = filename[0]
    with open(filename, 'rb') as fh:
        h = hashlib.sha256()
        h.update(fh.read())
        return h.hexdigest()


def create_output_file(output_type, filename, recipe):
    """ creates a output file from the passed data """
    logger.debug(f"Creating output, passed type: {output_type}")
    file_hash = hash_file(filename)
    ext = output_type.lower()
    if ext != "console":
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        if not os.path.exists(f"{OUTPUT_DIR}{os.path.sep}{output_type}"):
            os.makedirs(f"{OUTPUT_DIR}{os.path.sep}{output_type}")
        file_path = f"{OUTPUT_DIR}{os.path.sep}{output_type}{os.path.sep}{file_hash}-{recipe}.{ext}"
        logger.debug(f"Output file path generated, will use path: {file_path}")
        return file_path
    else:
        logger.debug("Output will be console based")
        return "CONSOLE"


def create_output(output_results, output_file):
    """ creates the file that the output will be stored in """
    if output_file.endswith(".json"):
        output = json_writer.output(output_results, output_file)
    elif output_file.endswith("pdf"):
        output = pdf_writer.output(output_results, output_file)
    elif output_file.endswith("txt"):
        output = txt_writer.output(output_results, output_file)
    elif output_file == "CONSOLE":
        output = console_writer.output(output_results, output_file)
    else:
        raise NotImplementedError("That output type is not implemented yet")
    return output


def get_user_plan():
    """ get the plan the user is currently using """
    return open(PLAN_FILE).read()


def user_can_use_recipe(allowed):
    """ can the user execute the passed recipe? """
    user_plan = get_user_plan()
    if check_is_trial():
        return True
    if allowed is None:
        return True
    else:
        if allowed.lower() in user_plan.lower():
            return False
        return True


def check_is_trial():
    """ is the user under the trial? """
    trial_file = f"{HOME}/.trial"
    if not os.path.exists(trial_file):
        return False
    else:
        try:
            data = json.load(open(trial_file))
        except:
            data = None
        if data is None:
            return False
        else:
            trial_end_timestamp = data['trial_end_date']
            today = datetime.datetime.utcnow()
            trial_end_date = datetime.datetime.utcfromtimestamp(trial_end_timestamp)
            trial_end_date = (trial_end_date + datetime.timedelta(days=30)).date()
            if today.date() > trial_end_date:
                logger.warning(
                    "Your premium trial has expired, please sign up for a plan here: https://malcore.io/pricing"
                )
                try:
                    with open(PLAN_FILE, 'w') as fh:
                        new_plan = open(BACKUP_USER_PLAN).read()
                        fh.write(new_plan)
                    os.remove(trial_file)
                except Exception as e:
                    logger.error(f"Failed to remove trial file, got error: {str(e)}")
            else:
                already_said = f"{HOME}/.spoken"
                if not os.path.exists(already_said):
                    logger.info(
                        f"You are currently on a premium trial membership! Your trial ends on: {trial_end_date}. "
                        f"By using this trial you are accepting our Terms of Service: https://malcore.io/terms-of-use, "
                        f"to upgrade your plan please see here: https://malcore.io/pricing"
                    )
                    open(already_said, "w").close()
                return True


def execute_chain(script, filename, **kwargs):
    """ execute the MalScript """
    if os.path.exists(script):
        extension = os.path.splitext(script)[1]
        acceptable_extensions = (".mals", ".mal", ".ms")
        if any(extension == e for e in list(acceptable_extensions)):
            exec_script = open(script).read()
        else:
            raise chain_script.InvalidScriptPassed(
                f"Script extension is unverifiable (not any of: {', '.join(list(acceptable_extensions))}), "
                f"will not execute the script"
            )
    else:
        exec_script = script
    return chain_script.run(exec_script, filename, kwargs)


def download_all_recipes(only_list=False):
    """ download all external recipes """
    percent = lambda part, whole: round((part / whole) * 100, 2)
    _api = api.Api(only_remote=True)
    data = _api.list_recipes()
    total_recipes = len(data)
    if only_list:
        return data
    total_downloaded = 0
    for recipe in data:
        is_successful = download_recipe(recipe['filename'].split(".")[0], recipe, force=True)
        if is_successful:
            total_downloaded += 1
    open(HAS_INITIALIZED_DOWNLOADS, "a+").close()
    logger.info(f"Downloaded {total_downloaded} recipes out of {total_recipes} ({percent(total_downloaded, total_recipes)}%)")


def check_for_recipe_updates(force_download=False):
    """ check if any of the local recipes need to be updated from the external source """
    import malcore_playbook.execution.recipe_exec as recipe_exec

    updates_needed = []
    total_needed = 0

    if force_download:
        logger.debug("Will be downloading all recipes that need to be updated automatically")

    downloaded_recipes = load_recipes()
    remote_recipes = download_all_recipes(only_list=True)
    imported_recipes = recipe_exec.load_recipe(downloaded_recipes, speak=False)
    local_recipes = [[i.__hashsum__, i.__file__.split(os.path.sep)[-1]] for i in imported_recipes]
    for remote_recipe in remote_recipes:
        for local_recipe in local_recipes:
            if local_recipe[1] == remote_recipe['filename']:
                if not local_recipe[0] == remote_recipe['hashsum']:
                    total_needed += 1
                    logger.warning(
                        f"Recipe: {local_recipe[1]} has an update available to version: {remote_recipe['version']}"
                    )
                    updates_needed.append(local_recipe[1])
                    if force_download:
                        download_recipe(remote_recipe['filename'].split(".")[0], remote_recipe, force=True)
    if len(updates_needed) == 0:
        logger.info("There are no recipes that need to be updated")
    else:
        logger.warning(f"There are a total of {total_needed} recipe(s) that require an update")


def check_for_updates():
    """ checks if the program is up to date or not """
    try:
        current_version = VERSION
        url = f"https://pypi.org/pypi/malcore-playbook/json"
        req = requests.get(url, timeout=3)
        data = req.json()
        newest_version = data['info']['version']
        if current_version < newest_version:
            logger.warning(f"New version available, it is highly suggested that you update to version: {newest_version}")
    except:
        logger.warning("Unable to check for a newer version")
