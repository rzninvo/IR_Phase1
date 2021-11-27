import pandas as pd
from IR_phase1 import IR

if __name__ == '__main__':
    data = pd.read_excel(r'IR.xlsx')
    content = data['content'].tolist()
    titles = data['title'].tolist()
    positional_index = IR().get_positional_index(content)
    query = input()
    query_results = IR().search(query, positional_index)
    IR().print_result(query_results, titles)