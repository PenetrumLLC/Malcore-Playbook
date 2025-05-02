from setuptools import setup, find_packages
from malcore_playbook import __version__


if __name__ == "__main__":
    setup(
        name='malcore-playbook',
        packages=find_packages(),
        version=__version__.VERSION,
        description='Malcore Playbook automates malware analysis, malware triaging, '
                    'and analyst workflows using modular recipes and DSL scripting',
        author="Thomas Perkins",
        author_email="penetrumcorp@gmail.com",
        install_requires=["requests"],
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/PenetrumLLC/malcore-playbook",
        entry_points={
            'console_scripts': [
                'malcore-playbook=malcore_playbook.cli_tool:run',
                'mcpb=malcore_playbook.cli_tool:run',
            ]
        }
    )
