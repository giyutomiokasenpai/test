import pytest
from main import headers_filter, read_csv, payout_counter, print_report, error_check_file, pars_parameters, main

def test_pars_parameters_valid(monkeypatch):
    monkeypatch.setattr('sys.argv', ['prog', 'file1.csv', '--report', 'payout'])
    files = pars_parameters()
    assert files == ['file1.csv']

def test_print_report_output(capfd):
    report = {
        'Sales': [
            {'name': 'Alice', 'hours_worked': 10, 'hourly_rate': 15, 'payout': 150},
        ]
    }
    print_report(report)
    out, _ = capfd.readouterr()
    assert 'Sales' in out
    assert 'Alice' in out
    assert '150$' in out

def test_headers_filter_basic():
    headers = ['ID', 'Name', 'Rate']
    expected = ['id', 'name', 'hourly_rate']
    assert headers_filter(headers) == expected

def test_payout_counter_basic():
    data = [
        {'name': 'Alice', 'hours_worked': 10, 'hourly_rate': 15, 'department': 'Sales', 'id': 1},
        {'name': 'Bob', 'hours_worked': 20, 'hourly_rate': 10, 'department': 'Sales', 'id': 2},
    ]
    report = payout_counter(data)
    assert 'Sales' in report
    assert report['Sales'][0]['payout'] == 150

def test_read_csv(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text("ID,Name,Hours_Worked,Rate,Department\n1,Alice,10,15,Sales\n", encoding='utf-8')
    data = read_csv(str(file))
    assert data[0]['id'] == 1
    assert data[0]['hours_worked'] == 10

def test_error_check_file_not_found():
    assert error_check_file('non_existent.csv') is None

def test_main(monkeypatch, capfd):
    monkeypatch.setattr('main.pars_parameters', lambda: ['file.csv'])
    monkeypatch.setattr('main.error_check_file', lambda f: [
        {'name': 'Alice', 'hours_worked': 10, 'hourly_rate': 15, 'department': 'Sales', 'id': 1}
    ])
    monkeypatch.setattr('main.print_report', lambda report: print("Report printed"))

    main()
    out, _ = capfd.readouterr()
    assert 'Report printed' in out