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

import typing as T

import requests
from jinja2 import Template

from .symbol import Symbol


class DataSource(object):
    """ Price data source """
    _url:Template
    _data:T.Dict[str, Template]
    _cryptos:T.Dict[str, Symbol]
    _fiats:T.Dict[str, Symbol]

    def __init__(self, url:str,
                       data:T.Dict[str, str],
                       cryptos:T.Dict[str, T.Dict[str, str]],
                       fiats:T.Dict[str, T.Dict[str, str]]) -> None:
        """
        Constructor

        @param  url      Data source API URL
        @param  data     Data mappings
        @param  cryptos  Supported cryptocurrencies and their properties
        @param  fiats    Supported fiat currencies and their properties
        """
        self._url = Template(url)

        self._data = {
            key: Template(template)
            for key, template in data.items()}

        self._cryptos = {
            crypto: Symbol(crypto, **properties)
            for crypto, properties in cryptos.items()}

        self._fiats = {
            fiat: Symbol(fiat, **properties)
            for fiat, properties in fiats.items()}

    def get_crypto(self, crypto:str) -> Symbol:
        """
        Get supported cryptocurrency by symbol as a string

        @param   crypto  Cryptocurrency symbol
        @return  Cryptocurrency symbol
        """
        return self._cryptos[crypto]

    def get_fiat(self, fiat:str) -> Symbol:
        """
        Get supported fiat currency by symbol as a string

        @param   fiat  Fiat currency symbol
        @return  Fiat currency symbol
        """
        return self._fiats[fiat]

    def get_data(self, crypto:Symbol, fiat:Symbol) -> T.Dict[str, str]:
        """
        Fetch the price data from the source and map it to the output
        schema

        @param   crypto  Cryptocurrency symbol
        @param   fiat    Fiat currency symbol
        @return  Mapped price data
        """
        url = self._url.render(crypto=crypto, fiat=fiat)
        json = requests.get(url).json()

        return {
            key: template.render(json=json, crypto=crypto, fiat=fiat)
            for key, template in self._data.items()}
