mkdir -p klirssia/resultado            # Cria a pasta "klirssia" e a subpasta "resultado"
curl -O https://vanilton.net/v1/download/zip.zip  # Baixa o arquivo zip para o diretório atual
unzip zip.zip -d klirssia               # Descompacta o arquivo zip na pasta "klirssia"
mv klirssia/* klirssia/resultado/       # Move o conteúdo descompactado para a pasta "resultado"
rm zip.zip                              # Remove o arquivo zip baixado
