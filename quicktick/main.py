"""
Copyright (c) 2017 Christopher Harrison

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from jinja2.exceptions import TemplateSyntaxError

from . import config, description, version
from .formatter import Formatter
from .datasource import DataSource


class ConfigException(BaseException):
    """ Raised on config parsing error """


def initialise_default_config() -> None:
    """
    Create a default configuration file in the user's home directory if
    it doesn't already exist
    """
    config_file = os.path.join(os.path.expanduser("~"), ".quicktick")
    if not os.path.exists(config_file):
        from . import default_config
        with open(config_file, "wt") as f:
            f.write(default_config)


def create_argument_parser() -> ArgumentParser:
    """
    Create the argument parser
    
    @return  Configured argument parser
    """
    parser = ArgumentParser(
        prog="quicktick",
        description=description,
        formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("-V", "--version", action="version", version=version, help="show version and license information")
    parser.add_argument("--config", default="~/.quicktick", help="use alternative configuration file [%(default)s]")
    parser.add_argument("--crypto", help="symbol to use as the cryptocurrency")
    parser.add_argument("--fiat", help="symbol to use as the fiat currency")
    parser.add_argument("--template", help="template name or raw Jinja2 template")
    parser.add_argument("--source", help="source for the price data")

    return parser


def run():
    initialise_default_config()
    args = create_argument_parser().parse_args()

    try:
        try:
            config_file = os.path.normpath(os.path.expanduser(args.config))
            conf = config.load(config_file)

            # Minimal structural checking
            assert "ticker" in conf
            assert "source" in conf["ticker"]
            assert "crypto" in conf["ticker"]
            assert "fiat" in conf["ticker"]
            assert "template" in conf["ticker"]
            assert "templates" in conf
            assert conf["templates"]
            assert "sources" in conf
            assert conf["sources"]

        except FileNotFoundError:
            raise ConfigException(f"Couldn't read configuration from {config_file}; file not found")

        except AssertionError:
            raise ConfigException(f"Couldn't read configuration from {config_file}; invalid structure")

        try:
            sources = {
                symbol: DataSource(**parameters)
                for symbol, parameters in conf["sources"].items()}

        except (AttributeError, TypeError):
            raise ConfigException(f"Couldn't read configuration from {config_file}; invalid source definition")

        try:
            source_name = args.source or conf["ticker"]["source"]
            source = sources[source_name]

        except KeyError:
            raise ConfigException(f"No such data source named {source_name}")

        try:
            crypto_symbol = args.crypto or conf["ticker"]["crypto"]
            crypto = source.get_crypto(crypto_symbol)

        except KeyError:
            raise ConfigException(f"Data source {source_name} does not support cryptocurrency {crypto_symbol}")

        try:
            fiat_symbol = args.fiat or conf["ticker"]["fiat"]
            fiat = source.get_fiat(fiat_symbol)

        except KeyError:
            raise ConfigException(f"Data source {source_name} does not support fiat currency {fiat_symbol}")

        try:
            template = conf["templates"].get(args.template, args.template) \
                    or conf["templates"][conf["ticker"]["template"]]

            formatter = Formatter(template)

        except KeyError:
            raise ConfigException(f"No such template named {template}")

        except TemplateSyntaxError:
            raise ConfigException(f"Couldn't parse template")

    except ConfigException as e:
        print(e, file=sys.stderr)
        exit(1)

    print(formatter.render(source, crypto, fiat))


if __name__ == "__main__":
    run()
