# Imagem oficial otimizada da AWS para Amazon Linux 2023
FROM public.ecr.aws/amazonlinux/amazonlinux:2023

# Boas práticas: Instalação enxuta e remoção imediata de cache de pacotes
RUN dnf install -y python3 python3-pip procps-ng && \
    dnf clean all && \
    rm -rf /var/cache/dnf /var/log/dnf*

WORKDIR /app

# Cache de dependências do Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia apenas os arquivos necessários do projeto (respeitando o .dockerignore)
COPY . .

# Permissões de execução para scripts de ciclo de vida
RUN chmod +x entrypoint.sh systemd/instalar.sh

# Ponto de entrada: orquestra a simulação completa de Boot, Execução e Shutdown
ENTRYPOINT ["/app/entrypoint.sh"]
