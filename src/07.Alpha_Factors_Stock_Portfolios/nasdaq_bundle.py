# nasdaq_bundle.py
import nasdaqdatalink
from zipline.data.bundles import register
from zipline.data.bundles.core import bundles, load
from zipline.data.bundles.nasdaq import nasdaq_equities


def register_nasdaq_bundle():
    register(
        "nasdaq",
        nasdaq_equities(["SPY", "AAPL", "MSFT"], start_date="2000-01-01"),  # Adicione seus símbolos
        calendar_name="NYSE",
    )