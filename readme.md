# Hello World!

Inspirado pela eficácia da metodologia Pimsleur, focada em diálogos práticos e repetição espaçada, desenvolvi um gerador de cursos de idiomas em MP3. O projeto utiliza scripts em Python e IA generativa para criar lições personalizáveis e narradas, permitindo uma experiência de aprendizado portátil e adaptada às necessidades do usuário.

## Como rodar

### Passo 1

```
./ setup.sh 
```

ou

```
python -m pip install -r requirements.txt
```

### Passo 2

Em seguida, rode o comando:

```
./python3/bin/python3 main.py example.json
``` 

ou 

```
python main.py example.json
``` 


## Passo3: Criando lições

Utilize o seguinte `prompt` para gerar uma lição em sua IA favorita:

Troque a variável `[NÍVEL]` (Ex: `A1`, `A2`, `B1`, `B2`, `C1`, `C2`, `Business`, etc.) e `[TEMA]` do prompt abaixo para o seu alvo de estudo.

Onde tem:  

`[IDIOMA_NATIVO]` troque por `pt_br` e `[IDIOMA_ALVO]` por `en_us`

### Prompt

```
Você é um linguista especialista em criação de cursos de idiomas com foco em áudio e repetição espaçada (estilo Pimsleur). 

Sua tarefa é gerar o roteiro de uma lição de idiomas no formato JSON estrito, focado no nível [NÍVEL] e sobre o tema [TEMA].

### DIRETRIZES DO CURSO:
1. Nível de Dificuldade: O vocabulário, a gramática e as expressões utilizadas no diálogo devem corresponder estritamente ao nível [NÍVEL].
2. Tamanho do Diálogo: O diálogo deve ser curto, natural e direto, contendo entre 4 a 8 frases no máximo. Deve soar como uma conversa real do dia a dia.
3. Target Words (Palavras-alvo): 
   - Escolha de 3 a 5 palavras ou expressões-chave do diálogo que sejam as mais desafiadoras ou importantes para o nível [NÍVEL].
   - Os arrays `target_words_[idioma_nativo]` e `target_words_[idioma_alvo]` devem ter EXATAMENTE o mesmo tamanho.
   - A palavra no índice 0 de um array deve ser a tradução exata da palavra no índice 0 do outro array.
   - Use palavras no infinitivo ou em sua forma base, a menos que a conjugação específica seja o foco da lição.
4. Vozes: Defina vozes neurais padrão da Microsoft (Edge TTS) compatíveis com os idiomas escolhidos. O Narrador sempre fala no idioma nativo. "person_1" e "person_2" falam no idioma alvo.

### IDIOMAS:
- Idioma Nativo: [IDIOMA_NATIVO]
- Idioma Alvo: [IDIOMA_ALVO]

### FORMATO DE SAÍDA EXIGIDO:
Você deve retornar APENAS um JSON válido, sem nenhum texto adicional, explicações ou blocos de formatação markdown antes ou depois. Use a estrutura exata abaixo:

{
    "[IDIOMA_NATIVO]": [ 
        { "person_1": "Frase 1 traduzida" }, 
        { "person_2": "Frase 2 traduzida" }
    ],
    "[IDIOMA_ALVO]": [ 
        { "person_1": "Frase 1 original" }, 
        { "person_2": "Frase 2 original" }
    ],
    "target_words_[IDIOMA_NATIVO]": ["palavra1", "palavra2", "palavra3"],
    "target_words_[IDIOMA_ALVO]": ["word1", "word2", "word3"],
    "voices": {
        "narrator": "pt-BR-AntonioNeural",
        "person_1": "en-US-JennyNeural",
        "person_2": "en-US-GuyNeural"
    }
}
```

Como output da IA, você terá um json, que poderá utilizar para rodar o script como nos passo 2 

## Passo 4: Rodando o Script

```
./python3/bin/python3 main.py [MEU_CURSO].json
``` 

ou

```
python main.py [MEU_CURSO].json
``` 


## Sugestão de Temas:

✈️ Viagens e Turismo (Sobrevivência)
Geralmente ideais para níveis A1 e A2 (Iniciante / Básico):

- "Fazendo o check-in no hotel e perguntando a senha do Wi-Fi."

- "Pedindo informações na rua para chegar à estação de trem."

- "Passando pela imigração e respondendo qual o motivo da viagem."

- "Pedindo a conta em um restaurante e perguntando se aceita cartão."

- "Comprando uma passagem de ônibus e perguntando o horário de partida."

💼 Negócios e Trabalho (Business)
Ideais para níveis B1, B2 e Business (Intermediário / Avançado):

- "Remarcando uma reunião de última hora com um cliente."

- "Apresentando-se no primeiro dia de trabalho em um novo escritório."

- "Negociando o prazo de entrega de um projeto com o chefe."

- "Fazendo networking no intervalo para o café de uma conferência."

- "Pedindo feedback sobre uma apresentação recente."

🤝 Vida Cotidiana e Socialização
Podem ser adaptados para qualquer nível (do A1 ao C1):

- "Encontrando um velho amigo na rua e perguntando das novidades." (B1)

- "Convidando um colega para tomar uma cerveja ou café na sexta-feira." (A2)

- "Reclamando educadamente com o vizinho sobre o barulho alto." (B2)

- "Discutindo o enredo de um filme ou série que acabaram de assistir." (B1)

- "Comprando roupas e pedindo um tamanho maior para o vendedor." (A1)

🚨 Saúde e Emergências
Fundamentais para níveis A2 e B1:

- "Explicando para o médico os sintomas de uma gripe ou dor de estômago."

- "Indo à farmácia comprar um remédio para dor de cabeça."

- "Reportando a perda de um passaporte ou carteira na delegacia."

- "Explicando que você tem uma alergia alimentar grave em um restaurante."

❤️ Relacionamentos e Romance
Para deixar o estudo mais divertido e dinâmico:

- "Convidando alguém para sair no primeiro encontro."

- "Elogiando a roupa de alguém e puxando assunto na festa."

- "Conhecendo os sogros pela primeira vez em um jantar."

## Exemplo de prompt

```
Você é um linguista especialista em criação de cursos de idiomas com foco em áudio e repetição espaçada (estilo Pimsleur). 

Sua tarefa é gerar o roteiro de uma lição de idiomas no formato JSON estrito, focado no nível A2 e sobre o tema "Fazendo o check-in no hotel e perguntando a senha do Wi-Fi.".

### DIRETRIZES DO CURSO:

1. Nível de Dificuldade: O vocabulário, a gramática e as expressões utilizadas no diálogo devem corresponder estritamente ao nível A2.
2. Tamanho do Diálogo: O diálogo deve ser curto, natural e direto, contendo entre 4 a 8 frases no máximo. Deve soar como uma conversa real do dia a dia.
3. Target Words (Palavras-alvo): 
   - Escolha de 3 a 5 palavras ou expressões-chave do diálogo que sejam as mais desafiadoras ou importantes para o nível A2.
   - Os arrays `target_words_pt_br` e `target_words_en_us` devem ter EXATAMENTE o mesmo tamanho.
   - A palavra no índice 0 de um array deve ser a tradução exata da palavra no índice 0 do outro array.
   - Use palavras no infinitivo ou em sua forma base, a menos que a conjugação específica seja o foco da lição.
4. Vozes: Defina vozes neurais padrão da Microsoft (Edge TTS) compatíveis com os idiomas escolhidos. O Narrador sempre fala no idioma nativo. "person_1" e "person_2" falam no idioma alvo.

### IDIOMAS:

- Idioma Nativo: pt_br
- Idioma Alvo: en_us

### FORMATO DE SAÍDA EXIGIDO:

Você deve retornar APENAS um JSON válido, sem nenhum texto adicional, explicações ou blocos de formatação markdown antes ou depois. Use a estrutura exata abaixo:

{
    "pt_br": [ 
        { "person_1": "Frase 1 traduzida" }, 
        { "person_2": "Frase 2 traduzida" }
    ],
    "en_us": [ 
        { "person_1": "Frase 1 original" }, 
        { "person_2": "Frase 2 original" }
    ],
    "target_words_pt_br": ["palavra1", "palavra2", "palavra3"],
    "target_words_en_us": ["word1", "word2", "word3"],
    "voices": {
        "narrator": "pt-BR-AntonioNeural",
        "person_1": "en-US-JennyNeural",
        "person_2": "en-US-GuyNeural"
    }
}
```