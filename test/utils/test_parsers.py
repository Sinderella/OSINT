from osint.utils.parsers import param_parser


def test_param_parser():
    line = 'set Name Sinderella'
    argc, argv = param_parser(line)
    assert argc == len(line.split())
    assert argv == line.split()
