from freezegun import freeze_time

from quark.views.record.schemas.record_list_request import record_list_request_schema


class TestRecord:
    @freeze_time('2023-06-19')
    def test_record_list_request(self):
        form = record_list_request_schema.load({})
        assert form['year'].year == 2023
