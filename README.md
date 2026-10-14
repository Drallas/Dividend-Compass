# Dividend Compass

Dividend Compass compares two ways of investing in funds: a **dividend fund** that pays out its income to you, and an **accumulating fund** that keeps the income inside the fund so it grows. Enter an amount, a monthly income goal (optional), a split between the two, and a scenario. The app then shows how that portfolio could develop over 1 to 40 years, including payouts, estimated tax and fund costs.

It is built for people who are deciding between income now and growth later, and want to see the numbers side by side before they commit. It is a scenario tool, not a forecast and not financial or tax advice.

## Who it is for

- Investors who are deciding how much of their portfolio should pay out as income and how much should grow.
- People who want to see what fund costs (TER) and tax do to the result over the years.
- Anyone who wants to compare tax per country on the same return, before choosing where to invest.

## Quick start

1. Open `index.html` in a browser. Nothing needs to be installed.
2. Enter your amount on the Forecast tab, and turn the monthly income goal on or off.
3. Pick a strategy (defensive, balanced or aggressive) as a starting point.
4. Read the Investment forecast and the Net worth forecast. Change the period with the slider.
5. Check the Payout forecast for the expected income per month.
6. Adjust the funds and their assumptions on the Funds and assumptions tab.
7. Save your scenario from the gear menu, or export it as CSV or PDF.

The app also has a built-in guide: open the gear menu and choose "How to use it".

## Features

- **Investment forecast**: value over time for the dividend and accumulating parts, with the total return per year.
- **Net worth forecast**: value after estimated Box 3 tax, with where the money went: payouts, tax and fund costs. Shows how long it takes to double your net investment.
- **Payout forecast**: expected income per month and per year from the dividend funds, with the cumulative total.
- **Tax**: per-country estimates for the Netherlands (Box 3), the United States (withholding tax), Argentina (foreign assets), Venezuela and a number of other countries, each with a note on its source and reliability.
- **Funds and assumptions**: the funds in the model with yield, price growth, TER and risk, plus the weight per fund. All values are editable.
- **Strategies**: defensive, balanced and aggressive presets for the split and the fund weights.
- **Scenarios**: low, base and high, which adjust the price growth and yield assumptions.
- **Saved scenarios and export**: save named scenarios in the browser, export a CSV, or print to PDF.
- **Cost warning**: a warning when the weighted TER of your mix goes above 0.40%.
- Dutch, English and Spanish, with a light and a dark theme.

## How it works

The model is deliberately simple. Each fund grows with its price growth minus its TER. The yield of a dividend fund is paid out each year, either reinvested or paid out to you. Scenarios add or subtract a fixed number of percentage points to growth and yield.

Your inputs are saved in your own browser's local storage. There is no server, no account and no tracking.

Fund data (yields, price growth, TER, US share of holdings) are estimates entered by hand. They are not live market data. Check them against the fund providers before you rely on them.

The tax estimates are rough. Box 3 uses the tax-free allowance and the flat return from the tax tab. Withholding tax and foreign tax are approximations. Figures for Argentina and Venezuela are estimates and should be verified with the tax authority.

Payouts are spread evenly over the twelve months. Real funds pay out irregularly.

## Disclaimer

This is a scenario tool, not a forecast and not financial or tax advice. Past returns do not predict future results. Verify all figures yourself before making decisions.

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE). You may use, study, share and modify the code. If you modify it and make it available to others, including as a network service, you must share your modified source under the same license.
