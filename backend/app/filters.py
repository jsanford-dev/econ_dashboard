# filters.py
def clean_label(label):
    return (
        label.strip()
             .lower()
             .replace('10y', 'teny')
             .replace('(', '')
             .replace(')', '')
             .replace('%', '')
             .replace("'", '')
             .replace('.', '')
             .replace(' ', '-')
             .rstrip('-')
    )