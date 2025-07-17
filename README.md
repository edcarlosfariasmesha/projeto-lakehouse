# Objetivo  
O objetivo desta POC (Prova de conceito) e montar uma plataforma de dados   mínima usando ferramentas de código aberta. 

# Objetivos específicos  
- Montar uma plataforma de dados mínima com as camadas de orquestração, processamento e armazenamento 
- Usar ferramentas de código aberto 

# Ferramentas usadas  
- [airflow - 3.0.2](https://airflow.apache.org/docs/apache-airflow/stable/index.html)  
- [pyspark - 4.0.0](https://spark.apache.org/docs/latest/api/python/index.html#)  
- [delta lake - 4.0.0](https://docs.delta.io/latest/index.html)
- [minio - RELEASE.2025-04-22T22-12-26Z](https://min.io/docs/minio/kubernetes/upstream/index.html)
- [papermil - 2.4.0](https://papermill.readthedocs.io/en/latest/index.html)  

# Configuração dos serviços  
> Atenção! Este projeto deve ser executado em uma maquina Linux ou wsl2 do windows  
> 
> Para saber mais sobre wsl2 click [aqui](https://learn.microsoft.com/pt-br/windows/wsl/about)  

## 0 - Pré-requisitos    
- Certifique-se de ter o Docker e Docker Compse instalados na sua máquina.    
- Para instalar o Docker, click [aqui](https://docs.docker.com/engine/install/)   
- Para instalar o Docker Compose, clique [aqui](https://docs.docker.com/compose/install/)    

## 1 - Abra o terminal de sua preferência  
- No Windows, click [aqui](https://elsefix.com/pt/tech/tejana/how-to-use-windows-terminal-in-windows-10-beginners-guide) para saber como abrir um terminal.  
- No Linux, click [aqui](https://pt.linux-console.net/?p=12268) para saber como abrir um terminal.  

## 2 - Clone do repositorio  
- Click [aqui](https://docs.github.com/pt/repositories/creating-and-managing-repositories/cloning-a-repository) e siga o passo de como clonar um respositório do github  

## 3 - Mude para a pasta do projeto  
~~~bash  
$ cd projeto-lakehouse  
~~~  

## 4 - Configure uma rede externa do docker  
~~~bash  
$ docker network create projeto-lakehouse  
~~~  

## 5 - Crie o arquivo .env baseado no .env.template  
~~~bash  
$ cp .env.template .env  
~~~  

## 6 - Abra um editor de código de sua preferência.  
> Sugestão! Use o vscode.  
- No Windows com wsl2, click [aqui](https://learn.microsoft.com/pt-br/windows/wsl/tutorials/wsl-vscode) para saber como instalar e usar.  
- No Linux, click [aqui](https://code.visualstudio.com/docs/setup/linux) para saber como instalar e usar.  

## 7 - Abra o arquivo .env e preencha os valores das variáveis  

## 8 - Volte para o terminal e execute o comando abaixo para iniciar os serviços  
~~~bash  
$ docker compose up  
~~~  
Este comando deixa o terminal preso, se preferir pode usar o comando abaixo para iniciar os serviços e liberar o terminal  
~~~bash  
$ docker compose up -d  
~~~  
  
## 9 - Verifique o status dos serviços Docker  
~~~bash  

$ docker ps

~~~  
Você deverá ver os contêineres para Airflow (database, scheduler, worker), MinIO, Postgres, etc., com o status Up.  

Para verificar os logs de um serviço específico (substitua airflow_api_server pelo nome do serviço que deseja inspecionar, como minio, airflow_scheduler etc.):  

~~~bash  

$ docker compose logs -f airflow_dag-processor

~~~  
Pressione Ctrl + C para sair dos logs.  

## 10 - Acesse as interfaces dos serviços  

  Acesse o MinIO pela interface web em:  

~~~bash 

http://localhost:10000  

~~~ 

Conforme definido no docker-compose.yml, certifique-se de que essa porta foi mapeada corretamente no seu ambiente.  

Faça login utilizando as credenciais definidas no arquivo .env:  

Access Key: MINIO_ROOT_USER  

Key: MINIO_ROOT_PASSWORD  

Para a criação dos buckets, após o login, siga os passos abaixo que representam as camadas da arquitetura de medalhão: 

No menu lateral esquerdo, clique em Administrator. 

Em seguida, clique em Buckets. 

No canto superior direito da tela, clique em Create Bucket. 

Crie o bucket inicial chamado landing e clique em Create Bucket para confirmar. 

Para verificar a criação, acesse o menu Object Browser (no menu esquerdo) e confira se o bucket landing aparece na lista. 

Repita o processo para criar os demais buckets necessários, como: bronze, silver, gold, entre outros. 

Esses buckets serão usados para armazenar os dados nos diferentes estágios de processamento do pipeline. 


## 11 - Configuração da conexão do MinIO 

Para permitir a comunicação entre o pipeline e o MinIO, foi necessário configurar uma conexão chamada minio_connection. 

Essa configuração foi realizada dentro do notebook, por meio da criação de um arquivo .json com as credenciais e o endpoint de acesso. O arquivo foi salvo no seguinte caminho: 

src/dags/geography/coordinates/variables/minio_connection.json 
O conteúdo do arquivo inclui as seguintes informações: 

"endpoint": URL interna de acesso ao MinIO 

"access_key": chave de acesso (gerada pelo MinIO)

"key": chave secreta (também gerada pelo MinIO)

Como gerar as credenciais: 

Acesse o MinIO pela interface web (http://localhost:10000).

No menu lateral, clique em Access Keys.

Clique em Create Access Key.

Copie os valores de Access Key e Secret Key gerados.

Preencha o arquivo minio_connection.json com essas informações.

Esse arquivo será utilizado posteriormente para autenticação automática nas DAGs ou scripts que interagem com o armazenamento do MinIO.

## 12 - Configuração do ambiente de desenvolvimento

Ambiente Python com uv, clique [aqui](https://docs.astral.sh/uv/) para saber como instalar e usar.

Após configurar os serviços, o ambiente Python foi instalado e gerenciado com a ferramenta uv, que oferece uma forma rápida e moderna de instalar dependências Python. 

O terminal foi aberto na pasta raiz do projeto dentro do VSCode, onde o comando de instalação das dependências foi executado (com base no arquivo pyproject.toml).

~~~bash 

uv sync 

~~~ 

O teste de funcionamento foi bem-sucedido. A aplicação Spark processou os dados conforme o esperado e os arquivos foram salvos corretamente no MinIO no formato Delta Lake. Isso valida a capacidade do ambiente de:

Processar dados com Apache Spark.

Utilizar as capacidades transacionais e de versionamento do Delta Lake.

Persistir dados de forma eficiente em um armazenamento de objetos compatível com S3 (MinIO).

A arquitetura demonstrada aqui estabelece uma base sólida para pipelines de dados escaláveis e confiáveis, utilizando tecnologias de código aberto para gerenciamento de data lakes.

## 13 Validando de infraestrura: Spark, Delta Lake e MinIO para um Data Lake 

Este repositório documenta um teste de validação da infraestrutura de dados, executado localmente no VS Code. O objetivo foi verificar se a escrita de dados no formato Delta Lake para um bucket MinIO (rodando via Docker) funcionava corretamente utilizando o Apache Spark com PySpark. 

O que foi testado: 

Execução local do código PySpark no VS Code, arquivo : src_lnd_geography_coordinates.ipynb 

Gravação de arquivos Delta (.parquet) em um bucket MinIO (S3 compatível) 

Integração com bibliotecas essenciais: delta-spark, hadoop-aws, aws-java-sdk 

Persistência bem-sucedida dos dados, com estrutura Delta armazenada no MinIO 

Resultado: A escrita no formato Delta funcionou conforme esperado, validando a comunicação entre Spark e MinIO e confirmando que a infraestrutura está pronta para os próximos passos do pipeline. 



