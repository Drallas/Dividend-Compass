# Dividend Compass

Dividend Compass is a scenario calculator that compares a dividend fund portfolio with an accumulating fund portfolio. Enter an amount, a desired monthly income, a split between dividend and accumulating funds, and a scenario. The app then shows how the portfolio could develop over a chosen period, including payouts, tax estimates and costs.

It is a single HTML file that runs in the browser. There is no server, no account and no tracking. Your inputs are saved in your own browser's local storage.

## Features

- **Investment forecast**: value over time for the dividend and accumulating parts, with the total return per year.
- **Net worth forecast**: the value after an estimated Box 3 tax, for periods of 1 to 40 years, with the time it takes to double your net investment.
- **Payout forecast**: the expected income per month and per year from the dividend funds, with the cumulative total.
- **Tax**: per-country estimates for the Netherlands (Box 3), the United States (withholding tax), Argentina (foreign assets) and a number of other countries, with an explanation per country.
- **Funds and assumptions**: the funds in the model with their yields, price growth, TER and risk, plus the weights per fund. All values are editable.
- **Strategies**: defensive, balanced and aggressive presets that set the split and the fund weights.
- **Scenarios**: low, base and high, which adjust the price growth and yield assumptions.
- **Saved scenarios and export**: save named scenarios in the browser, export a CSV, or print to PDF.
- **Cost warning**: a warning appears when the weighted TER of your mix goes above 0.40%.
- Dutch, English and Spanish, with a light and a dark theme.

## How it works

The model is deliberately simple. Each fund grows with its price growth minus its TER. The yield of a dividend fund is paid out each year, either reinvested or paid out to you. Scenarios add or subtract a fixed number of percentage points to growth and yield.

Fund data (yields, price growth, TER, US share of holdings) are estimates entered by hand. They are not live market data and they are not guaranteed to be correct. Check them against the fund providers before you rely on them.

The tax estimates are rough. Box 3 uses the tax-free allowance and the flat return from the tax tab. Withholding tax and foreign tax are approximations. The Argentine foreign-asset figures are estimates and should be verified with the tax authority.

Payouts are spread evenly over the twelve months. Real funds pay out irregularly, per month or per quarter.

## Disclaimer

This is a scenario tool, not a forecast and not financial or tax advice. Past returns do not predict future results. Verify all figures yourself before making decisions.

## Running it

Open `index.html` in a browser. Nothing needs to be installed.

## License

See [LICENSE](LICENSE).
