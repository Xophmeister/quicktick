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

from jinja2 import BaseLoader, Environment, Template

from .datasource import DataSource
from .symbol import Symbol


class Formatter(object):
    """ Formatter """
    _template:Template

    def __init__(self, template:str) -> None:
        """
        Constructor

        @param  template  Jinja2 template string
        """
        env = Environment(loader=BaseLoader())
        self._template = env.from_string(template)

    def render(self, source:DataSource, crypto:Symbol, fiat:Symbol) -> str:
        """
        Render the template with the given context, which includes
        fetching the price data

        @param   source  Price data source
        @param   crypto  Cryptocurrency symbol
        @param   fiat    Fiat currency symbol
        @return  Rendered output
        """
        try:
            price_data = source.get_data(crypto, fiat)

        except:
            return "Data source failure"

        return self._template.render(crypto=crypto, fiat=fiat, **price_data)
