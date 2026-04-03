import argparse
import logging
import sys
import requests
import subprocess
from pathlib import Path


URL = 'http://127.0.0.1:8080'


def request(args, message=None):
    """
    Request to run the llm model.
    """
    # If args.query is None, which means user is in loop and allowed to ask directly to the model without using arguments.
    if args is None:
        params = {
            "query": message
        }
    else:
        params = {
            "query": args.query
        }

    response = requests.get(f'{URL}/request/', params=params)

    if response.status_code == 200:
        data = response.json()
        print(data["ai_response"])
    else:
        print(f"Error: Received status code {response.status_code}")


def exit_func(args):
    """
    Exit the system.
    """
    sys.exit()


def start(args):
    """
    Start the server and model locally.
    """
    subprocess.run("cd ~/.blueclawai/bin/server; uvicorn llm_server:app --port=8080", shell=True)


def run(args):
    """
    Run the model.
    """
    subprocess.run("./~/.blueclawai/bin/app", shell=True)



class ArgumentParser(argparse.ArgumentParser):
    """
    Argument parser for the command line interface.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "A command to run the BlueClaw locally on your terminal"
        
    def parse_args(self, args=None, namespace=None):
        return super().parse_args(args, namespace)
    
    def error(self, message):
        return message



def parser_init():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    request_parser = subparsers.add_parser('request', help='Request to run the llm model')
    request_parser.add_argument('-q','--query', type=str, help='text or query to ask the model')
    request_parser.set_defaults(func=request)

    if Path("~/.blueclawai/server").is_dir:
        start_parser = subparsers.add_parser('start_server', help='Start to run the server and model locally')
        start_parser.set_defaults(func=start)
    
    run_parser = subparsers.add_parser('run', help='Run the model')
    run_parser.add_argument('-m', '--model', type=str, default='llm', help='Choosing the Artificial Intelligence model')
    run_parser.set_defaults(func=run)

    return parser
