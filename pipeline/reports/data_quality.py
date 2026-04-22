import os
import pandas as pd

def run_data_quality():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    report_path = os.path.join(docs_dir, 'data_quality_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Relatório de Qualidade de Dados (Northwind)\n\n")
        f.write("Este documento apresenta uma análise básica da qualidade dos dados extraídos dos arquivos CSV.\n\n")
        
        for file in os.listdir(data_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(data_dir, file)
                try:
                    df = pd.read_csv(file_path, sep=';', encoding='utf-8')
                    f.write(f"## {file}\n")
                    f.write(f"- **Total de Linhas:** {len(df)}\n")
                    f.write(f"- **Total de Colunas:** {len(df.columns)}\n\n")
                    
                    f.write("### Colunas e Valores Nulos\n")
                    f.write("| Coluna | Tipo | Valores Nulos | % Nulos |\n")
                    f.write("|--------|------|---------------|----------|\n")
                    for col in df.columns:
                        nulls = df[col].isnull().sum()
                        pct = (nulls / len(df)) * 100 if len(df) > 0 else 0
                        dtype = str(df[col].dtype)
                        f.write(f"| {col} | {dtype} | {nulls} | {pct:.2f}% |\n")
                    
                    f.write("\n---\n\n")
                except Exception as e:
                    f.write(f"## {file}\n")
                    f.write(f"Erro ao ler o arquivo: {e}\n\n")

if __name__ == '__main__':
    run_data_quality()
    print("Relatório de Data Quality gerado em docs/data_quality_report.md")
