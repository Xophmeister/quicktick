quicktick
=========
Output a cryptocurrency price ticker to stdout based on the
configuration found, by default, in ``~/.quicktick``. Options can be
provided at the command line to override any part of the ticker
configuration.

Installation
------------
quicktick requires Python 3.6, or newer, and can be installed using
``pip``:

::

  pip install quicktick

Usage
-----
::

  quicktick [-h] [-V] [--config CONFIG] [--crypto CRYPTO] [--fiat FIAT] [--template TEMPLATE] [--source SOURCE]


Options are as follows:

-h, --help           Show this help message and exit
-V, --version        Show version and license information
--config CONFIG      Use alternative configuration file
--crypto CRYPTO      Symbol to use as the cryptocurrency
--fiat FIAT          Symbol to use as the fiat currency
--template TEMPLATE  Template name or raw Jinja2 template
--source SOURCE      Source for the price data

Configuration
-------------
The configuration is a YAML file, which will be created in your home
directory on first run (if it doesn't already exist), which defines the
default ticker, how to output price data and how data sources are
defined. Jinja2 templating is used to make this very adaptable to your
needs.

The default configuration only defines a data source for the
`CoinMarketCap <https://coinmarketcap.com/>`_ API with support for:

:Cryptocurrencies:
  * Bitcoin
  * Bitcoin Cash
  * Ethereum
  * Litecoin

:Fiat currencies:
  * US Dollars
  * Euros
  * Chinese Yuan
  * British Pounds

:Price data:
  * Exchange rate
  * Change in the last hour

CoinMarketCap's API supports many more options and these can be added to
your configuration, as needed. Alternatively, other JSON-based HTTP APIs
can be defined as data sources.

Ticker
~~~~~~
The default ticker is defined under the ``ticker`` section in the
configuration. It takes four attributes:

``source``
  The data source to use, defined in the ``sources`` section.

``crypto``
  The cryptocurrency symbol to use, as defined by the ``source``.

``fiat``
  The fiat currency symbol to use, as defined by the ``source``.

``template``
  The template to use to render the ticker, defined in the ``templates``
  section (n.b., this must be a predefined template; a raw Jinja2
  template string can only be used at the command line).

Templates
~~~~~~~~~
The ``templates`` section is used to define named Jinja2 templates. By
default, there is ``simple`` and ``ansi`` (which is the same as
``simple``, with ANSI escape sequences used for colour output). When the
templates are rendered, they have access to three sets of data:

``fiat``
  The fiat currency symbol (see `Data Sources`_ for details).

``crypto``
  The cryptocurrency symbol (see `Data Sources`_ for details).

Price data
  The price data variables returned by the data source (see `Data
  Sources`_ for details).

Data Sources
~~~~~~~~~~~~
The ``sources`` section is used to define named data sources; that is,
JSON-based HTTP APIs. Each data source takes four attributes:

``url``
  The URL for the data source; again, a Jinja2 template that is supplied
  with the ``fiat`` and ``crypto`` symbols.

``data``
  This subsection allows you to define the price data variables that are
  available to the output template. These are again Jinja2 templates
  that describe the mapping from the API's ``json`` response, along with
  the ``crypto`` and ``fiat`` symbols.

``cryptos`` and ``fiats``
  These subsections allow you to define cryptocurrencies and fiat
  currencies, respectively. Conventionally, you would use the symbol
  name as the currency's identifier, which take a dictionary of named
  parameters. These parameters are then available to the templates that
  use the symbols.

License
-------
Copyright (c) 2017 Christopher Harrison

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.
