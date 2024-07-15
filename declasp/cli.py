import sys
from argparse import ArgumentParser

def run_conformance_checking(args):
    from declasp.tasks import conformance_checking, ConformanceCheckingResult
    from declasp.log import StringEventLog
    from declasp.declare import declare_model_from_json
    import json

    with open(args.model) as data:
        model = declare_model_from_json(json.load(data))
    log = StringEventLog.from_xes(args.log)

    result: ConformanceCheckingResult = conformance_checking(model, log)
    print(json.dumps(result.as_json(), indent=2))

    sys.exit(0)

def run_query_checking(args):
    print("Query checking is currently not implemented in the CLI, sorry!\nRefer to Python examples!")
    sys.exit(0)

def run_satisfiability(args):
    from declasp.tasks import satisfiability
    from declasp.declare import declare_model_from_json
    import json

    with open(args.model) as data:
        model = declare_model_from_json(json.load(data))
    ans = satisfiability(model, args.horizon)

    print(json.dumps(ans, indent=2))

    sys.exit(0)


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    # Conformance subcommand
    parser_conformance = subparsers.add_parser('conformance_checking')
    parser_conformance.add_argument('model', type=str, help="Path to a Declare model in JSON format.")
    parser_conformance.add_argument('log', type=str, help="Path to an event log in XES format.")
    parser_conformance.set_defaults(func=run_conformance_checking)

    # Query subcommand
    parser_query = subparsers.add_parser('query_checking', help='Run a query')
    parser_query.add_argument('model', type=str, help="Path to a Declare model in JSON format.")
    parser_query.add_argument('log', type=str, help="Path to an event log in XES format.")
    parser_query.set_defaults(func=run_query_checking)

    # Satisfiability subcommand
    parser_satisfiability = subparsers.add_parser('bounded_satisfiability')
    parser_satisfiability.add_argument('model', type=str, help='Path to a Declare model in JSON format.')
    parser_satisfiability.add_argument('horizon', type=int, help='Maximum length for the searched model.')
    parser_satisfiability.set_defaults(func=run_satisfiability)

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
