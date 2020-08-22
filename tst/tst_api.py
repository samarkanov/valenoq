import os
import unittest
from valenoq.api import config, request
from pdb import set_trace as stop


class ApiGetSingleTickerOHCLVTest(unittest.TestCase):

    def setUp(self):
        self.ticker = "TSLA"

    def tearDown(self):
        pass

    #@unittest.skip("")
    def testIntradayDay_gw(self):
        print("== ApiGetSingleTickerOHCLVTest: testIntradayDay_gw ==")

        data = request.get(self.ticker, date="2018-05-01", frequency="day")
        self.assertEqual(len(data), 1)
        self.assertEqual(set(data.ticker), set([self.ticker]))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[0].strftime("%Y%m%d%H"), "2018050100")
        self.assertEqual(int(data.close.mean()), 299)
        self.assertEqual(int(data.vol.mean()), 4625600)

        data_2 = request.get(self.ticker, date="2018-05-01", frequency="day")
        self.assertTrue(data_2.equals(data))

        data_3 = request.get(self.ticker, start="2018-05-01", end="2018-05-01", frequency="day")
        self.assertTrue(data_3.equals(data))

        data_4 = request.get(self.ticker, start="2018-05-01", end="2018-05-01", frequency="day")
        self.assertTrue(data_4.equals(data))

    #@unittest.skip("")
    def testIntradayHour_gw(self):
        print("== ApiGetSingleTickerOHCLVTest: testIntradayHour_gw ==")

        data = request.get(self.ticker, date="2018-05-01")
        self.assertEqual(len(data), 8)
        self.assertEqual(set(data.ticker), set([self.ticker]))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[0].strftime("%Y%m%d%H"), "2018050109")
        self.assertEqual(int(data.close.mean()), 297)
        self.assertEqual(int(data.vol.mean()), 413927)

        data_2 = request.get(self.ticker, date="2018-05-01", frequency="hour")
        self.assertTrue(data_2.equals(data))

        data_3 = request.get(self.ticker, start="2018-05-01", end="2018-05-01")
        self.assertTrue(data_3.equals(data))

        data_4 = request.get(self.ticker, start="2018-05-01", end="2018-05-01", frequency="hour")
        self.assertTrue(data_4.equals(data))

    #@unittest.skip("")
    def testIntraday_Default_Minute_gw(self):
        print("== ApiGetSingleTickerOHCLVTest: testIntraday_Default_Minute_gw ==")

        data = request.get(self.ticker, date="2018-05-01", frequency="minute")
        self.assertEqual(len(data), 95)
        self.assertEqual(set(data.ticker), set([self.ticker]))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[0].strftime("%Y%m%d%H"), "2018050109")
        self.assertEqual(int(data.close.mean()), 296)
        self.assertEqual(int(data.vol.mean()), 34670)

        data_2 = request.get(self.ticker, date="2018-05-01", frequency="minute")
        self.assertTrue(data_2.equals(data))

        data_3 = request.get(self.ticker, start="2018-05-01", end="2018-05-01", frequency="minute")
        self.assertTrue(data_3.equals(data))

    #@unittest.skip("")
    def testIntraday_1_Minute_gw(self):
        print("== ApiGetSingleTickerOHCLVTest: testIntraday_1_Minute_gw ==")

        data = request.get(self.ticker, date="2018-05-01", frequency="minute", collapse=1)
        self.assertEqual(len(data), 424)
        self.assertEqual(set(data.ticker), set([self.ticker]))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[0].strftime("%Y%m%d%H"), "2018050109")
        self.assertEqual(int(data.close.mean()), 296)
        self.assertEqual(int(data.vol.mean()), 8057)

        data_2 = request.get(self.ticker, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=1)
        self.assertTrue(data_2.equals(data))

    #@unittest.skip("")
    def testIntraday_5_Minute_gw(self):
        print("== ApiGetSingleTickerOHCLVTest: testIntraday_5_Minute_gw ==")

        data = request.get(self.ticker, date="2018-05-01", frequency="minute", collapse=5)
        self.assertEqual(len(data), 95)
        self.assertEqual(set(data.ticker), set([self.ticker]))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[4].strftime("%Y%m%d %H%M"), "20180501 0920")
        self.assertEqual(int(data.close.mean()), 296)
        self.assertEqual(int(data.vol.mean()), 34670)

        data_2 = request.get(self.ticker, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=5)
        self.assertTrue(data_2.equals(data))

    #@unittest.skip("")
    def testIntraday_10_Minute_gw(self):
        print("== ApiGetSingleTickerOHCLVTest: testIntraday_10_Minute_gw ==")

        data = request.get(self.ticker, date="2018-05-01", frequency="minute", collapse=10)
        self.assertEqual(len(data), 48)
        self.assertEqual(set(data.ticker), set([self.ticker]))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[4].strftime("%Y%m%d %H%M"), "20180501 0950")
        self.assertEqual(int(data.close.mean()), 296)
        self.assertEqual(int(data.vol.mean()), 71175)

        data_2 = request.get(self.ticker, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=10)
        self.assertTrue(data_2.equals(data))

    #@unittest.skip("")
    def testIntraday_15_Minute_gw(self):
        print("== ApiGetSingleTickerOHCLVTest: testIntraday_15_Minute_gw ==")

        data = request.get(self.ticker, date="2018-05-01", frequency="minute", collapse=15)
        self.assertEqual(len(data), 32)
        self.assertEqual(set(data.ticker), set([self.ticker]))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[5].strftime("%Y%m%d %H%M"), "20180501 1030")
        self.assertEqual(int(data.close.mean()), 296)
        self.assertEqual(int(data.vol.mean()), 106763)

        data_2 = request.get(self.ticker, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=15)
        self.assertTrue(data_2.equals(data))

    #@unittest.skip("")
    def testIntraday_30_Minute_gw(self):
        print("== ApiGetSingleTickerOHCLVTest: testIntraday_30_Minute_gw ==")

        data = request.get(self.ticker, date="2018-05-01", frequency="minute", collapse=30)
        self.assertEqual(len(data), 16)
        self.assertEqual(set(data.ticker), set([self.ticker]))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[-1].strftime("%Y%m%d %H%M"), "20180501 1700")
        self.assertEqual(int(data.close.mean()), 296)
        self.assertEqual(int(data.vol.mean()), 213527)

        data_2 = request.get(self.ticker, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=30)
        self.assertTrue(data_2.equals(data))


class ApiGetListTickersOHCLVTest(unittest.TestCase):

    def setUp(self):
        self.tickers = ["AAPL", "MU"]

    def tearDown(self):
        pass

    #@unittest.skip("")
    def testIntradayDay_gw(self):
        print("== ApiGetListTickersOHCLVTest: testIntradayDay_gw ==")

        data = request.get(self.tickers, date="2018-05-01", frequency="day")
        self.assertEqual(len(data), 2)
        self.assertEqual(set(data.ticker), set(self.tickers))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[0].strftime("%Y%m%d%H"), "2018050100")
        self.assertEqual(data.index[1].strftime("%Y%m%d%H"), "2018050100")
        self.assertEqual(int(data[data.ticker=="MU"].close.mean()), 46)
        self.assertEqual(int(data[data.ticker=="AAPL"].close.mean()), 169)
        self.assertEqual(int(data[data.ticker=="MU"].vol.mean()), 34154900)
        self.assertEqual(int(data[data.ticker=="AAPL"].vol.mean()), 53569300)

        data_2 = request.get(self.tickers, date="2018-05-01", frequency="day")
        self.assertTrue(data_2.equals(data))

        data_3 = request.get(self.tickers, start="2018-05-01", end="2018-05-01", frequency="day")
        self.assertTrue(data_3.equals(data))

        data_4 = request.get(self.tickers, start="2018-05-01", end="2018-05-01", frequency="day")
        self.assertTrue(data_4.equals(data))

    #@unittest.skip("")
    def testIntradayHour_gw(self):
        print("== ApiGetListTickersOHCLVTest: testIntradayHour_gw ==")

        data = request.get(self.tickers, date="2018-05-01")
        self.assertEqual(len(data), 16)
        self.assertEqual(set(data.ticker), set(self.tickers))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[0].strftime("%Y%m%d%H"), "2018050109")
        self.assertEqual(int(data[data.ticker=="MU"].close.mean()), 46)
        self.assertEqual(int(data[data.ticker=="AAPL"].close.mean()), 168)
        self.assertEqual(int(data[data.ticker=="MU"].vol.mean()), 3625867)
        self.assertEqual(int(data[data.ticker=="AAPL"].vol.mean()), 4772560)

        data_2 = request.get(self.tickers, date="2018-05-01", frequency="hour")
        self.assertTrue(data_2.equals(data))

        data_3 = request.get(self.tickers, start="2018-05-01", end="2018-05-01")
        self.assertTrue(data_3.equals(data))

        data_4 = request.get(self.tickers, start="2018-05-01", end="2018-05-01", frequency="hour")
        self.assertTrue(data_4.equals(data))

    #@unittest.skip("")
    def testIntraday_Default_Minute_gw(self):
        print("== ApiGetListTickersOHCLVTest: testIntraday_Default_Minute_gw ==")

        data = request.get(self.tickers, date="2018-05-01", frequency="minute")
        self.assertEqual(len(data), 192)
        self.assertEqual(set(data.ticker), set(self.tickers))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[0].strftime("%Y%m%d%H"), "2018050109")
        self.assertEqual(int(data[data.ticker=="MU"].close.mean()), 46)
        self.assertEqual(int(data[data.ticker=="AAPL"].close.mean()), 168)
        self.assertEqual(int(data[data.ticker=="MU"].vol.mean()), 303816)
        self.assertEqual(int(data[data.ticker=="AAPL"].vol.mean()), 433039)

        data_2 = request.get(self.tickers, date="2018-05-01", frequency="minute")
        self.assertTrue(data_2.equals(data))

        data_3 = request.get(self.tickers, start="2018-05-01", end="2018-05-01", frequency="minute")
        self.assertTrue(data_3.equals(data))

    #@unittest.skip("")
    def testIntraday_1_Minute_gw(self):
        print("== ApiGetListTickersOHCLVTest: testIntraday_1_Minute_gw ==")

        data = request.get(self.tickers, date="2018-05-01", frequency="minute", collapse=1)
        self.assertEqual(len(data), 952)
        self.assertEqual(set(data.ticker), set(self.tickers))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[0].strftime("%Y%m%d%H"), "2018050109")
        self.assertEqual(int(data[data.ticker=="MU"].close.mean()), 46)
        self.assertEqual(int(data[data.ticker=="AAPL"].close.mean()), 168)

        data_2 = request.get(self.tickers, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=1)
        self.assertTrue(data_2.equals(data))

    #@unittest.skip("")
    def testIntraday_5_Minute_gw(self):
        print("== ApiGetListTickersOHCLVTest: testIntraday_5_Minute_gw ==")

        data = request.get(self.tickers, date="2018-05-01", frequency="minute", collapse=5)
        self.assertEqual(len(data), 192)
        self.assertEqual(set(data.ticker), set(self.tickers))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[4].strftime("%Y%m%d %H%M"), "20180501 0920")
        self.assertEqual(int(data[data.ticker=="MU"].close.mean()), 46)
        self.assertEqual(int(data[data.ticker=="AAPL"].close.mean()), 168)

        data_2 = request.get(self.tickers, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=5)
        self.assertTrue(data_2.equals(data))

    #@unittest.skip("")
    def testIntraday_10_Minute_gw(self):
        print("== ApiGetListTickersOHCLVTest: testIntraday_10_Minute_gw ==")

        data = request.get(self.tickers, date="2018-05-01", frequency="minute", collapse=10)
        self.assertEqual(len(data), 96)
        self.assertEqual(set(data.ticker), set(self.tickers))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[4].strftime("%Y%m%d %H%M"), "20180501 0950")
        self.assertEqual(int(data[data.ticker=="MU"].close.mean()), 46)
        self.assertEqual(int(data[data.ticker=="AAPL"].close.mean()), 168)

        data_2 = request.get(self.tickers, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=10)
        self.assertTrue(data_2.equals(data))

    #@unittest.skip("")
    def testIntraday_15_Minute_gw(self):
        print("== ApiGetListTickersOHCLVTest: testIntraday_15_Minute_gw ==")

        data = request.get(self.tickers, date="2018-05-01", frequency="minute", collapse=15)
        self.assertEqual(len(data), 64)
        self.assertEqual(set(data.ticker), set(self.tickers))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[5].strftime("%Y%m%d %H%M"), "20180501 1030")
        self.assertEqual(int(data[data.ticker=="MU"].close.mean()), 46)
        self.assertEqual(int(data[data.ticker=="AAPL"].close.mean()), 168)

        data_2 = request.get(self.tickers, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=15)
        self.assertTrue(data_2.equals(data))

    #@unittest.skip("")
    def testIntraday_30_Minute_gw(self):
        print("== ApiGetListTickersOHCLVTest: testIntraday_30_Minute_gw ==")

        data = request.get(self.tickers, date="2018-05-01", frequency="minute", collapse=30)
        self.assertEqual(len(data), 32)
        self.assertEqual(set(data.ticker), set(self.tickers))
        self.assertEqual(data.index.name, "dt")
        self.assertEqual(data.index[-1].strftime("%Y%m%d %H%M"), "20180501 1700")
        self.assertEqual(int(data[data.ticker=="MU"].close.mean()), 46)
        self.assertEqual(int(data[data.ticker=="AAPL"].close.mean()), 168)

        data_2 = request.get(self.tickers, start="2018-05-01", end="2018-05-01", frequency="minute", collapse=30)
        self.assertTrue(data_2.equals(data))


class ApiGetBalanceSheetTest(unittest.TestCase):

    def setUp(self):
        self.ticker = "TSLA"
        self.tickers_list = ["AAPL", "MU", "ASML", "INTC", "EBAY"]

    def tearDown(self):
        pass

    #@unittest.skip("")
    def test_1quarter_1ticker(self):
        print("== ApiGetBalanceSheetTest: test_1quarter_1ticker ==")
        data = request.balance_sheet(self.ticker)
        self.assertEqual(len(data), 1)
        self.assertEqual(float(data["current_cash"]), 8818000000)

    #@unittest.skip("")
    def test_12quarters_1ticker(self):
        print("== ApiGetBalanceSheetTest: test_12quarters_1ticker ==")
        data = request.balance_sheet(self.ticker, nr_quarters=12)
        self.assertEqual(len(data), 12)
        self.assertEqual(int(data["current_cash"].loc["2020-06-30"]), 8818000000)

    #@unittest.skip("")
    def test_1quarter_5tickers(self):
        print("== ApiGetBalanceSheetTest: test_1quarter_5tickers ==")
        data = request.balance_sheet(self.tickers_list)
        self.assertEqual(len(data), 5)
        self.assertEqual(int(data["accounts_payable"].mean()), 8581800000)


if __name__ == "__main__":
    config.set(api_key=os.getenv("VALENOQ_API_KEY"))
    unittest.main()
