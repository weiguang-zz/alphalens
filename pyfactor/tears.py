from plotting import *
import performance as perf
import utils
import pandas as pd


def create_factor_tear_sheet(factor,
                             prices,
                             sectors=None,
                             sector_plots=True,
                             days=(1, 5, 10)
                             ):
    """

    Creates a full tear sheet for analysis and evaluating single return predicting (alpha) factors.

    Parameters
    ----------
    factor : pd.Series - MultiIndex
        A MultiIndex Series indexed by date and equity, containing the values for a single alpha factor.
    prices : pd.DataFrame
        A long form Pandas DataFrame indexed by date with equities in the columns.
    sectors : pd.Series - MultiIndex
        A MultiIndex Series indexed by date and equity, containing the sector codes for each equity.
    sector_plots : boolean
        If True create sector specific plots.
    days: list
        Days to compute forward returns on.

    """

    can_sector_adjust = sectors is not None
    factor, forward_returns = utils.format_input_data(factor, prices, sectors, days)

    daily_ic, _ = perf.factor_information_coefficient(factor, forward_returns,
                                                      sector_adjust=can_sector_adjust,
                                                      by_sector=False)

    quintile_factor = perf.quantize_factor(factor, by_sector=False, quantiles=5)
    decile_factor = perf.quantize_factor(factor, by_sector=False, quantiles=10)

    mean_ret_by_quintile = perf.mean_daily_return_by_factor_quantile(quintile_factor,
                                                                     forward_returns,
                                                                     by_sector=False)
    mean_ret_by_decile = perf.mean_daily_return_by_factor_quantile(decile_factor,
                                                                   forward_returns,
                                                                   by_sector=False)

    # What is the sector-netural rolling mean IC for our different forward price windows?
    plot_daily_ic_ts(daily_ic)
    plot_daily_ic_hist(daily_ic)

    # What are the sector-neutral factor quantile mean returns for our different forward price windows?
    plot_quantile_returns_bar(mean_ret_by_quintile, by_sector=False)
    plot_quantile_returns_bar(mean_ret_by_decile, by_sector=False)

    # How much are the contents of the the top and bottom quintile changing each day?
    plot_top_bottom_quantile_turnover(quintile_factor)
    plot_factor_rank_auto_correlation(factor)

    # Sector Specific Breakdown
    if can_sector_adjust and sector_plots:
        ic_by_sector, _ = perf.mean_information_coefficient(factor, forward_returns, by_sector=True)
        quintile_factor_by_sector = perf.quantize_factor(factor, by_sector=True, quantiles=5)

        plot_ic_by_sector(ic_by_sector)

        plot_quantile_returns_bar(quintile_factor_by_sector, by_sector=True)
