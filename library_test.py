import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    def test_extract_date(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, "2015-07-25")

    def test_extract_date_no_date(self):
        self.assert_extract('I was born on.', library.dates_iso8601)

    def test_extract_date_m_gt_12(self):
        self.assert_extract('I was born on 2015-13-25.', library.dates_iso8601)

    def test_extract_date_d_gt_31(self):
        self.assert_extract('I was born on 2015-07-32.', library.dates_iso8601)

    def test_extract_date_short_mon_format(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_short_mon, "25 Jan 2017")

    def test_extract_date_short_mon_format_no_date(self):
        self.assert_extract('I was born on .', library.dates_short_mon)

    def test_extract_date_short_mon_format_Apr(self):
        self.assert_extract('I was born on 25 Apr 2017.', library.dates_short_mon, "25 Apr 2017")

    def test_extract_date_short_mon_format_Jan(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_short_mon, "25 Jan 2017")

    def test_extract_date_short_mon_format_Jun(self):
        self.assert_extract('I was born on 25 Jun 2017.', library.dates_short_mon, "25 Jun 2017")

    def test_extract_date_short_mon_format_Mar(self):
        self.assert_extract('I was born on 25 Mar 2017.', library.dates_short_mon, "25 Mar 2017")

    def test_extract_date_short_mon_format_May(self):
        self.assert_extract('I was born on 25 May 2017.', library.dates_short_mon, "25 May 2017")

    def test_iso8601_with_ts_min_w(self):
        self.assert_extract('I was born on 2018-06-22 18:22. I was born', library.dates_iso8601, "2018-06-22 18:22")

    def test_iso8601_with_ts_min_t(self):
        self.assert_extract('I was born on 2018-06-22T18:22. I was born', library.dates_iso8601, "2018-06-22T18:22")

    def test_iso8601_with_ts_sec_w(self):
        self.assert_extract('I was born on 2018-06-22 18:22:11. I was born', library.dates_iso8601, "2018-06-22 18:22:11")

    def test_iso8601_with_ts_sec_t(self):
        self.assert_extract('I was born on 2018-06-22T18:22:22. I was born', library.dates_iso8601, "2018-06-22T18:22:22")

    def test_iso8601_with_ts_msec_w(self):
        self.assert_extract('I was born on 2018-06-22 18:22:11.123. I was born', library.dates_iso8601, "2018-06-22 18:22:11.123")

    def test_iso8601_with_ts_msec_t(self):
        self.assert_extract('I was born on 2018-06-22T18:22:22.123. I was born', library.dates_iso8601, "2018-06-22T18:22:22.123")

    def test_iso8601_with_ts_wrong_h(self):
        self.assert_extract('I was born on 2018-06-22 30:22:11.123. I was born', library.dates_iso8601)

    def test_iso8601_with_ts_wrong_m(self):
        self.assert_extract('I was born on 2018-06-22 18:70:22.123. I was born', library.dates_iso8601)

    def test_iso8601_with_ts_wrong_s(self):
        self.assert_extract('I was born on 2018-06-22 18:22:90.123. I was born', library.dates_iso8601)

    def test_iso8601_with_ts_wrong_ms(self):
        self.assert_extract('I was born on 2018-06-22 18:22:22.adf. I was born', library.dates_iso8601)

    def test_iso8601_with_ts_min_w_tz_offset(self):
        self.assert_extract('I was born on 2018-06-22 18:22-0800. I was born', library.dates_iso8601, "2018-06-22 18:22-0800")

    def test_iso8601_with_ts_min_t_tz_offset(self):
        self.assert_extract('I was born on 2018-06-22T18:22+0800. I was born', library.dates_iso8601, "2018-06-22T18:22+0200")

    def test_iso8601_with_ts_sec_w_tz_offset(self):
        self.assert_extract('I was born on 2018-06-22 18:22:11-0800. I was born', library.dates_iso8601, "2018-06-22 18:22:11-0800")

    def test_iso8601_with_ts_sec_t_tz_offset(self):
        self.assert_extract('I was born on 2018-06-22T18:22:22+0100. I was born', library.dates_iso8601, "2018-06-22T18:22:22+0100")

    def test_iso8601_with_ts_msec_w_tz_offset(self):
        self.assert_extract('I was born on 2018-06-22 18:22:11.123-0800. I was born', library.dates_iso8601, "2018-06-22 18:22:11.123-0800")

    def test_iso8601_with_ts_msec_t_tz_offset(self):
        self.assert_extract('I was born on 2018-06-22T18:22:22.123+0100. I was born', library.dates_iso8601, "2018-06-22T18:22:22.123+0100")

    def test_iso8601_with_ts_wrong_tz_offset_sep(self):
        self.assert_extract('I was born on 2018-06-22 10:22:11.123|0800. I was born', library.dates_iso8601)

    def test_iso8601_with_ts_wrong_tz_offset(self):
        self.assert_extract('I was born on 2018-06-22 18:10:22.123-9999. I was born', library.dates_iso8601)

    def test_iso8601_with_ts_tz_letter(self):
        self.assert_extract('I was born on 2018-06-22 18:22:10.123UTC. I was born', library.dates_iso8601, "2018-06-22 18:22:10.123UTC")

    def test_iso8601_with_ts_tz_wrong_letter(self):
        self.assert_extract('I was born on 2018-06-22 18:22:22.123asdf. I was born', library.dates_iso8601)

    def test_extract_date_short_mon_com(self):
        self.assert_extract('I was born on 25 Jan, 2017.', library.dates_short_mon, "25 Jan, 2017")

    def test_extract_int_com_sep(self):
        self.assert_extract('I was born on 25,000,000.', library.integers, "25,000,000")

    def test_extract_int_com_sep_wrong(self):
        self.assert_extract('I was born on 25,0,0,0,000.', library.integers)


if __name__ == '__main__':
    unittest.main()
