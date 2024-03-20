from datetime import datetime
from decimal import Decimal

from quark.services.chart import category_trend as category_trend_svc


class TestChart:
    def test_make_monthly_trend(self):
        rows = [
            category_trend_svc.TrendRow('202301', 1, 'CMB', Decimal(100)),
            category_trend_svc.TrendRow('202301', 2, 'Alipay', Decimal(200)),
            category_trend_svc.TrendRow('202301', 3, 'Snowball', Decimal(-300)),
            category_trend_svc.TrendRow('202301', 4, 'ICBC', Decimal(10)),
        ]
        result = category_trend_svc.make_monthly_trend(
            rows, datetime(2023, 1, 1), datetime(2023, 12, 31), 2)

        assert result['categories'][0]['name'] == 'Snowball'
        assert result['categories'][1]['name'] == 'Alipay'
        assert result['categories'][2]['name'] == 'Other'
        assert result['data'][0]['category_0'] == 110
