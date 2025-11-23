with open("backend_py\\ids_detection_model.ubj", 'rb') as f:
    header = f.read(100)  # Lê os primeiros 100 bytes
    print("Cabeçalho do arquivo:", header)