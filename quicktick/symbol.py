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


class Symbol(T.Mapping[str, str]):
    """ Ticker symbol """
    _symbol:str
    _properties:T.Dict[str, str]

    def __init__(self, symbol:str, **properties:str) -> None:
        """
        Constructor

        @param  symbol      Ticker symbol
        @param  properties  Property keys and values
        """
        self._symbol = symbol
        self._properties = properties

    def __str__(self) -> str:
        return self._symbol

    def __len__(self) -> int:
        return len(self._properties)

    def __getitem__(self, key:str) -> str:
        return self._properties[key]

    def __iter__(self) -> T.Iterator[str]:
        return iter(self._properties)

    def __contains__(self, key:str) -> bool:
        return key in self._properties

    def __eq__(self, other:"Symbol") -> bool:
        return self._symbol == other._symbol \
           and self._properties == other._properties

    def __ne__(self, other:"Symbol") -> bool:
        return not self == other

    def keys(self) -> T.KeysView[str]:
        return self._properties.keys()

    def items(self) -> T.ItemsView[str, str]:
        return self._properties.items()

    def values(self) -> T.ValuesView[str]:
        return self._properties.values()

    def get(self, key:str, default:T.Optional[str] = None) -> T.Optional[str]:
        return self._properties.get(key, default)
