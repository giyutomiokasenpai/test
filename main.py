import argparse
from filter import FIELD_ALIASES

def pars_parameters() -> list[str]:
    '''
    Parses command-line arguments.

    Returns:
        list[str]: List of input CSV files.
    '''
    parser = argparse.ArgumentParser(description='Read and process employee payout report.')
    parser.add_argument('files', nargs='+', help='Path to one or more CSV files.')
    parser.add_argument('--report', type=str, required=True, choices=['payout'], help='Type of report to generate.')
    args = parser.parse_args()

    data = []
    if args.report == 'payout':
        return args.files


def headers_filter(headers: list[str]) -> list[str]:
    '''yto
    Filters headers in the given list by alias words.

    Args:
        headers(list[str]): List of headers.

    Returns:
        list[str]: List of filtered header keys based on known aliases.
    '''
    filtered = []
    for header in headers:
        filtered_header = header.strip().lower()
        for key, value in  FIELD_ALIASES.items():
            if any(filtered_header == alias.lower() for alias in value):
                filtered.append(key)

    return filtered

def read_csv(filename: str) -> list[dict]:
    '''
    Reads the given CSV file.

    Args:
        filename(str): Path to the CSV file.

    Returns:
        list[dict]: List of employee dictionaries: 
    '''
    with open(filename, 'r', encoding='utf-8')as file:
        lines = file.readlines()        

    data = []
    headers = headers_filter(lines[0].strip().split(','))
    for line in lines[1:]:
        values = line.strip().split(',')
        row = dict(zip(headers, values))    
        row['id'] = int(row.get('id', 0))
        row['hours_worked'] = int(row.get('hours_worked', 0))
        row['hourly_rate'] = int(row.get('hourly_rate', 0))
        data.append(row)
    return data


def payout_counter(data: list[dict]) -> dict[str, list[dict]]:
    '''
    Calculates payout for each employee in the given data list.

    Args:
        data(list[dict]): List of employee dictionaries.

    Returns:
        dict[str, list[dict]]: Dictionary with department as key and list of employees as value.
    '''

    report = {}
    for employee in data:
        employee['payout'] = employee.get('hours_worked', 0) * employee.get('hourly_rate', 0)
        department = employee.pop('department')
        if department not in report:
            report[department] = []
        report[department].append(employee)

    return report

def print_report(report: dict[str, list[dict]]) -> None:
    '''
    Prints the given report.

    Args:
        report(dict[str, list[dict]]): Dictionary where keys are departments names, and values are list of employee dictionaries.
    '''

    print(f"{'name':>40} {'hours_worked':>20} {'hourly_rate':>20} {'payout':>20}")
    for department, employees in report.items():
        print(f'{department}')
        for emp in employees:
            print(f'{emp.get("name"):>40} {emp.get("hours_worked"):>20} {emp.get("hourly_rate"):>20} {emp.get("payout"):>20}$')
        total_hours = sum(emp.get('hours_worked') for emp in employees)
        total_payout = sum(emp.get('payout') for emp in employees)
        print(f'{total_hours:>61} {total_payout:>41}$')

def error_check_file(filename: str) -> list[dict] | None: 
    '''
    Detects error and prints it with reading the CSV file.

    Args:
        filename(str): Path to the CSV file.

    Returns:
        list[dict] | None: The readen data if file is correct, else None.
    '''
    try:
        file_data = read_csv(filename)
        if not file_data:
            print(f'The file {filename} is empty.')
            return None
        return file_data
    except FileNotFoundError:
        print(f'File {filename} not found.')
    except ValueError as ve:
        print(f'File {filename} data error: {ve}.')
    except Exception as e:
        print(f'Failed to process the file: {filename}.')
    return None

def main() -> None:
    filenames_list = pars_parameters()
    
    for filename in filenames_list:
        file_data = error_check_file(filename)
        if file_data is not None:
            report = payout_counter(file_data)
            print_report(report)

if __name__ == '__main__':
    main()  