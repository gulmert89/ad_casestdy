# 1. Data Scientist Case Study
Case study kapsamında verilen bir stock photo ve prompt ile Stable Diffusion kullanarak
benzer tarzda yeni bir görsel oluşturulmasını istiyoruz. Ürettiğiniz görseli ve vereceğimiz
diğer inputları kullanarak basit bir dinamik reklam template’i oluşturmanızı istiyoruz.
Hazırladığınız bu çalışmayı API yoluyla bizimle paylaşmanızı bekliyoruz. Aşağıda gerekli
step’leri bulabilirsiniz:

- **Task 1:** Stable Diffusion’un Img2Img algoritmasını kullanarak verilen görsele benzer yeni
bir görsel üretmek. Bunu seçeceğiniz hazır bir modelle yapabilirsiniz. Üretilen görselde
bizim verdiğimiz bir rengin de kullanılmasını bekliyoruz.
    - Input: Image (png), Prompt (text), Renk (hex code)
    - Output: Image
- **Task 2:** Üretilen görseli ve diğer inputları kullanarak basit bir dinamik reklam template’i
üretmek. En tepede logo, ortada görsel, altında punchline ve en altta button olacak şekilde tasarlayabilirsiniz. Button’un ve punchline’ın rengi ayrı bir input olarak verilecek.
Aşağıdaki örnek görsele çok benzer bir çıktı üretmenizi bekliyoruz.
    - **Input:** Task 1’deki image, Logo (png), Renk (hex code), Punchline (text), Button (text)
    - **Output:** Image (png veya svg)

![case sample](case_sample.png)
- Task 3: Tasarladığınız bu sistemi cloud üzerinde veya kendi bilgisayarınızı kullanarak
deploy etmenizi ve API yoluyla ulaşılabilir olmasını istiyoruz. Bunun için istediğiniz
teknolojik altyapıları kullanabilirisiniz. API yoluyla bahsedilen inputları alacak ve reklam
görseli döndürecek bir yapı kurmanızı bekliyoruz.

**Bonus:** Aynı anda birden fazla request alabilen ve paralel çalışabilen bir yapı kurmak.

# 2. Mert's Solution
Aşağıda, AWS üzerinde çalıştırdığım makinenin linki bulunuyor.
8GB RAM'e sahip cpu-only bir makine. Aynı anda 2 worker çalıştırdığım için (bonus point'te bahsedilen), 2 adet paralel request alabiliyor. Tabii -maliyetinden dolayı- seçtiğim makine, GPU olmadığı için 20 inference step, yaklaşık 5-10 dakika arası sürebiliyor.

Aşağıdaki linkten, FastAPI'nin Swagger UI'ını kullanarak modeli deneyebilirsiniz. Ben yine de örnek curl request'leri de koydum "appendix" kısmına.

* **Deployed case study:** http://52.208.57.153:8000/docs
* **create_image endpoint'i:** Task 1
* **create_ad endpoint'i:** Task 2

Ayrıca ekte, üç task'ın da `.py` uzantılı dosyaları mevcut.

Direkt olarak, `task3.py` üzerinden<br>

`> uvicorn task3:case_app --host 0.0.0.0 --port 8000 --workers 2`<br>

kodu ile, gerekli paketleri yükledikten sonra server'i kendi bilgisayarınızda ayağa kaldırabilirsiniz.

Hepinize iyi çalışmalar dilerim.

### Appendix:
**Task 1:** Img2Img ile Yeni Görsel Üretmek
* prompt: "a cup of coffee"
* hex color: "670E94"
* inference steps: 10
* inference seed: 42
* uploaded_img: "reference_img.jpg"

```bash
curl -X 'POST' \
  'http://52.208.57.153:8000/create_image?text_prompt=a%20cup%20of%20coffee&color_hex=670E94&inference_steps=10&inference_seed=42' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'reference_img=@reference_img.jpg;type=image/jpeg' \
--output "my_generated_img_1.png"
```


**Task 2:** Reklam Template'i Yaratmak
- punchline: "This is the best coffee you will ever drink."
- button text: "Click here!"
- hex color: "551122"
- uploaded_base_img: "my_generated_img.jpg"
- uploaded_logo: "my_logo.png"

```bash
curl -X 'POST' \
  'http://52.208.57.153:8000/create_ad?punchline=This%20is%20the%20best%20coffee%20you%20will%20ever%20drink.&button_text=Click%20here%21&color_hex=551122' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'uploaded_base_img=@reference_img.jpg;type=image/jpeg' \
  -F 'uploaded_logo=@logo_wide.png;type=image/png' --output "my_generated_ad_1.png"
```
