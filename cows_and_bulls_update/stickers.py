HELLO_STIC = [
    "CAACAgIAAxkBAAImoWTTdRbLykceCJmdylaj_5gBNNUrAAJZAANfrU48ZGEdxFgTJmswBA",
    "CAACAgIAAxkBAAImp2TTdlkR1E3sAAF9nM-aTdGWwxxOCwACPR8AAmvmQUkDnMUSjIR-fDAE"
]

GOODBYE_STIC = "CAACAgIAAxkBAAImu2TUf6FjjFdhuHQGnWP0-hwjEdJCAAJnAgACVp29CgfnbKzvzsg_MAQ"


import rsa

#Боб формирует публичный и секретный ключ

# (bob_pub, bob_priv) = rsa.newkeys(512)

# with open("cows_and_bulls_update/ssh/key", "w", encoding="utf-8") as file:
#     file.write(str(bob_priv))
    
# with open("cows_and_bulls_update/ssh/key.pub", "w", encoding="utf-8") as file:
#     file.write(str(bob_pub))
# with open(f"cows_and_bulls_update/ssh/key.pub", encoding="utf-8") as file:
#     public_key = file.read().split(", ")
#     public_key = [int(number) for number in public_key]
#     public_key = rsa.PublicKey(*public_key)
# with open(f"cows_and_bulls_update/coins.txt", mode ="wb") as file:
#     message = f"{17}".encode('utf8')
#     crypto = rsa.encrypt(message, public_key)
#     file.write(crypto)

