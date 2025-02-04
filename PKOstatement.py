import fitz  # PyMuPDF
import os

def add_text_to_pdf(input_pdf, output_pdf, positions, Statement_Num, sort):
    doc = fitz.open(input_pdf)

    if sort == "1":
        number = len(positions)
    elif sort == "2":
        number = -1

    if Statement_Num != "0":
        doc[0].insert_text((500, 40), Statement_Num, fontsize=40, color=(1, 0, 0)) 
        text_template = f"{Statement_Num}/"
    else:
        text_template = ""

    for position in positions:
        page_number = position[0]
        page = doc[page_number - 1]
        page.insert_text((450, position[1]), text_template + str(abs(number)), fontsize=20, color=(1, 0, 0))  # Red text at position (450, x[1])"
        number = number - 1

    version = 1
    new_output_pdf = output_pdf  # Inicjalizujemy zmienną nowego pliku


    while os.path.exists(new_output_pdf):
        version += 1  # Increment version number
        new_output_pdf = f"{output_pdf[:-4]}_{version}.pdf"  # Add version number to filename
    
    try:
        doc.save(new_output_pdf)
        doc.close()
        print(f"Twój wyciąg został ponumerowany i zapisany jako: \033[32m{new_output_pdf}\033[0m")
    except Exception as e:
        print(f"\033[31mNie udało się zapisać pliku: {e}\033[0m")


def find_text_positions(input_pdf):
    doc = fitz.open(input_pdf)
    positions = []
    
    for page_num, page in enumerate(doc):
        text_instances = page.search_for("identyfikator")
        for inst in text_instances:
            positions.append((page_num + 1, inst[1]))  #Page number and position

    doc.close()

    if not positions:
        print("\033[31mNie rozpoznano formatu pliku.\033[0m")
        exit()

    return positions

while True:
    try:
        print("""Podaj nazwę pliku z wyciągiem PKO
              1. Podaj nazwę bez rozszerzenia \".pdf\",
              2. Plik musi znajdować się w tym samym katalogu co program)""")
        print("Nazwa pliku: ", end="")
        input_pdf = input()
        output_pdf = input_pdf+"_PONUMEROWANY.pdf"
        input_pdf = input_pdf+".pdf"
        doc = fitz.open(input_pdf)
        doc.close()
        break
    except Exception as e:
        print("\033[31mNie udało się otworzyć pliku lub taki nie istnieje.\033[0m")

positions = find_text_positions(input_pdf)

print("Podaj numer wyciągu (wpisz 0 jeżeli nie chcesz dodawać numeru wyciągu):", end="")
Statement_Num=input()

while True:
    print("""Wybierz opcję:\n
        1. Numeruj od najstarszego do najnowszego
        2. Numeruj od najnowszego do najstarszego
        """)
    sort = input("Podaj numer opcji: ")
    if sort in ["1", "2"]: break
    else: print("\033[31mBłędny wybór!.\033[0m")


add_text_to_pdf(input_pdf, output_pdf, positions,Statement_Num, sort)