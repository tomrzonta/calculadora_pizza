import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys

# --- Funções de Lógica ---

def reiniciar_calculadora():
    """Limpa todos os campos de entrada e a área de resultados."""
    entry_total_partes.delete(0, tk.END)
    entry_valor_uma_parte.delete(0, tk.END)
    texto_resultados.config(state=tk.NORMAL)
    texto_resultados.delete('1.0', tk.END)
    texto_resultados.config(state=tk.DISABLED)
    entry_total_partes.focus_set()

def calcular_fracoes():
    """
    Lógica Definitiva:
    1. Calcula o valor total do produto (o "inteiro").
    2. Com o valor total, calcula as possíveis divisões por sabores.
    """
    try:
        # Pega os valores dos campos de entrada
        total_partes_str = entry_total_partes.get()
        valor_uma_parte_str = entry_valor_uma_parte.get().replace(',', '.')

        if not total_partes_str or not valor_uma_parte_str:
            messagebox.showerror("Erro de Entrada", "Por favor, preencha todos os campos.")
            return

        total_partes = int(total_partes_str)
        valor_uma_parte = float(valor_uma_parte_str)

        if total_partes <= 0 or valor_uma_parte <= 0:
            messagebox.showerror("Erro de Valor", "Os valores devem ser maiores que zero.")
            return

        # --- PASSO 1: CALCULAR O VALOR DO INTEIRO ---
        valor_do_inteiro = total_partes * valor_uma_parte

        # Prepara a área de resultados para atualização
        texto_resultados.config(state=tk.NORMAL)
        texto_resultados.delete('1.0', tk.END)

        # Adiciona uma linha informativa sobre o valor total calculado
        info_total = f"Valor total do produto calculado: R$ {valor_do_inteiro:.2f}\n\n"
        texto_resultados.insert(tk.END, info_total)

        # --- PASSO 2: CALCULAR AS DIVISÕES ---
        cabecalho = " Divisão   | Valor por Sabor (R$) | Percentual\n"
        separador = "-----------|----------------------|-----------\n"
        tabela = cabecalho + separador

        # Loop para calcular e formatar a tabela de divisões
        # A divisão vai até o número total de partes do produto
        for i in range(1, total_partes + 1):
            valor_por_sabor = valor_do_inteiro / i
            percentual = 100.0 / i

            # Formata a linha para alinhar as 3 colunas
            col1 = f"{i} Sabor(es)".ljust(9)
            col2 = f'{valor_por_sabor:.2f}'.rjust(20)
            col3 = f'{percentual:.2f}%'.rjust(10)
            
            linha = f" {col1} | {col2} | {col3}\n"
            tabela += linha

        # Insere a tabela e desabilita a edição
        texto_resultados.insert(tk.END, tabela)
        texto_resultados.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Erro de Formato", "Por favor, insira apenas números válidos.")
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

# --- Configuração da Interface Gráfica ---
janela = tk.Tk()
janela.title("Calculadora de Frações (Nova Lógica)")
janela.geometry("480x620") # Janela um pouco maior
janela.resizable(False, False)

# Imagem
try:
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(base_path, 'pizza.png')
    img_original = Image.open(image_path)
    img_redimensionada = img_original.resize((150, 150), Image.LANCZOS)
    img_pizza = ImageTk.PhotoImage(img_redimensionada)
    label_imagem = tk.Label(janela, image=img_pizza)
    label_imagem.pack(pady=10)
except Exception:
    label_imagem_fallback = tk.Label(janela, text="Imagem 'pizza.png' não encontrada", fg="red")
    label_imagem_fallback.pack(pady=10)

# Frame de Entradas
frame_entradas = tk.Frame(janela)
frame_entradas.pack(pady=10)

# --- RÓTULOS NOVOS E MAIS CLAROS ---
label_total_partes = tk.Label(frame_entradas, text="O produto se divide em quantas partes?")
label_total_partes.grid(row=0, column=0, padx=5, sticky="w")
entry_total_partes = tk.Entry(frame_entradas, width=12)
entry_total_partes.grid(row=0, column=1, padx=5)

label_valor_uma_parte = tk.Label(frame_entradas, text="Qual o valor de UMA parte (R$)?")
label_valor_uma_parte.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_valor_uma_parte = tk.Entry(frame_entradas, width=12)
entry_valor_uma_parte.grid(row=1, column=1, padx=5)

# Frame de Botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

botao_calcular = tk.Button(frame_botoes, text="Calcular", command=calcular_fracoes, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=10)
botao_calcular.pack(side=tk.LEFT, padx=10)
botao_reiniciar = tk.Button(frame_botoes, text="Reiniciar", command=reiniciar_calculadora, font=("Arial", 12), bg="#f44336", fg="white", width=10)
botao_reiniciar.pack(side=tk.LEFT, padx=10)

# Área de Resultados
label_resultados = tk.Label(janela, text="Tabela de Divisão de Sabores:", font=("Arial", 11, "bold"))
label_resultados.pack()
texto_resultados = tk.Text(janela, height=12, width=55, state=tk.DISABLED, font=("Courier", 11), bg="#f0f0f0")
texto_resultados.pack(pady=10, padx=10)

janela.mainloop()