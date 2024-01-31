import g4f

text = input("Введи запрос")

response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_35_long,
    messages=[{"role": "user", "content": text}],
    stream=True,
)

for message in response:
    print(message, flush=True, end='')


''' gpt_35_long
gpt_35_turbo
 '''
