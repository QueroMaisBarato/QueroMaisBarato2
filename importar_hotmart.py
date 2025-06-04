import requests
from bs4 import BeautifulSoup
from catalog.models import Category, Product
from django.utils.text import slugify
from django.core.files import File
import os
from requests.exceptions import RequestException, ConnectionError, Timeout, TooManyRedirects
import time

# -------- SUA LISTA DE LINKS --------
links = [
    "https://go.hotmart.com/H100053671N?dp=1",
    "https://go.hotmart.com/K100053692Y?dp=1",
    "https://go.hotmart.com/X100053734A?dp=1",
    "https://go.hotmart.com/D100053883X",
    "https://go.hotmart.com/G100053988E?dp=1",
    "https://go.hotmart.com/X100054040A?dp=1",
    "https://go.hotmart.com/K100054053R?dp=1",
    "https://go.hotmart.com/E100054062A",
    "https://go.hotmart.com/Q100054155F?dp=1",
    "https://go.hotmart.com/G100051547C?dp=1",
    "https://go.hotmart.com/H100051580R?dp=1",
    "https://go.hotmart.com/H100052120E?dp=1",
    "https://go.hotmart.com/P100051654A?dp=1",
    "https://go.hotmart.com/V100051673U?dp=1",
    "https://go.hotmart.com/D100051691O?dp=1",
    "https://go.hotmart.com/G100051729R?ap=2347",
    "https://go.hotmart.com/B100051737D?ap=776e",
    "https://go.hotmart.com/I100051805M?dp=1",
    "https://go.hotmart.com/T100051815W?dp=1",
    "https://go.hotmart.com/B100051872B?dp=1",
    "https://go.hotmart.com/H100051896X?dp=1",
    "https://go.hotmart.com/W100051926W?dp=1",
    "https://go.hotmart.com/T100051966C?dp=1",
    "https://go.hotmart.com/J100051977I?dp=1",
    "https://go.hotmart.com/Q100051995L?dp=1",
    "https://go.hotmart.com/G100052055K?dp=1",
    "https://go.hotmart.com/R100052089A?dp=1",
    "https://go.hotmart.com/H100052120E?dp=1",
    "https://go.hotmart.com/W100052128T?dp=1",
    "https://go.hotmart.com/U100052174W",
    "https://go.hotmart.com/U100052174W",
    "https://go.hotmart.com/Q100052215G",
    "https://go.hotmart.com/D100052241P?dp=1",
    "https://go.hotmart.com/E100052259V?dp=1",
    "https://go.hotmart.com/V100052336C?dp=1",
    "https://go.hotmart.com/P100052343Y?dp=1"
]

IMAGE_PATH = os.path.abspath('imagens/teste.png')

# -------- BUSCA CATEGORIA EXISTENTE PELO SLUG --------
category_slug = "cursos-digitais"
try:
    category = Category.objects.get(slug=category_slug)
except Category.DoesNotExist:
    print(f"Categoria com slug '{category_slug}' não existe! Crie-a antes de rodar o script.")
    exit()

def get_hotmart_data(url, max_retries=3, retry_delay=2):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            
            # Nome
            name = "Curso Hotmart"
            h1 = soup.find("h1")
            if h1:
                name = h1.get_text(strip=True)
            elif soup.title:
                name = soup.title.get_text(strip=True)
            
            # Descrição
            desc = ""
            desc_tag = soup.find("p")
            if desc_tag:
                desc = desc_tag.get_text(strip=True)
            else:
                meta = soup.find("meta", attrs={"name": "description"})
                if meta:
                    desc = meta["content"]
            
            # Imagem
            img_url = None
            img_tag = soup.find("img")
            if img_tag and img_tag.get("src"):
                img_url = img_tag["src"]
            
            # Preço
            price = 0.0
            price_tag = soup.find("span", class_="price")
            if price_tag:
                try:
                    price_text = price_tag.get_text(strip=True).replace("R$", "").replace(".", "").replace(",", ".").strip()
                    price = float(price_text)
                except (ValueError, AttributeError):
                    price = 0.0
            
            return {
                "name": name,
                "description": desc,
                "image_url": img_url,
                "price": price,
                "external_url": url
            }
            
        except ConnectionError as e:
            if attempt < max_retries - 1:
                print(f"Erro de conexão ao acessar {url}. Tentativa {attempt + 1} de {max_retries}. Aguardando {retry_delay} segundos...")
                time.sleep(retry_delay)
                continue
            print(f"Não foi possível conectar ao site {url} após {max_retries} tentativas.")
            return None
            
        except Timeout as e:
            if attempt < max_retries - 1:
                print(f"Timeout ao acessar {url}. Tentativa {attempt + 1} de {max_retries}. Aguardando {retry_delay} segundos...")
                time.sleep(retry_delay)
                continue
            print(f"Timeout ao acessar {url} após {max_retries} tentativas.")
            return None
            
        except TooManyRedirects as e:
            print(f"Erro de redirecionamento ao acessar {url}")
            return None
            
        except RequestException as e:
            print(f"Erro ao acessar {url}: {str(e)}")
            return None
            
        except Exception as e:
            print(f"Erro inesperado ao processar {url}: {str(e)}")
            return None
    
    return None

def create_product_with_fallback(data, category):
    if not data:
        return None
        
    try:
        # Cria o produto com dados básicos
        product = Product(
            category=category,
            name=data["name"],
            description=data["description"],
            price=data["price"],
            external_url=data["external_url"]
        )
        
        # Tenta baixar a imagem se houver URL
        if data["image_url"]:
            try:
                img_response = requests.get(data["image_url"], timeout=10)
                img_response.raise_for_status()
                
                # Salva a imagem temporariamente
                temp_img_path = f"temp_{slugify(data['name'])}.jpg"
                with open(temp_img_path, 'wb') as f:
                    f.write(img_response.content)
                
                # Adiciona a imagem ao produto
                with open(temp_img_path, 'rb') as f:
                    product.image.save(f"{slugify(data['name'])}.jpg", File(f), save=False)
                
                # Remove o arquivo temporário
                os.remove(temp_img_path)
            except Exception as e:
                print(f"Erro ao baixar imagem para {data['name']}: {str(e)}")
                # Usa imagem padrão se falhar
                with open(IMAGE_PATH, 'rb') as f:
                    product.image.save("default.jpg", File(f), save=False)
        else:
            # Usa imagem padrão se não houver URL
            with open(IMAGE_PATH, 'rb') as f:
                product.image.save("default.jpg", File(f), save=False)
        
        product.save()
        return product
        
    except Exception as e:
        print(f"Erro ao criar produto {data['name']}: {str(e)}")
        return None

# -------- PROCESSAMENTO DOS LINKS --------
print(f"Iniciando importação de {len(links)} produtos...")
successful_imports = 0
failed_imports = 0

for url in links:
    print(f"\nProcessando: {url}")
    data = get_hotmart_data(url)
    
    if data:
        product = create_product_with_fallback(data, category)
        if product:
            print(f"Produto '{product.name}' importado com sucesso na categoria {category.name}!")
            successful_imports += 1
        else:
            print(f"Falha ao criar produto para {url}")
            failed_imports += 1
    else:
        print(f"Não foi possível obter dados do produto em {url}")
        failed_imports += 1

print(f"\nResumo da importação:")
print(f"Total de links processados: {len(links)}")
print(f"Importações bem-sucedidas: {successful_imports}")
print(f"Importações com falha: {failed_imports}")