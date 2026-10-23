# 🧮 Calculadora Neon

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Concluído](https://img.shields.io/badge/Status-Concluído-brightgreen)](https://github.com/KBlester)

Uma calculadora moderna com interface gráfica em Python, visual dark-mode com accents neon, histórico persistente e funcionalidades de memória.

Desenvolvido por **[Kalebe Santos](https://github.com/KBlester)** — Desenvolvedor Fullstack com foco em aplicações web, APIs e sistemas.

[![Visite meu GitHub](https://img.shields.io/badge/GitHub-KBlester-181717?logo=github)](https://github.com/KBlester)

---

## 👨‍💻 Sobre o autor

**Kalebe Santos** (`KBlester`)  
*Striving daily for academic excellence, intellectual maturity, and financial independence.*

Desenvolvedor Fullstack desde os 14 anos, com experiência prática em **JavaScript, TypeScript, React, Node.js, SQL e Python**. Atualmente focado em criar interfaces, APIs, integrações e sistemas completos.

---


## ✨ Destaques

| Recurso | Descrição |
|---------|-----------|
| 🎨 **Interface moderna** | Tema escuro com cores neon e botões responsivos |
| 📜 **Histórico persistente** | Operações salvas em arquivo JSON (painel lateral) |
| 🧠 **Memória** | M+, M-, MR e MC para armazenar valores |
| ⌨️ **Teclado** | Digite diretamente usando o teclado (Enter, Backspace, Esc) |
| 🔬 **Científica** | Porcentagem, raiz quadrada, potência (x²) e negação (+/-) |
| 🖱️ **Reuso rápido** | Duplo clique no histórico para reutilizar resultados |
| 🐍 **Zero dependências** | Apenas biblioteca padrão do Python |

## 📸 Preview

```
Calculadora Neon
================
[ Display Neon ]
     0
================
[ 7 ] [ 8 ] [ 9 ] [ ÷ ]
[ 4 ] [ 5 ] [ 6 ] [ × ]
[ 1 ] [ 2 ] [ 3 ] [ - ]
[ . ] [ 0 ] [ = ] [ + ]
```

## 🚀 Como executar

### Pré-requisitos
- Python 3.10 ou superior

### Rodar localmente
```bash
# Clone o repositório
git clone https://github.com/KBlester/calculadora-neon.git
cd calculadora-neon

# Execute
python calculadora/src/main.py
```

Ou diretamente:
```bash
python calculadora/src/main.py
```

## 🛠️ Estrutura do projeto

```
calculadora/
├── src/
│   ├── main.py        # Ponto de entrada da aplicação
│   ├── calculator.py  # Lógica de cálculo (motor)
│   ├── ui.py          # Interface gráfica (Tkinter)
│   └── history.py     # Gerenciador de histórico persistente (JSON)
├── LICENSE            # Licença MIT
├── README.md          # Esta documentação
├── requirements.txt   # Dependências (apenas stdlib)
└── .gitignore         # Arquivos ignorados pelo Git
```

## 🧪 Testes

```bash
# Teste rápido da lógica
python -c "from src.calculator import Calculator; c = Calculator(); c.input_digit('5'); c.set_operation('add'); c.input_digit('3'); print(c.compute())"
# Resultado esperado: 8
```

## 🗺️ Roadmap

- [ ] Modo claro/escuro alternável
- [ ] Mais funções científicas (sin, cos, tan, log)
- [ ] Histórico exportável para CSV/TXT
- [ ] Empacotamento como executável (.exe)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Feito com ❤️ por **[Kalebe Santos](https://github.com/KBlester)** para destacar no GitHub.
