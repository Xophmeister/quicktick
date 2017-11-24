__version__ = "0.2.5"

description = """\
Output a cryptocurrency price ticker to stdout based on the
configuration found in ~/.quicktick. Options can be provided at the
command line to override any part of the ticker configuration.
"""

version = f"""\
quicktick v{__version__}

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
with this program. If not, see <https://www.gnu.org/licenses/>."""

default_config = r"""---
ticker:
  source: coinmarketcap
  crypto: BTC
  fiat: USD
  template: simple

templates:
  simple: >
    {{ fiat }}/{{ crypto }}
    {{ "%.2f" | format(rate | float) }}
    ({{ "%.2f" | format(change | float) }}%)

  ansi: >
    {{ fiat }}/{{ crypto }}
    {{ "%.2f" | format(rate | float) }}
    {% if (change | float) > 0 %}{{ "\033[32m" }}{{ "%.2f" | format(change | float) }}%
    {% elif (change | float) < 0 %}{{ "\033[31m" }}{{ "%.2f" | format(change | float | abs) }}%
    {% endif %}{{ "\033[0m" }}

sources:
  coinmarketcap:
    url: https://api.coinmarketcap.com/v1/ticker/{{ crypto["api_path"] }}/?convert={{ fiat }}

    data:
      rate: >
        {{ json[0]["price_" + ( fiat | lower )] }}
      change: >
        {{ json[0]["percent_change_1h"] }}

    cryptos:
      BTC:
        api_path: bitcoin
      BCH:
        api_path: bitcoin-cash
      ETH:
        api_path: ethereum
      LTC:
        api_path: litecoin

      # CoinMarketCap supports many more cryptocurrencies.
      # Add them here, as required...

    fiats:
      CNY: {}
      EUR: {}
      GBP: {}
      USD: {}

      # CoinMarketCap supports many more fiat currencies.
      # Add them here, as required...
"""
